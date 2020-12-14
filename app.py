import random
import string

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_util_js import FlaskUtilJs

from models.funcs import bcrypt, session
from models.funcs import calculate_rating, comment, create_user, delete_user, post

from models.classes import Comment, Post, User, Rating


app = Flask(__name__)
fujs = FlaskUtilJs(app)

app.config['SECRET_KEY'] = ''.join(random.choices(string.printable, k=22))

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).filter(User.id == user_id).first()


@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        try:
            email = request.form["email"]
            password = request.form["password"]
        except (TypeError, Flask.werkzeug.exceptions.BadRequestKeyError) as error:
            return redirect(url_for('incorrect'))
        else:
            if email and password:
                instance = session.query(User).filter(User.email == email).first()
                if instance:
                    if bcrypt.checkpw(password.encode('utf8'), instance.password):
                        login_user(instance)
                        return redirect(url_for('sort_rating'))
            return redirect(url_for('incorrect'))
    else:
        return render_template('index.j2')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/home/sort-rating')
@login_required
def sort_rating():
    if current_user:
        path = '/fetch/rating'
        return render_template('home.j2', path=path)
    return redirect(url_for('index'))


@app.route('/home/sort-date')
@login_required
def sort_date():
    if current_user:
        path = '/fetch/date'
        return render_template('home.j2', path=path)
    return redirect(url_for('index'))


@app.route('/post/<int:post_id>')
@login_required
def post_template(post_id):
    post = session.query(Post).filter(Post.id == post_id).first()
    calc_rating = calculate_rating(session, post_id)
    if calc_rating:
        rating = calc_rating
    else:
        rating = 'No votes yet.'
    
    comments = session.query(Comment).filter(Comment.post_id == post_id).order_by(Comment.date_published.desc()).all()
    return render_template('post_template.j2', post=post, rating=rating, comments=comments)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            username = request.form['username']
            email = request.form['email']
            raw_password = request.form['password']
        except (TypeError, Flask.werkzeug.exceptions.BadRequestKeyError) as error:
            return redirect(url_for('incorrect'))
        else:
            if username and email and raw_password:
                test = create_user(session, username, email, raw_password)
                if test:
                    return redirect(url_for('index'))

            return redirect(url_for('incorrect'))
    else:
        return render_template('register.j2')


@app.route('/write', methods=["POST", "GET"])
@login_required
def write():
    if request.method == "POST":
        if current_user:
            title = request.form["title"]
            content = request.form["editordata"]

            if title and content:
                post(session, current_user.id, title, content)
                new_post = session.query(Post).filter(Post.title == title).first()
                post_id = new_post.id
                return redirect(url_for('post_template', post_id=post_id))
    
    return render_template('write.j2')


@app.route('/account/<int:user_id>', methods=["POST", "GET"])
@login_required
def account(user_id):
    user_id = current_user.id
    user = session.query(User).filter(User.id == user_id).first()

    if request.method == "POST":
        delete_user(session, user.id)
        return redirect(url_for('index'))
    else:
        return render_template('account.j2', user=user)


@app.route('/<int:post_id>/comment', methods=["POST", "GET"])
@login_required
def comment_post(post_id):
    if request.method == "POST":
        if current_user:
            content = request.form["content"]
            rating = request.form["rating"]
            if int(rating) == 1:
                rating = session.query(Rating).filter(Rating.id == 1).first()
            else:
                rating = session.query(Rating).filter(Rating.id == 2).first()

            comment(session=session, post_id=post_id, user_id=current_user.id, content=content, rating=rating.id)
            return redirect(url_for('sort_rating'))
    else:
        return render_template('comment-template.j2')
            

@app.route('/incorrect')
def incorrect():
    return render_template('incorrect.j2')


@app.route('/fetch/date')
def fetch_date():
    posts = [i.as_dict() for i in session.query(Post).order_by(Post.date_published.desc()).all()]
    return jsonify(posts)


@app.route('/fetch/rating')
def fetch_rating():
    posts = [i.as_dict() for i in session.query(Post).order_by(Post.likes.desc()).all()]
    return jsonify(posts)


if __name__ == '__main__':
    app.run(debug=True)