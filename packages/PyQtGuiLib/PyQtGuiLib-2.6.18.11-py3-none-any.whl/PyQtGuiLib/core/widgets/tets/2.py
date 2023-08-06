
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    qt,
    Qt,
    QPoint,
    QPainter,
    QColor,
    QRect,
    QBrush,
    QPen,
    QPaintEvent,
    QGraphicsDropShadowEffect,
    QVBoxLayout,
    QSize,
    QMainWindow,
    QMenuBar,
    QAction,
    QMenu,
    QIcon,
    QPixmap,
    qt,
)
'''
https://icons8.com/
https://www.flaticon.com/
https://www.iconfinder.com/
'''


from PyQt5 import QtCore

class Test(QWidget):

    def __init__(self,*args,**kwargs):
        super(Test, self).__init__(*args,**kwargs)

        self.spring = 6

        self.vboy = QVBoxLayout(self)
        self.vboy.setContentsMargins(self.spring,self.spring,self.spring,self.spring)
        self.vboy.setSpacing(0)

        self.core = QMainWindow()
        self.core.resize(self.size())
        self.vboy.addWidget(self.core)

        # 菜单栏
        self.menubar = QMenuBar()

        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 23))
        self.core.setMenuBar(self.menubar)

        self.g = QGraphicsDropShadowEffect()
        self.g.setOffset(0, 0)
        self.g.setBlurRadius(self.spring * 2)
        self.g.setColor(QColor(0, 0, 0))

        self.core.setGraphicsEffect(self.g)

        # -----------------------------------

        self.resize(QSize(800,800))
        # self.resize(100,100)

        self.setAttribute(qt.WA_TranslucentBackground,True)
        self.setWindowFlags(qt.FramelessWindowHint | qt.Widget)


        self.core.setStyleSheet('''
        background-color: rgb(255, 170, 0);
        border-radius:8px;
        ''')

        self.about = QMenu()
        icon = QIcon(r"D:\code\PyQtGuiLib\PyQtGuiLib\tests\temp_image\python1.png")
        new_size = QSize(100, 100)
        icon = icon.pixmap(new_size).scaled(new_size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

        self.about.setIcon(QIcon(icon))
        # self.core.setWindowIcon(QIcon(r"D:\code\PyQtGuiLib\PyQtGuiLib\tests\temp_image\python1.svg"))
        self.about.setEnabled(False)
        self.about.setStyleSheet('''
        background-color: rgb(255, 170, 0);
        border-radius:10px;
        ''')
        self.test = QAction("222")
        self.about.addAction(self.test)
        self.menubar.addMenu(self.about)


    def parent(self) -> 'QObject':
        return self.core.parent()

    def size(self) -> QSize:
        # print("父类",super().size())
        return self.core.size()

    def resize(self,*args) -> None:
        if len(args) == 2:
            size = QSize(args[0],args[1])
        elif len(args) == 1 and isinstance(args[0],QSize):
            size = args[0]
        else:
            raise TypeError("size error!")

        self.core.resize(size)
        size.setWidth(size.width()+self.spring*2)
        size.setHeight(size.height()+self.spring*2)
        super().resize(size)

    def width(self) -> int:
        return self.width()

    def height(self) -> int:
        return self.height()

    def geometry(self) ->QRect:
        return self.core.geometry()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test()

    win.resize(500,500)
    print(win.size())
    print(win.geometry())
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())