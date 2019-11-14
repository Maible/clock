from appdirs import user_data_dir
import json
import os

app_name = "MaibleClock"
app_authors = "Emin Mastizada, Nurdogan Karaman"

directory = user_data_dir(app_name, app_authors)
config_file = os.path.join(directory, "config.json")


class Settings(object):
    """Basic settings models that converts json file to a Python object properties.

    Params:
    :clock str: analog, digital
    """
    def __init__(self):
        if not os.path.exists(directory):
            os.mkdir(directory)
        if not os.path.exists(config_file):
            # Create the configuration file
            config = {
                "clock": "analog"
            }
            with open(config_file, 'w') as f:
                json.dump(config, f)
        with open(config_file, 'r') as f:
            params = json.load(f)
        for key in params:
            setattr(self, key, params[key])
        # specific settings
        self.app_name = app_name
        self.app_authors = app_authors
        self.app_dir = os.path.dirname(os.path.realpath(__file__))
        self.images_dir = os.path.join(self.app_dir, "images")


settings = Settings()

__all__ = [settings]
