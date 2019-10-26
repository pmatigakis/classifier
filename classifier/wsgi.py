from os import path, getcwd

from classifier.application import create_app


settings_file = path.join(getcwd(), "settings.py")
app = create_app(settings_file)
