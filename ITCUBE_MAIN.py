from docx.shared import Cm
from PIL import Image, ImageDraw, ImageFont
from PyQt5 import QtCore, QtGui, QtWidgets
from qt_material import apply_stylesheet
from PyQt5.QtGui import QIcon
import pandas as pd
import os
import datetime
import docx
import threading


class Ui_mainWindow(QtWidgets.QMainWindow):
    
    def setupUi(self, mainWindow):
        
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(300, 400)
        mainWindow.setMinimumSize(QtCore.QSize(300, 285))
        mainWindow.setMaximumSize(QtCore.QSize(300, 285))
        self.setFixedSize(self.size())
        icon_path = "icon.ico"
        app_icon = QIcon(icon_path)
        mainWindow.setWindowIcon(app_icon)
        
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(50, 20, 201, 41))
        self.comboBox.setObjectName("comboBox")
        
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(75, 180, 151, 61))

        self.FILEButton = QtWidgets.QPushButton(self.centralwidget)
        self.FILEButton.setGeometry(QtCore.QRect(60, 80, 180, 30))
        
        self.checkpdf = QtWidgets.QCheckBox(mainWindow)
        self.checkpdf.setGeometry(QtCore.QRect(40, 130, 300, 41))
        
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        
        self.text_status = QtWidgets.QLabel(self.centralwidget)
        self.text_status.setGeometry(QtCore.QRect(110, 260, 171, 20))
        self.text_status.setObjectName("text_status")
        
        mainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Генератор дипломов"))
        self.pushButton.setText(_translate("mainWindow", "Создать"))
        self.FILEButton.setText(_translate('mainWindow', 'Открыть файл с ФИО'))
        self.text_status.setText(_translate("mainWindow", "Жду задания!"))
        self.checkpdf.setText(_translate("mainWindow", "Создать docx файл с дипломами"))
        list1 = [
            self.tr('VR'),
            self.tr('MR'),
            self.tr('PP'),
            self.tr('PR'),
            self.tr('KG'),
            self.tr('SA'),
        ]
        self.comboBox.addItems(list1)
        self.FILEButton.clicked.connect(self.open_file_children)
        self.pushButton.clicked.connect(self.start_create_img)
        self.comboBox.activated.connect(self.clear_text)
        self.status_doc = False
        self.checkpdf.stateChanged.connect(self.checked_pdf)

    def checked_pdf(self):
        self.status_doc = self.checkpdf.isChecked()

    def open_file_children(self):
        napravlenie = self.comboBox.currentText()
        file = f'data\\{napravlenie}_DB.CSV'
        os.startfile(file, 'edit') 

    def clear_text(self):
        self.text_status.setText("Жду задания...")

    def drawing(self, img, name_img):
        draw = ImageDraw.Draw(img)
        font_FIO = ImageFont.truetype("arial.ttf", 70, encoding='utf-8')
        font_year = ImageFont.truetype("arial.ttf", 45, encoding='utf-8')
        name_size = len(name_img)
        now_year = f'{datetime.datetime.now().year} год'
        if name_size > 25:
            draw.text(xy=(500, 610), text=f'{name_img}', fill=(0, 0, 0), font=font_FIO)
        elif name_size > 16:
            draw.text(xy=(649 - name_size * 4 , 610), text=f'{name_img}', fill=(0, 0, 0), font=font_FIO)
        else:
            draw.text(xy=(649, 610), text=f'{name_img}', fill=(0, 0, 0), font=font_FIO)
        draw.text(xy=(890, 1300), text=f'{now_year}', fill=(0, 0, 0), font=font_year)


    def save_doc(self, imagelist, napravlenie):
        doc = docx.Document()
        sections = doc.sections
        for section in sections:
            section.top_margin = Cm(0)
            section.bottom_margin = Cm(0)
            section.left_margin = Cm(1)
            section.right_margin = Cm(0)
        for image in imagelist:
            doc.add_picture(image, width=Cm(19.6), height=Cm(13.6))
        if not os.path.exists('doc'):
            os.makedirs('doc')
        doc.save(f'doc/{napravlenie}.docx')
    
    def create_img(self):
        imagelist = []
        napravlenie = self.comboBox.currentText()
        df = pd.read_csv(f"data/{napravlenie}_DB.csv")
        pathc = os.path.abspath('pictures')
        url_patch = f'{pathc}\{napravlenie}'.replace('\\', '/')
        if os.path.exists(url_patch):
            pass 
        else:
            os.mkdir(url_patch)
        for index, j in df.iterrows():
            img = Image.open(f'tmp/{napravlenie}.png')
            name_img = (j['name'])
            self.drawing(img, name_img)
            patch_name = f'pictures/{napravlenie}/{name_img}.png'.replace(' ', '_')
            img.save(patch_name) 
            imagelist.append(patch_name)
        if self.status_doc == True: 
            self.save_doc(imagelist, napravlenie)
        self.text_status.setText("Готово!")
    

    def start_create_img(self):
        thread = threading.Thread(target=self.create_img)
        thread.start()

def main():
    import sys
    if os.path.exists('pictures') == False:
        os.mkdir("pictures")
    if os.path.exists('doc') == False:
        os.mkdir("doc")
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    apply_stylesheet(app, theme='dark_blue.xml')
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()