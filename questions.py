# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QDir
from mainwindow import * # 主窗口

if __name__ == '__main__':
    # Many browsers for security reason disable the loading of local files, but you can enable that capability with:
    sys.argv.append("--disable-web-security")
    app = QApplication(sys.argv)
    iconpath = QDir.currentPath() + r'/icon.ico'
    app.setWindowIcon(QIcon(iconpath))
    main_ui = MainWindow()
    main_ui.show()
    sys.exit(app.exec_())
