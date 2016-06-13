# -*- coding: utf-8 -*-

import asyncio
import sys
from PyQt5.QtWidgets import QApplication
from quamash import QEventLoop
from Application import App
from plugins.local_oo.OO import OO


if __name__ == '__main__':

    q_app = QApplication(sys.argv)
    q_app.setQuitOnLastWindowClosed(True)
    q_app.setApplicationName('神奇的播放器啊')

    app_event_loop = QEventLoop(q_app)
    asyncio.set_event_loop(app_event_loop)
    app = App()
    app.show()
    oo = OO(app)

    app_event_loop.run_forever()
    sys.exit(0)