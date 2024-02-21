---
title: Pyside6可视化界面制作
date: '2024-02-21'
summary: 正在学习中···持续更新
tags:
  - 笔记
share: false
---

## 准备工作

①在Qt Designer完成界面设计后，命名为main_window.ui并保存至项目所在文件夹

②将main_window.ui进行编译：右键选择Compile Qt UI File，会生成main_window_ui.py文件

**建议保存一个base内容，方便后续直接修改使用**

```python
# base_ui.py内容
import cv2
import sys
import torch

from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap, QImage

from main_window_ui import Ui_MainWindow

def convert2QImage(img):
    height,width,channel = img.shape
    return QImage(img, width, height, width * channel, QImage.Format_RGB888)

class MainWindow(QMainWindow, Ui_MainWindow):  #类 继承
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
```

以设计YOLOv5的图形界面为例

```python
import cv2
import sys
import torch

from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap, QImage

from main_window_ui import Ui_MainWindow

def convert2QImage(img):
    height,width,channel = img.shape
    return QImage(img, width, height, width * channel, QImage.Format_RGB888)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.bind_slots()
        
    def open_image(self):
        pass
    def open_video(self):
        pass
    # 为按钮添加绑定事件
    def bind_slots(self):
        self.detect_img.click.connect(self.open_image)
        self.detect_video.click.connect(self.open_video)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
```

