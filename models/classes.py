from sqlalchemy import Column, ForeignKey, Integer, String, LargeBinary
from sqlalchemy.orm import backref, relationship
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import DateTime, VARCHAR


Base = declarative_base()


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    author = Column(Integer, ForeignKey('users.id'), nullable=False)
    date_published = Column(DateTime(timezone=True), default=func.now())
    title = Column(String, nullable=False)
    content = Column(VARCHAR, nullable=False)
    dislikes = Column(Integer)
    likes = Column(Integer)

    comments = relationship("Comment", backref="post_comments")

    def as_dict(self):
        return {str(c.name): str(getattr(self, c.name)) for c in self.__table__.columns}


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    author = Column(Integer, ForeignKey('users.id'), nullable=False)
    date_published = Column(DateTime(timezone=True), default=func.now())
    content = Column(VARCHAR, nullable=False)
    rating = Column(Integer, ForeignKey('rating.id'), nullable=False)


class Rating(Base):
    __tablename__ = 'rating'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    comments = relationship("Comment", backref="rating_comments")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    name = Column(String(35), unique=True)
    password = Column(LargeBinary)
    email = Column(VARCHAR, unique=True)

    posts = relationship("Post", backref="user_posts")
    comments = relationship("Comment", backref="user_comments")   

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return self.id
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')