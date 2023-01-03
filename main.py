import sys

import sqlite3
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QPushButton, QMdiSubWindow
from UI import Ui_MainWindow
from book import Book
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy
from PyQt5.QtWidgets import QInputDialog


class Library(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connection = sqlite3.connect("library.db")
        self.search_mode = "author"
        self.book_list = {}
        self.initUI()

    def initUI(self):
        self.cmb_search_mode.currentTextChanged.connect(self.set_search_mode)
        self.btn_search.clicked.connect(self.search_books)

    def search_books(self):
        try:
            self.clear_layout()
            self.book_list.clear()
            if self.lineEdit_query.text():
                self.set_books_to_table()
                self.btns_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        except Exception as ex:
            print(ex)

    def set_books_to_table(self):
        cur = self.connection.cursor()
        query = self.lineEdit_query.text()
        res = cur.execute(f"""SELECT name, author, image, year, genre FROM books
        WHERE {self.search_mode} LIKE '%{query}%'""").fetchall()
        for elem in res:
            btn = QPushButton(elem[0])
            btn.clicked.connect(self.open_book)
            self.book_list[elem[0]] = {'name': elem[0], 'author': elem[1],
                                       'image': elem[2], 'year': elem[3], 'genre': elem[4]}
            self.btns_layout.addWidget(btn)

    def clear_layout(self):
        widgets = [self.btns_layout.itemAt(i) for i in range(self.btns_layout.count())]
        for elem in widgets:
            if elem.widget():
                self.btns_layout.removeWidget(elem.widget())
            else:
                self.btns_layout.removeItem(elem)

    def set_search_mode(self):
        mode = self.cmb_search_mode.currentText()
        if mode == "Автор":
            self.search_mode = "author"
        elif mode == "Название":
            self.search_mode = "name"

    def open_book(self):
        try:
            name = self.sender().text()
            data = [elem for elem in self.book_list[name].values()]
            self.window = Book(data[0], data[1], data[2], data[3], data[4])
            self.window.show()
        except Exception as ex:
            print(ex)

    def closeEvent(self, event):
        self.connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Library()
    ex.show()
    sys.exit(app.exec())
