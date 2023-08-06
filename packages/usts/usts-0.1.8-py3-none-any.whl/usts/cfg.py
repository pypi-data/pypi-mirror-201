import configparser
import importlib
import sys
import os

class Config:

    def __init__(self):
        self.config = configparser.ConfigParser()
        
        self.home_dir           = os.path.expanduser('~')
        self.config_dir_path    = self.home_dir + "/.config/usts/"
        self.config_path        = self.config_dir_path + "config.py"

        sys.path.append(self.config_dir_path)

        self.make_config_dir()
        self.load_config()

    def is_config_exists(self):
        return os.path.exists(self.config_path)

    def make_config_dir(self):
        os.makedirs(self.config_dir_path, exist_ok=True)

    def load_config(self):
        if not self.is_config_exists(): return None, None
        pfile = importlib.import_module("config")
        return pfile


