# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt5.QtWidgets import (QMenu, QAction, QHeaderView, QVBoxLayout,
                             QAbstractItemView, QHBoxLayout)

from libs.widgets.base import (MLabel, MFrame, MQLineEdit, MButton,
                                            MDialog)
from libs.widgets.components import MusicTable, LPGroupItem
from model import SongModel

