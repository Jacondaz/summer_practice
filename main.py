import pandas as pd
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (QWidget, QComboBox, QApplication, QPushButton, QLabel, QFileDialog)
from PyQt6.QtGui import QPixmap


def to_csv():
    for item in names_of_dat:
        temp_df = new_file[new_file['Ячейка::алиас'] == item][::2]
        temp_df = temp_df[['Точка::штамп времени', 'Ячейка::значение']]
        temp_df.columns = ['Время', 'Значение']
        temp_df.to_csv(f'{item}.csv', sep=';', index=False)


def main():

    class Example(QWidget):
        temp = names_of_dat[0]
        temp1 = names_of_dat[0]
        x1 = list()
        y1 = list()
        titles = list()

        def __init__(self):
            super().__init__()
            self.pixmap = None
            self.label = None
            self.pixmap1 = None
            self.label1 = None
            self.ax = plt.figure()
            self.initUI()

        def initUI(self):
            # -------------- Комбинированные графики -----------------
            self.pixmap = QPixmap("1.png")
            self.label = QLabel(self)
            self.label.setPixmap(self.pixmap)
            self.label.move(400, 70)

            combo = QComboBox(self)
            combo.addItems(names_of_dat)
            combo.move(20, 70)
            combo.textActivated.connect(self.onChanged)

            button1 = QPushButton(self)
            button1.setText("Добавить")
            button1.move(20, 100)
            button1.clicked.connect(self.add_to_list)

            button2 = QPushButton(self)
            button2.setText("Убрать")
            button2.move(105, 100)
            button2.clicked.connect(self.remove_from_list)

            button_clf = QPushButton(self)
            button_clf.setText("Очистить график")
            button_clf.move(20, 130)
            button_clf.clicked.connect(self.clear)

            button_save = QPushButton(self)
            button_save.setText("Сохранить график")
            button_save.move(20, 160)
            button_save.clicked.connect(self.save)
            # ---------------- Одиночные графики -------------------
            self.pixmap1 = QPixmap("2.png")
            self.label1 = QLabel(self)
            self.label1.setPixmap(self.pixmap1)
            self.label1.move(400, 545)

            combo2 = QComboBox(self)
            combo2.addItems(names_of_dat)
            combo2.move(20, 600)
            combo2.textActivated.connect(self.onChanged1)

            button3 = QPushButton(self)
            button3.setText("Отобразить")
            button3.move(165, 600)
            button3.clicked.connect(self.showImage)

            button4 = QPushButton(self)
            button4.setText("Следующий")
            button4.move(132, 630)
            button4.clicked.connect(self.next)

            button5 = QPushButton(self)
            button5.setText("Предыдущий")
            button5.move(20, 630)
            button5.clicked.connect(self.prev)

            button_clf1 = QPushButton(self)
            button_clf1.setText("Очистить график")
            button_clf1.move(20, 660)
            button_clf1.clicked.connect(self.clear1)

            button_save1 = QPushButton(self)
            button_save1.setText("Сохранить график")
            button_save1.move(20, 690)
            button_save1.clicked.connect(self.save1)
            # -------------------------------------------------------
            self.setGeometry(500, 350, 1060, 1040)
            self.setWindowTitle('Анализ показателей донных датчиков')
            self.show()

        def add_to_list(self):
            if len(self.temp) != 0:
                temp_df = new_file[new_file['Ячейка::алиас'] == self.temp][::2]
                list_time_temp = [x.split(':') for x in temp_df['Точка::штамп времени'].tolist()]
                list_time = [float(x[1]) * 60 + float(x[2].replace(',', '.')) for x in list_time_temp]
                list_mean = [round(float(x.replace(',', '.')), 3) for x in temp_df['Ячейка::значение'].tolist()]
                for j in list_mean:
                    if j < 0:
                        tm = list_mean.index(j)
                        list_mean.remove(j)
                        list_time.pop(tm)
                for c in range(1, len(list_time)):
                    list_time[c] -= list_time[0]
                list_time[0] = 0
                if self.temp not in self.titles:
                    self.x1.append(list_time)
                    self.y1.append(list_mean)
                    self.titles.append(self.temp)
                    # print(self.titles)
                    self.draw()
                    self.reload_image()

        def remove_from_list(self):
            temp_df = new_file[new_file['Ячейка::алиас'] == self.temp][::2]
            list_time_temp = [x.split(':') for x in temp_df['Точка::штамп времени'].tolist()]
            list_time = [float(x[1]) * 60 + float(x[2].replace(',', '.')) for x in list_time_temp]
            list_mean = [round(float(x.replace(',', '.')), 3) for x in temp_df['Ячейка::значение'].tolist()]
            for j in list_mean:
                if j < 0:
                    tm = list_mean.index(j)
                    list_mean.remove(j)
                    list_time.pop(tm)
            for c in range(1, len(list_time)):
                list_time[c] -= list_time[0]
            list_time[0] = 0
            if list_time in self.x1:
                self.x1.remove(list_time)
                self.y1.remove(list_mean)
                self.titles.remove(self.temp)
                # print(self.titles)
                self.draw()
                self.reload_image()

        def draw(self):
            plt.clf()
            plt.xlabel("с")
            plt.ylabel("Па")
            plt.grid()
            for k in range(len(self.x1)):
                plt.plot(self.x1[k], self.y1[k])
            plt.legend(self.titles)
            if len(self.titles) == 0:
                plt.title("Комбинированный график")
            plt.savefig("1.png")
            self.reload_image()

        def showImage(self):
            temp_df = new_file[new_file['Ячейка::алиас'] == self.temp1][::2]
            list_time_temp = [x.split(':') for x in temp_df['Точка::штамп времени'].tolist()]
            list_time = [float(x[1]) * 60 + float(x[2].replace(',', '.')) for x in list_time_temp]
            list_mean = [round(float(x.replace(',', '.')), 3) for x in temp_df['Ячейка::значение'].tolist()]
            for j in list_mean:
                if j < 0:
                    tm = list_mean.index(j)
                    list_mean.remove(j)
                    list_time.pop(tm)
            for c in range(1, len(list_time)):
                list_time[c] -= list_time[0]
            list_time[0] = 0
            plt.clf()
            plt.xlabel("с")
            plt.ylabel("Па")
            plt.grid()
            plt.plot(list_time, list_mean)
            plt.title(self.temp1)
            plt.savefig("2.png")
            self.reload_image1()

        def next(self):
            if names_of_dat.index(self.temp1) < len(names_of_dat) - 1:
                temp_df = new_file[new_file['Ячейка::алиас'] == names_of_dat[names_of_dat.index(self.temp1) + 1]][::2]
                list_time_temp = [x.split(':') for x in temp_df['Точка::штамп времени'].tolist()]
                list_time = [float(x[1]) * 60 + float(x[2].replace(',', '.')) for x in list_time_temp]
                list_mean = [round(float(x.replace(',', '.')), 3) for x in temp_df['Ячейка::значение'].tolist()]
                for j in list_mean:
                    if j < 0:
                        tm = list_mean.index(j)
                        list_mean.remove(j)
                        list_time.pop(tm)
                for c in range(1, len(list_time)):
                    list_time[c] -= list_time[0]
                list_time[0] = 0
                plt.clf()
                plt.xlabel("с")
                plt.ylabel("Па")
                plt.grid()
                plt.plot(list_time, list_mean)
                plt.title(names_of_dat[names_of_dat.index(self.temp1) + 1])
                plt.savefig("2.png")
                self.reload_image1()
                self.temp1 = names_of_dat[names_of_dat.index(self.temp1) + 1]

        def prev(self):
            if names_of_dat.index(self.temp1) > 0:
                temp_df = new_file[new_file['Ячейка::алиас'] == names_of_dat[names_of_dat.index(self.temp1) - 1]][::2]
                list_time_temp = [x.split(':') for x in temp_df['Точка::штамп времени'].tolist()]
                list_time = [float(x[1]) * 60 + float(x[2].replace(',', '.')) for x in list_time_temp]
                list_mean = [round(float(x.replace(',', '.')), 3) for x in temp_df['Ячейка::значение'].tolist()]
                for j in list_mean:
                    if j < 0:
                        tm = list_mean.index(j)
                        list_mean.remove(j)
                        list_time.pop(tm)
                for c in range(1, len(list_time)):
                    list_time[c] -= list_time[0]
                list_time[0] = 0
                plt.clf()
                plt.xlabel("с")
                plt.ylabel("Па")
                plt.grid()
                plt.plot(list_time, list_mean)
                # print(self.temp1)
                plt.title(names_of_dat[names_of_dat.index(self.temp1) - 1])
                plt.savefig("2.png")
                self.reload_image1()
                self.temp1 = names_of_dat[names_of_dat.index(self.temp1) - 1]

        def save(self):
            plt.clf()
            plt.xlabel("с")
            plt.ylabel("Па")
            plt.grid()
            for k in range(len(self.x1)):
                plt.plot(self.x1[k], self.y1[k])
            plt.legend(self.titles)
            if len(self.titles) == 0:
                plt.title("Комбинированный график")
            plt.savefig(f'{self.titles}.png')

        def save1(self):
            temp_df = new_file[new_file['Ячейка::алиас'] == self.temp1][::2]
            list_time_temp = [x.split(':') for x in temp_df['Точка::штамп времени'].tolist()]
            list_time = [float(x[1]) * 60 + float(x[2].replace(',', '.')) for x in list_time_temp]
            list_mean = [round(float(x.replace(',', '.')), 3) for x in temp_df['Ячейка::значение'].tolist()]
            for j in list_mean:
                if j < 0:
                    tm = list_mean.index(j)
                    list_mean.remove(j)
                    list_time.pop(tm)
            for c in range(1, len(list_time)):
                list_time[c] -= list_time[0]
            list_time[0] = 0
            plt.clf()
            plt.xlabel("с")
            plt.ylabel("Па")
            plt.grid()
            plt.plot(list_time, list_mean)
            plt.title(self.temp1)
            plt.savefig(f'{self.temp1}.png')

        def clear(self):
            self.x1.clear()
            self.y1.clear()
            self.titles.clear()
            self.draw()

        def clear1(self):
            plt.clf()
            plt.xlabel("с")
            plt.ylabel("Па")
            plt.grid()
            plt.plot([], [])
            plt.title("Одиночный график")
            plt.savefig("2.png")
            self.reload_image1()

        def onChanged(self, text):
            self.temp = text
            # print(self.temp)

        def onChanged1(self, text):
            self.temp1 = text
            # print(self.temp1)

        def reload_image1(self):
            self.pixmap1 = QPixmap("2.png")
            self.label1.setPixmap(self.pixmap1)

        def reload_image(self):
            self.pixmap = QPixmap("1.png")
            self.label.setPixmap(self.pixmap)

    ex = Example()
    app.exec()


if __name__ == '__main__':
    app = QApplication([])
    path = QFileDialog.getOpenFileName()[0]
    file = pd.read_csv(path, delimiter=';')
    new_file = file[file['Устройство::сер.№'] == 'Вычисляемые выражения']
    new_file = new_file[['Точка::штамп времени', 'Ячейка::алиас', 'Ячейка::значение']]
    names_of_dat = new_file['Ячейка::алиас'].unique().tolist()
    for i in range(len(new_file)):
        temp = new_file.iloc[i]['Точка::штамп времени'].split()
        new_file.iloc[i]['Точка::штамп времени'] = temp[1]
    plt.plot([], [])
    plt.xlabel("с")
    plt.ylabel("Па")
    plt.grid()
    plt.title("Комбинированный график")
    plt.savefig("1.png")
    plt.title("Одиночный график")
    plt.savefig("2.png")
    to_csv()
    main()
