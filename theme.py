# -*- coding: utf-8 -*-

import os
import configparser

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QColor

from setting import THEME_FILE_PATH


class ThemeManager(object):

    def __init__(self, app):
        super().__init__()
        self._app = app

        self.current_theme = None
        self._themes = list()    # config file name (involve file path)

    def get_theme_file(self):
        """ get theme file under the 'my_program/themes/' file
        """
        for directory in THEME_FILE_PATH:
            files = os.listdir(directory)
            for file in files:
                f_name, f_ext = file.split('.')
                if f_ext == 'cs':
                    self._themes.append(directory+file)

    def list(self):
        """ show themes under the THEME_FILE_PATH
        :return:  themes name list
        """
        if not self._themes:
            self.get_theme_file()
        return self._themes

    def get_theme(self, theme_name):
        """ implement for future
        :param theme_name: theme unique name
        :return:
        """
        pass

    def set_theme(self, theme_name):
        """ set current theme
        :param theme_name: theme unique name
        """
        self.current_theme = Theme(theme_name)

    def choose_theme(self, theme_name):
        """ set current theme and change theme in app
        :param theme_name: theme unique name
        :return:
        """
        def recursive_update(widget):
            """ recursive update widget
            :param widget: app
            """
            if hasattr(widget, 'set_theme_style'):  # test this attribute is in or not
                widget.set_theme_style()
            for child in widget.children():
                if isinstance(child, QWidget):  # test child is QWidget or not
                    recursive_update(child)  # recursive update child

        self.set_theme(theme_name)
        recursive_update(self._app)


class Theme(object):

    def __init__(self, config_file=None):
        """ init theme's config from Themes's file named from config_name
        :param config_file: themes's file name
        """
        self._config = configparser.ConfigParser()
        self.file_path = config_file

        self.read(config_file)

    def read(self, config_path):
        """ read config file from config_path
        :param config_path: file involve file path so that we can read it
        directly
        :return: if we get config success return True
         else return False
        """
        if config_path is not None:
            config = self._config.read(config_path)
            if config:
                return True
        return False

    @property
    def name(self):
        tmp_name = self.file_path.split('/')
        tmp_name = tmp_name[len(tmp_name) - 1].split('.')[0]
        return tmp_name

    # In this area we defined many decorators,
    # in order to get themes's color configs as an attribute immediately
    @property
    def background_light(self):
        color_section = self._config['Background']
        return self._parse_color_str(color_section['color'])

    @property
    def background(self):
        color_section = self._config['BackgroundIntense']
        return self._parse_color_str(color_section['color'])

    @property
    def foreground_light(self):
        color_section = self._config['Foreground']
        return self._parse_color_str(color_section['color'])

    @property
    def foreground(self):
        color_section = self._config['ForegroundIntense']
        return self._parse_color_str(color_section['color'])

    @property
    def color0_light(self):
        color_section = self._config['Color0']
        return self._parse_color_str(color_section['color'])

    @property
    def color0(self):
        color_section = self._config['Color0Intense']
        return self._parse_color_str(color_section['color'])

    @property
    def color1_light(self):
        color_section = self._config['Color1']
        return self._parse_color_str(color_section['color'])

    @property
    def color1(self):
        color_section = self._config['Color1Intense']
        return self._parse_color_str(color_section['color'])

    @property
    def color2_light(self):
        color_section = self._config['Color2']
        return self._parse_color_str(color_section['color'])

    @property
    def color2(self):
        color_section = self._config['Color2Intense']
        return self._parse_color_str(color_section['color'])

    @property
    def color3_light(self):
        color_section = self._config['Color3']
        return self._parse_color_str(color_section['color'])

    @property
    def color3(self):
        color_section = self._config['Color3Intense']
        return self._parse_color_str(color_section['color'])

    @property
    def color4_light(self):
        color_section = self._config['Color4']
        return self._parse_color_str(color_section['color'])

    @property
    def color4(self):
        color_section = self._config['Color4Intense']
        return self._parse_color_str(color_section['color'])

    @property
    def color5_light(self):
        color_section = self._config['Color5']
        return self._parse_color_str(color_section['color'])

    @property
    def color5(self):
        color_section = self._config['Color5Intense']
        return self._parse_color_str(color_section['color'])

    @property
    def color6_light(self):
        color_section = self._config['Color6']
        return self._parse_color_str(color_section['color'])

    @property
    def color6(self):
        color_section = self._config['Color6Intense']
        return self._parse_color_str(color_section['color'])

    @property
    def color7_light(self):
        color_section = self._config['Color7']
        return self._parse_color_str(color_section['color'])

    @property
    def color7(self):
        color_section = self._config['Color7Intense']
        return self._parse_color_str(color_section['color'])

    def _parse_color_str(self, color_str):
        """ change str to int and set it as a color config
        :param color_str: str from config file
        :return: QColor object
        """
        rgb = [int(x) for x in color_str.split(',')]
        return QColor(rgb[0], rgb[1], rgb[2])