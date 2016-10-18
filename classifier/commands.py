from flask_script import Command, Option

from models import db, User


class CreateUser(Command):
    """Create a user"""

    option_list = [
        Option("--username", dest="username", help="the user's username",
               required=True),
        Option("--password", dest="password", help="the user's password",
               required=True)
    ]

    def run(self, username, password):
        User.create(username, password)

        db.session.commit()


class ChangeUserPassword(Command):
    """Change a user's password"""

    option_list = [
        Option("--username", dest="username", help="the user's username",
               required=True),
        Option("--password", dest="password", help="the user's password",
               required=True)
    ]

    def run(self, username, password):
        user = User.get_by_username(username)

        if user is None:
            print("Unknown user '%s'" % username)
            return

        user.change_password(password)

        db.session.commit()


class DeleteUser(Command):
    """delete a user"""

    option_list = [
        Option("--username", dest="username", help="the user's username",
               required=True)
    ]

    def run(self, username):
        user = User.get_by_username(username)

        if user is None:
            print("Unknown user '%s'" % username)
            return

        user.delete()

        db.session.commit()
