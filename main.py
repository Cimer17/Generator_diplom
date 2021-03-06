from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os
from PyQt5 import QtCore, QtGui, QtWidgets

from fpdf import FPDF

sheet_id = "12af7tn0YCg0C7l8dZAzBMy-4mPtXc4vxSo8YUekz4As"

class Ui_mainWindow(QtWidgets.QMainWindow):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(300, 400)
        mainWindow.setMinimumSize(QtCore.QSize(300, 400))
        mainWindow.setMaximumSize(QtCore.QSize(300, 400))
        self.setFixedSize(self.size())
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(50, 40, 201, 41))
        self.comboBox.setObjectName("comboBox")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(70, 290, 151, 61))
        self.QCheckBox = QtWidgets.QCheckBox(mainWindow)
        self.QCheckBox.setGeometry(QtCore.QRect(40, 150, 300, 41))
        self.checkpdf = QtWidgets.QCheckBox(mainWindow)
        self.checkpdf.setGeometry(QtCore.QRect(40, 200, 300, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.text_status = QtWidgets.QLabel(self.centralwidget)
        self.text_status.setGeometry(QtCore.QRect(110, 370, 171, 20))
        self.text_status.setObjectName("text_status")
        mainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Генератор дипломов"))
        self.pushButton.setText(_translate("mainWindow", "Создать"))
        self.text_status.setText(_translate("mainWindow", "Жду задания!"))
        self.QCheckBox.setText(_translate("mainWindow", "Использовать локальное хранилище"))
        self.checkpdf.setText(_translate("mainWindow", "Создать pdf файл с дипломами"))

        list1 = [
            self.tr('VR'),
            self.tr('MR'),
            self.tr('PP'),
            self.tr('PR'),
            self.tr('KG'),
            self.tr('SA'),
        ]
        self.comboBox.addItems(list1)
        self.pushButton.clicked.connect(self.create_img)
        self.comboBox.activated.connect(self.clear_text)

        self.QCheckBox.stateChanged.connect(self.checked)
        self.status = False
        self.status_pdf = False


        self.checkpdf.stateChanged.connect(self.checked_pdf)


    def checked_pdf(self):
        self.status_pdf = self.checkpdf.isChecked()


    def checked(self):
        self.status = self.QCheckBox.isChecked()


    def clear_text(self):
        self.text_status.setText("Жду задания...")



    def create_img(self):
        imagelist = []
        pdf = FPDF(orientation = 'L', unit = 'mm', format='A4')
        if self.status == False:
            napravlenie = self.comboBox.currentText()
            url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={napravlenie}"
            df = pd.read_csv(url)
            font = ImageFont.truetype("arial.ttf", 70, encoding='utf-8')
            for index, j in df.iterrows():
                img = Image.open(f'tmp/{napravlenie}.jpg')
                draw = ImageDraw.Draw(img)
                len_fio = len(j["name"])
                if 17 < len_fio < 23:
                    draw.text(xy=(470, 530), text='{}'.format(j['name']), fill=(0, 0, 0), font=font)
                elif 28 > len_fio >= 26:
                    draw.text(xy=(380, 530), text='{}'.format(j['name']), fill=(0, 0, 0), font=font)
                elif len_fio <= 16:
                    draw.text(xy=(550, 530), text='{}'.format(j['name']), fill=(0, 0, 0), font=font)
                elif 30 > len_fio >= 28:
                    draw.text(xy=(350, 530), text='{}'.format(j['name']), fill=(0, 0, 0), font=font)
                elif len_fio >= 30:
                    draw.text(xy=(330, 530), text='{}'.format(j['name']), fill=(0, 0, 0), font=font)
                else:
                    draw.text(xy=(410, 530), text='{}'.format(j['name']), fill=(0, 0, 0), font=font)
                img.save('pictures/{}.jpg'.format(j['name']))
                name_img = (j['name'])
                imagelist.append(f"pictures/{name_img}.jpg")
            if self.status_pdf == True:
                for image in imagelist:
                    pdf.add_page()
                    pdf.image(image, 0, 0, 297, 210)
                pdf.output(f"pdf/{napravlenie}.pdf", "F")
            self.text_status.setText("Готово!")

        elif self.status == True:
            napravlenie = self.comboBox.currentText()
            df = pd.read_csv(f"data/{napravlenie}_DB.csv")
            font = ImageFont.truetype("arial.ttf", 70, encoding='utf-8')
            for index, j in df.iterrows():
                img = Image.open(f'tmp/{napravlenie}.jpg')
                draw = ImageDraw.Draw(img)
                len_fio = len(j["name"])
                if 17 < len_fio < 23:
                    draw.text(xy=(470, 530), text='{}'.format(j['name']), fill=(0, 0, 0), font=font)
                elif 28 > len_fio >= 26:
                    draw.text(xy=(380, 530), text='{}'.format(j['name']), fill=(0, 0, 0), font=font)
                elif len_fio <= 16:
                    draw.text(xy=(550, 530), text='{}'.format(j['name']), fill=(0, 0, 0), font=font)
                elif 30 > len_fio >= 28:
                    draw.text(xy=(350, 530), text='{}'.format(j['name']), fill=(0, 0, 0), font=font)
                elif len_fio >= 30:
                    draw.text(xy=(330, 530), text='{}'.format(j['name']), fill=(0, 0, 0), font=font)
                else:
                    draw.text(xy=(410, 530), text='{}'.format(j['name']), fill=(0, 0, 0), font=font)
                img.save('pictures/{}.jpg'.format(j['name']))
                name_img = (j['name'])
                imagelist.append(f"pictures/{name_img}.jpg")
            if self.status_pdf == True:
                for image in imagelist:
                    pdf.add_page()
                    pdf.image(image, 0, 0, 297, 210)
                pdf.output(f"pdf/{napravlenie}.pdf", "F")
            self.text_status.setText("Готово!")


if __name__ == "__main__":
    import sys
    check = os.path.exists('pictures')
    if check == False:
        os.mkdir("pictures")
    check = os.path.exists('pdf')
    if check == False:
        os.mkdir("pdf")
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())

