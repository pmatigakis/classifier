from os import path

from flask_script import Manager

from classifier.commands import CreateUser, DeleteUser, ChangeUserPassword
from classifier.application import create_app


def main():
    settings_file = path.join(path.dirname(path.abspath(__name__)), "settings.py")

    app = create_app(settings_file)

    manager = Manager(app)

    users_manager = Manager(help="user management", description="user management")
    users_manager.add_command("create", CreateUser())
    users_manager.add_command("delete", DeleteUser())
    users_manager.add_command("change_password", ChangeUserPassword())

    manager.add_command("users", users_manager)

    manager.run()


if __name__ == "__main__":
    main()
