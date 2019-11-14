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
                "clock": "analog",
                "calendar_url": None,
                "background_color": [100, 100, 100, 220],
                "hour_color": [150, 114, 114, 220],
                "minute_color": [64, 64, 64, 200],
                "second_color": [96, 96, 105, 200],
                "shadow_color": [255, 255, 255, 100],
                "helper_color": [211, 211, 211, 75],
                "text_color": [18, 18, 19, 255],
                "helper_text_color": [238, 238, 238, 200]
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

    def save(self):
        config = {
            "clock": self.clock,
            "calendar_url": self.calendar_url,
            "background_color": self.background_color,
            "hour_color": self.hour_color,
            "minute_color": self.minute_color,
            "second_color": self.second_color,
            "shadow_color": self.shadow_color,
            "helper_color": self.helper_color,
            "text_color": self.text_color,
            "helper_text_color": self.helper_text_color
        }
        with open(config_file, 'w') as f:
            json.dump(config, f)


settings = Settings()

__all__ = [settings]
