from os import path, getcwd

from flask_script import Manager

from classifier.application import create_app


def main():
    settings_file = path.join(getcwd(), "settings.py")

    app = create_app(settings_file)

    manager = Manager(app)

    manager.run()
