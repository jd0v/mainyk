import logging_make
import helper
import json_manager


class Container:
    def __init__(self, website=None, json_filename=None):
        self.website = website
        self.log = logging_make.Log(self).log
        self.helper = helper.Helper(self)
        self.json_filename = json_filename
        self.json = json_manager.JsonManager(self, self.json_filename)
