# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QWidget, QFrame, QPushButton, QLabel, QSlider,
                             QScrollArea, QDialog, QLineEdit, QCheckBox,
                             QTableWidget, QComboBox)
from PyQt5.QtCore import QObject


class MButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_theme_style(self):
        pass


class MCheckBox(QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_theme_style(self):
        pass


class MComboBox(QComboBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_theme_style(self):
        pass


class MDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_theme_style(self):
        pass


class MFrame(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_theme_style(self):
        self.setStyleSheet('background: transparent;')


class MLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_theme_style(self):
        pass


class MQLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_theme_style(self):
        pass


class MObject(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_theme_style(self):
        pass


class MSlider(QSlider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_theme_style(self):
        pass


class MScrollArea(QScrollArea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_theme_style(self):
        pass


class MTableWidget(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_theme_style(self):
        pass


class MWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_theme_style(self):
        pass