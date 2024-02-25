---
title: Pyside6可视化界面制作
date: '2024-02-21'
summary: 正在学习中···持续更新
tags:
  - 笔记
share: false
---

## 界面设计

① 在Qt Designer完成界面设计后，命名为main_window.ui并保存至项目所在文件夹

② 将main_window.ui进行编译：右键选择Compile Qt UI File，会生成main_window_ui.py文件

## 代码部分

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

**以设计YOLOv5的图形界面为例(图片检测+视频检测)**

```python
import cv2
import sys
import torch

from PySide6.QtWidgets import QMainWindow, QApplication, QFileDialog
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import QTimer

from main_window_ui import Ui_MainWindow


def convert2QImage(img):
    height, width, channel = img.shape
    return QImage(img, width, height, width * channel, QImage.Format_RGB888)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.model = torch.hub.load("./", "custom", path="runs/train/exp/weights/best.pt", source="local")
        self.timer = QTimer()
        self.timer.setInterval(1)
        self.video = None
        self.bind_slots()

    def image_pred(self, file_path):
        results = self.model(file_path)
        image = results.render()[0]
        return convert2QImage(image)

    def open_image(self):
        print("点击了检测图片！")
        self.timer.stop()
        file_path = QFileDialog.getOpenFileName(self, dir="./dataset/images/train", filter="*.jpg;*.png;*.jpeg")
        if file_path[0]:
            file_path = file_path[0]
            qimage = self.image_pred(file_path)
            self.input.setPixmap(QPixmap(file_path))
            self.output.setPixmap(QPixmap.fromImage(qimage))

    def video_pred(self):
        ret, frame = self.video.read()
        if not ret:
            self.timer.stop()
        else:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.input.setPixmap(QPixmap.fromImage(convert2QImage(frame)))
            results = self.model(frame)
            image = results.render()[0]
            self.output.setPixmap(QPixmap.fromImage(convert2QImage(image)))

    def open_video(self):
        print("点击了检测视频！")
        file_path = QFileDialog.getOpenFileName(self, dir="./dataset", filter="*.mp4")
        if file_path[0]:
            file_path = file_path[0]
            self.video = cv2.VideoCapture(file_path)
            self.timer.start()
                
    def bind_slots(self):
        self.detect_img.clicked.connect(self.open_image)
        self.detect_video.clicked.connect(self.open_video)
        self.timer.timeout.connect(self.video_pred)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    
    app.exec()
```

