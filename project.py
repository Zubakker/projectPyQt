import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDial, QWidget, QMainWindow, QTableWidgetItem, QLabel
from PyQt5.QtGui import QPixmap
from PIL import Image
from random import randrange
from math import *


class MyWidget(QMainWindow):
    # Здесь мы создаем основные элементы
    def __init__(self):
        super().__init__()
        self.opened = 0
        self.nums = 0
        self.upes = 0
        self.mash = 0.05
        self.chords = [None, None]
        uic.loadUi("poject.ui", self)
        # Открываем картинку и загружаем ее
        self.im = Image.new("RGB", [400, 400])
        self.img = self.im.load()
        self.im.save("___image.jpg")
        self.label_3.setPixmap(QPixmap("___image.jpg"))
        self.pushButton_2.clicked.connect(self.help)
        self.hep = QLabel(self)
        self.pushButton.clicked.connect(self.run)
        # Запускаем функцию, которая отрисовывает график
        self.run()
        self.setGeometry(472, 93, 420, 520)

    def run(self):
        try:
            # Получаем масштаб функцию и закрашиваем все поле белым
            k = self.mash
            fun = lambda x: eval(self.lineEdit.text())
            for i in range(400):
                for j in range(400):
                    self.img[i, j] = (255, 255, 255)
            # Отрисовываем координатные оси
            for i in range(400):
                try:
                    self.img[i, 200 - self.upes] = (0, 0, 0)
                except:
                    pass
                try:
                    self.img[200 - self.nums, i] = (0, 0, 0)
                except:
                    pass
            # Передвигаем точку (0; 0)
            try:
                self.label_2.move(210 - self.nums, 240 - self.upes)
            except:
                pass
            # Ставим точки по серединам сторон поля
            self.label_5.setText("(" + str(round(-200 * k - k * self.nums, 2)) + "; " + str(round(-k * self.upes, 2)) + ")")
            self.label_6.setText("(" + str(round(200 * k - k * self.nums, 2)) + "; " + str(round(-k * self.upes, 2)) + ")")
            self.label_3.setText("(" + str(round(-k * self.nums, 2)) + "; " + str(round(200 * k - k * self.upes, 2)) + ")")
            self.label_4.setText("(" + str(round(-k * self.nums, 2)) + "; " + str(round(-200 * k - k * self.upes, 2)) + ")")
            # lax -- это прошлый икс он нам пригодится для расчетов
            lax = (self.nums - 200) * k
            for i in range(400):
                # Проходимся по каждому пикселю картинки, подбираем к нему х
                x = (i - 200 + self.nums) * k
                try:
                    # Отрисовываем х
                    self.img[i, int(200 - fun(x) / k - self.upes)] = (255, 0, 0)
                except:
                    pass
                try:
                    # Это нужно для соединения точек, если х + 0.01 или х + 0.5 или х + 0.99 выходит за границы поля, то мы их не соединяем х и х + 1
                    if abs(fun(x) - fun(lax)) > k:
                        if (-200 < fun(lax + 0.01 * k) / k - self.upes < 200 and
                                -200 < fun(lax + 0.5 * k) / k - self.upes < 200 and
                                -200 < fun(lax + 0.99 * k) / k - self.upes < 200):
                            for j in range(min([int(fun(x) / k), int(fun(lax) / k)]), max([int(fun(x) / k), int(fun(lax) / k)])):
                                self.img[i, 200 - j - int(self.upes)] = (255, 0, 0)
                except:
                    pass
                try:
                    # Если х или lax выходит за границы поля, то мы все равно пытаемся их соединить
                    if not -200 < fun(lax) / k < 200 and -200 < fun(x) / k < 200:
                        for j in range(min([int(fun(lax) / k), int(fun(x) / k)]), max([int(fun(lax) / k), int(fun(x) / k)])):
                            try:
                                self.img[i, 200 - j - int(self.upes)] = (255, 0, 0)
                            except:
                                pass
                    if not -200 < fun(x) / k < 200 and -200 < fun(lax) / k < 200:
                        for j in range(min([int(fun(lax) / k), int(fun(x) / k)]), max([int(fun(lax) / k), int(fun(x) / k)])):
                            try:
                                self.img[i, 199 - j - int(self.upes)] = (255, 0, 0)
                            except:
                                pass
                except:
                    pass
                lax = x
            # Сохраняем картинку и загружаем ее в label
            self.im.save("___image.jpg")
            self.label.setPixmap(QPixmap("___image.jpg"))
        except Exception as ex:
            print(ex)

    def mousePressEvent(self, event):
        # При нажатии кнопки мыши мы ловим координаты, для того чтобы следить за ее перемещениями
        self.chords = event.x(), event.y()

    def mouseMoveEvent(self, event):
        # Следим за перемещениями мыши для того, чтобы передвигать поле
        self.nums += self.chords[0] - event.x()
        self.upes += self.chords[1] - event.y()
        self.chords = event.x(), event.y()
        self.run()

    def wheelEvent(self, event):
        # Ловим перемещение колесика для того, чтобы изменять масштаб
        if event.angleDelta().y() > 0:
            self.mash /= 1.1
        else:
            self.mash *= 1.1
        self.run()

    def help(self):
        self.opened = 1 - self.opened
        # Изменяем размеры окна и создаем там текстовое поле с подсказкой
        if self.opened:
            self.setGeometry(472, 93, 700, 520)
            try:
                self.hep.move(430, 10)
                self.hep.resize(250, 500)
                self.hep.setText("""ИНСТРУКЦИЯ ПО ИСПОЛЬЗОВАНИЮ
ПРОГРАММЫ

1) В ПОЛЕ НУЖНО ВСТАВЛЯТЬ ФУНКЦИИ В
ФОРМАТЕ, КОТОРЫЙ ПОНИМАЕТ ПИТОН 
(* для умножения, ** для возведения 
в степень, / для деления)

2) ПОЛЕ ПРИНИМАЕТ НЕКОТОРЫЕ МАТЕМ 
ФУНКЦИИ (sin() cos() tan() и т. д.)
И КОНСТАНТЫ (pi, e)

3) ПОЛЕ НЕ ПРИНИМАЕТ ФУНКЦИИ ВИДА 
у = ...
ПОЖАЛУЙСТА, ВСТАВЛЯЙТЕ ФУНКЦИИ,
СОДЕРЖАЩИЕ только х
(x**2, sin(x), pi*x + 2)

4) ВЫ МОЖЕТЕ ДВИГАТЬ ПОЛЕ МЫШЬЮ И 
МАСШТАБИРОВАТЬ КОЛЕСИКОМ
""")
            except Exception as ex:
                print(ex)
        else:
            self.setGeometry(472, 93, 420, 520)


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
