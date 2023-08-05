from schema_creator import *

from erdiagram import ER

from random import Random

from faker import Faker

random = Random()
fake = Faker()


class Users(Table):
    user_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    user_type = Column(Enum("person", "organization"))
    bio = Column(String)
    homepage = Column(String, nullable=True)
    profile_picture = Column(String, nullable=True)

    @staticmethod
    def populate(session, seed=None) -> None:
        for _ in range(100):
            is_company = random.choice([True, False])
            if is_company:
                company_name = fake.company()
                company_domain = f"{company_name.replace(' ', '_')}.{random.choice(['com', 'org', 'net'])}"
                company_email = f"contact@{company_domain}"
                company_url = f"https://{company_domain}"
                user = Users(
                    username=company_name,
                    email=company_email,
                    password=fake.password(),
                    user_type="organization",
                    bio=fake.text(),
                    homepage=company_url,
                    profile_picture=fake.image_url(),
                )
            else:
                if random.random() < 0.5:
                    first_name = fake.first_name()
                    last_name = fake.last_name()
                    user_name = f"{first_name}.{last_name}"
                    user_email = f"{first_name}.{last_name}@{fake.free_email_domain()}"
                else:
                    user_name = fake.user_name()
                    user_email = fake.email()
                user = Users(
                    username=user_name,
                    email=user_email,
                    password=fake.password(),
                    user_type="person",
                    bio=fake.text(),
                    homepage=None,
                    profile_picture=fake.image_url(),
                )
            session.add(user)

    @staticmethod
    def to_er_diagram():
        g = ER()
        g.add_entity("User")
        g.add_attribute("User", "user_id", is_pk=True)
        g.add_attribute("User", "username")
        g.add_attribute("User", "email")
        g.add_attribute("User", "password")
        g.add_attribute("User", "bio")
        g.add_attribute("User", "profile_picture")
        g.add_entity("Person")
        g.add_entity("Organization")
        g.add_attribute("Organization", "homepage")
        g.add_is_a("User", ["Person", "Organization"], is_total=True, is_disjunct=True)
        return g


class Followers(Table):
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    follower_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)

    dependencies = {Users}

    @staticmethod
    def populate(session, seed=None) -> None:
        users = session.query(Users).all()
        for user in users:
            added_followers = set()
            for _ in range(random.randint(0, 90)):
                follower = random.choice(users)
                if follower.user_id in added_followers:
                    continue
                if follower.user_id == user.user_id:
                    continue
                added_followers.add(follower.user_id)
                session.add(
                    Followers(user_id=user.user_id, follower_id=follower.user_id)
                )

    @staticmethod
    def to_er_diagram():
        g = ER()
        g.add_relation(
            {"User": "n"},
            "follows",
            {"User": "m"},
        )
        return g


class Posts(Table):
    post_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    caption = Column(String)
    image = Column(String)

    dependencies = {Users}

    @staticmethod
    def populate(session, seed=None) -> None:
        users = session.query(Users).all()
        for _ in range(1000):
            user = random.choice(users)
            post = Posts(
                user_id=user.user_id,
                caption=fake.text(),
                image=fake.image_url(),
            )
            session.add(post)

    @staticmethod
    def to_er_diagram():
        g = ER()
        g.add_entity("Post", is_weak=True)
        g.add_attribute("Post", "post_id", is_pk=True, is_weak=True)
        g.add_attribute("Post", "caption")
        g.add_attribute("Post", "image")
        g.add_relation(
            {"User": "1"},
            "posts",
            {
                "Post": {
                    "cardinality": "m",
                    "is_weak": True,
                }
            },
        )
        return g


class Likes(Table):
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.post_id"), primary_key=True)

    dependencies = {Users, Posts}

    @staticmethod
    def populate(session, seed=None) -> None:
        users = session.query(Users).all()
        posts = session.query(Posts).all()
        for post in posts:
            added_users = set()
            for _ in range(random.randint(0, 100)):
                user = random.choice(users)
                if user.user_id in added_users:
                    continue
                added_users.add(user.user_id)
                like = Likes(
                    user_id=user.user_id,
                    post_id=post.post_id,
                )
                session.add(like)

    @staticmethod
    def to_er_diagram():
        g = ER()
        g.add_relation(
            {"User": "n"},
            "likes",
            {"Post": "m"},
        )
        return g


class Hashtags(Table):
    hashtag_id = Column(Integer, primary_key=True)
    hashtag_name = Column(String)

    @staticmethod
    def populate(session, seed=None) -> None:
        for _ in range(1000):
            hashtag = Hashtags(
                hashtag_name=fake.word(),
            )
            session.add(hashtag)

    @staticmethod
    def to_er_diagram():
        g = ER()
        g.add_entity("Hashtag")
        g.add_attribute("Hashtag", "hashtag_id", is_pk=True)
        g.add_attribute("Hashtag", "hashtag_name")
        return g


class Post_Hashtags(Table):
    post_id = Column(Integer, ForeignKey("posts.post_id"), primary_key=True)
    hashtag_id = Column(Integer, ForeignKey("hashtags.hashtag_id"), primary_key=True)

    dependencies = {Posts, Hashtags}

    @staticmethod
    def populate(session, seed=None) -> None:
        posts = session.query(Posts).all()
        hashtags = session.query(Hashtags).all()
        for post in posts:
            added_hashtags = set()
            for _ in range(random.randint(0, 4)):
                hashtag = random.choice(hashtags)
                if hashtag.hashtag_id in added_hashtags:
                    continue
                added_hashtags.add(hashtag.hashtag_id)
                post_hashtag = Post_Hashtags(
                    post_id=post.post_id,
                    hashtag_id=hashtag.hashtag_id,
                )
                session.add(post_hashtag)

    @staticmethod
    def to_er_diagram():
        g = ER()
        g.add_relation(
            {"Post": "n"},
            "has_hashtag",
            {"Hashtag": "m"},
        )
        return g


class Comments(Table):
    comment_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    post_id = Column(Integer, ForeignKey("posts.post_id"))
    comment_text = Column(String)

    dependencies = {Users, Posts}

    @staticmethod
    def populate(session, seed=None) -> None:
        users = session.query(Users).all()
        posts = session.query(Posts).all()
        for post in posts:
            for _ in range(random.randint(0, 10)):
                user = random.choice(users)
                comment = Comments(
                    user_id=user.user_id,
                    post_id=post.post_id,
                    comment_text=fake.text(),
                )
                session.add(comment)

    @staticmethod
    def to_er_diagram():
        g = ER()
        g.add_entity("Comment", is_weak=True)
        g.add_attribute("Comment", "comment_id", is_pk=True, is_weak=True)
        g.add_attribute("Comment", "comment_text")
        g.add_relation(
            {"Post": "n"},
            "has_comment",
            {"Comment": {"cardinality": "m", "is_weak": True}},
        )
        g.add_relation(
            {"Comment": "n"},
            "reply_to",
            {"Comment": {"cardinality": "1", "is_weak": True}},
        )
        g.add_relation({"User": "1"}, "comments", {"Comment": "m"})
        return g


class Comment_Hashtags(Table):
    comment_id = Column(Integer, ForeignKey("comments.comment_id"), primary_key=True)
    hashtag_id = Column(Integer, ForeignKey("hashtags.hashtag_id"), primary_key=True)

    dependencies = {Comments, Hashtags}

    @staticmethod
    def populate(session, seed=None) -> None:
        hashtags = session.query(Hashtags).all()
        for comment in session.query(Comments).all():
            added_hashtags = set()
            for _ in range(random.randint(0, 2)):
                hashtag = random.choice(hashtags)
                if hashtag.hashtag_id in added_hashtags:
                    continue
                added_hashtags.add(hashtag.hashtag_id)
                comment_hashtag = Comment_Hashtags(
                    comment_id=comment.comment_id,
                    hashtag_id=hashtag.hashtag_id,
                )
                session.add(comment_hashtag)

    @staticmethod
    def to_er_diagram():
        g = ER()
        g.add_relation({"Comment": "n"}, "has_hashtag", {"Hashtag": "m"})
        return g


import sqlite3
import subprocess


def test_social_media():
    tables = set(
        [
            Users,
            Followers,
            Posts,
            Likes,
            Hashtags,
            Post_Hashtags,
            Comments,
            Comment_Hashtags,
        ]
    )

    factory = SchemaFactory(tables)
    factory.populate()

    schema = factory.to_sql()
    # load into sqlite
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.executescript(schema)
    conn.commit()
    for table in tables:
        tablename = table.__tablename__
        # select all from table, check that not empty
        cursor.execute(f"SELECT * FROM {tablename}")
        assert len(cursor.fetchall()) > 0
    conn.close()

    graph = factory.to_er_diagram()

    graphviz_is_installed = False
    try:
        subprocess.check_output(["dot", "-V"])
        graphviz_is_installed = True
    except subprocess.CalledProcessError:
        graphviz_is_installed = False
    except FileNotFoundError:
        graphviz_is_installed = False

    if graphviz_is_installed:
        digraph = graph.draw()
        digraph.render("social_media", format="png", view=False, cleanup=True)


import pytest


def test_dependency_not_present():
    tables = set(
        [
            Followers,
        ]
    )
    with pytest.raises(DependencyNotPresentError):
        _ = SchemaFactory(tables)
