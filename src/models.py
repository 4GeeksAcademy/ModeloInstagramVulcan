from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(50), nullable=False)
    lastname: Mapped[str] = mapped_column(
        String(50), nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "lastname": self.lastname,
            "email": self.email,
        }

    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    comments: Mapped[list["Comment"]] = relationship(back_populates="user")
    featured: Mapped[list["Featured"]] = relationship(back_populates="user")


class Post(db.Model):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    media: Mapped[str] = mapped_column(String(50))

    user: Mapped["User"] = relationship(back_populates="posts")
    featured: Mapped[list["Featured"]] = relationship(back_populates="post")
    comments: Mapped[list["Comment"]] = relationship(back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "media": self.media,
        }

class Comment(db.Model):
    __tablename__ = "comment"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    text: Mapped[str] = mapped_column(
        String(250), nullable=False)

    user: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "text": self.text,
        }

class Featured(db.Model):
    __tablename__ = "featured"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))


    user: Mapped["User"] = relationship(back_populates="featured")
    post: Mapped["Post"] = relationship(back_populates="featured")


    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id" : self.post_id,
        }