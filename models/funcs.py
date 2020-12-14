import os

import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.classes import Post, Comment, User, Rating

os.getenv("WEATHER_API")

postgre_username = os.getenv("POSTGRE_USERNAME")
postgre_password = os.getenv("POSTGRE_PASS")


engine = create_engine(f"postgresql://{postgre_username}:{postgre_password}@blackitreddit.herokuapp.com/blackit, echo=False") #database
Session = sessionmaker(bind=engine)
session = Session()


def user_exist(session, check_name, check_email):
    for instance in session.query(User):
        if instance.name == check_name or instance.email == check_email:
            return True
    return False


def email_exist(session, check_email):
    for instance in session.query(User):
        if instance.email == check_email:
            return True
    return False


def create_user(session, new_name, new_email, new_password):
    if not user_exist(session, new_name, new_email):
        hash_pass = encrypt_password(new_password)
        instance = User(name=new_name, password=hash_pass, email=new_email)
        session.add(instance)
        session.commit()
        return instance.id
    else:
        return False


def change_password(session, name, new_password):
    instance = session.query(User).filter(User.name == name).first()
    instance.password = new_password
    session.commit()
    return True


def check_if_commented(session, post_id, user_id):
    for instance in session.query(Comment):
        if instance.post_id == post_id and instance.author == user_id:
            return True
    return False


def rate_post(session, post_id, rating):
    instance = session.query(Post).filter(Post.id == post_id).first()
    if rating == like.id:
        instance.likes += 1
    elif rating == dislike.id:
        instance.dislikes += 1


def comment(session, post_id, user_id, content, rating):
    if not check_if_commented(session, post_id, user_id):
        instance = Comment(post_id=post_id, author=user_id, content=content, rating=rating)
        session.add(instance)
        rate_post(session, post_id, rating)
        session.commit()
        return True
    else:
        return False


def post(session, user_id, title, content):
    instance = Post(author=user_id, title=title, content=content, dislikes=0, likes=0)
    session.add(instance)
    session.commit()
    return True


def calculate_rating(session, post_id):
    instance = session.query(Post).filter(Post.id == post_id).first()

    if instance:
        try:
            rating = (instance.likes / (instance.likes + instance.dislikes)) * 100
        except ZeroDivisionError:
            return None
        else:
            return rating
    return None


def encrypt_password(password):
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(rounds=12, prefix=b'2b'))


def delete_comments(session, user_id):
    comments = session.query(Comment).filter(Comment.author == user_id).all()
    for i in comments:
        session.delete(i)
    session.commit()
    return True


def delete_posts(session, user_id):
    posts = session.query(Post).filter(Post.author == user_id).all()
    for i in posts:
        for c in i.comments:
            session.delete(c)
        session.delete(i)
    session.commit()
    return True


def delete_user(session, user_id):
    delete_comments(session, user_id)
    delete_posts(session, user_id)
    user = session.query(User).filter(User.id == user_id).first()
    session.delete(user)
    session.commit()
    return True


def get_posts_date():
    return session.query(Post).order_by(Post.date_published.desc()).all()


def get_posts_rating():
    return session.query(Post).order_by(Post.likes.desc()).all()


like = Rating(name='like')
dislike = Rating(name='dislike')
