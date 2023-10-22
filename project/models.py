from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from project import login_manager, db, app

class TimedBase(db.Model):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())


@login_manager.user_loader
def load_user(user_id: int):
    """
    The function `load_user` loads a user from the database based on their user ID.
    
    :param user_id: The user_id parameter is the unique identifier of the user that we want to load from
    the database
    :return: the user object with the specified user_id.
    """
    with app.app_context():
        user: User | None = User.query.filter_by(id=user_id).first()
    return user


# The `User` class represents a user in a web application, with attributes such as email, username,
# password, and profile image.
class User(TimedBase, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    profile_img: Mapped[str] = mapped_column(
        String(64), nullable=False, default="default_profile.png"
    )
    email: Mapped[str] = mapped_column(
        String(64), nullable=False, unique=True, index=True
    )
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(128))
    posts: Mapped[list["BlogPost"]] = relationship(back_populates="author", passive_deletes=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.username} | email: {self.email}"

    def check_password(self, password):
        """
        The function is used to check the validity of a password.
        
        :param password: The `password` parameter is a string that represents the password that needs to be
        checked
        """
        return check_password_hash(self.password_hash, password)
    
    def json(self):
        """
        The function is used to convert User data to JSON format.
        """
        return {
            "user_id" : self.id,
            "username": self.username,
            "email": self.email,
            "profile_img": self.profile_img,
            "created_at" : self.created_at,
            "posts": len(self.posts)
        }


class BlogPost(TimedBase):
    __tablename__ = "blogposts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(128),nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)
    author: Mapped["User"] = relationship(back_populates="posts")
    
    def __init__(self, user_id, title, text):
        self.user_id = user_id
        self.title = title
        self.text = text
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: Title: {self.title} | Created at: {self.created_at}\n{self.text}"
    
    def json(self):
        """
        The function is used to convert BlogPost data to JSON format.
        """
        return {
            "author": self.author.username,
            "created_at": self.created_at,
            "author_id": self.user_id,
            "title": self.title,
            "text": self.text.strip(),
        }
    
