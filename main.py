from docxtpl import DocxTemplate
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QTextEdit, QVBoxLayout, QFileDialog
import datetime
import sys
import os

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.file_path = ''
        self.initUI()
    
    def initUI(self):
        
        lbl = QLabel('Введите ФИО, каждое с новой строки:', self)
        self.textEdit = QTextEdit(self)

        btn = QPushButton('Выбрать шаблон', self)
        btn.setToolTip('Формат doc, docx')
        btn.clicked.connect(self.on_click)
        btnenter = QPushButton('Создать', self)
        btnenter.clicked.connect(self.create)
        
        vbox = QVBoxLayout()
        vbox.addWidget(lbl)
        vbox.addWidget(self.textEdit)
        vbox.addWidget(btn)
        vbox.addWidget(btnenter)

        self.setLayout(vbox)
        
        self.setWindowTitle('Генератор дипломов')
        self.setGeometry(300, 300, 300, 250)
        self.show()

    def on_click(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileName(self, "Выбрать файл", "", "Microsoft Word (*.docx *.doc)", options=options)
        if file:
            self.file_path = file

    def create(self):
        if not os.path.exists('img'):
            os.makedirs('img')
        now = datetime.datetime.now()
        names = self.textEdit.toPlainText().splitlines()
        doc = DocxTemplate(self.file_path)
        for name in names:
            doc.render({'ФИО': name, 'ГОД' : f'{now.year} г.'})
            doc.save(f"img/{name}.docx")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())