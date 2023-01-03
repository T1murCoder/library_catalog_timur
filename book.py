import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from book_ui import Ui_MainWindow
from PyQt5.QtGui import QPixmap


class Book(QMainWindow, Ui_MainWindow):
    def __init__(self, name, author, image, year, genre):
        super().__init__()
        self.setupUi(self)
        self.data = {'name': name, 'author': author, 'image': image, 'year': year, 'genre': genre}
        self.initUI()

    def initUI(self):
        try:
            self.lbl_name.setText(self.data['name'])
            self.lbl_author.setText(self.data['author'])
            if self.data['image']:
                pixmap = QPixmap(f'images/{self.data["image"]}')
                self.lbl_image.setPixmap(pixmap)
            else:
                pixmap = QPixmap('images/book.png')
                self.lbl_image.setPixmap(pixmap)
            self.lbl_year.setText(str(self.data['year']))
            self.lbl_genre.setText(self.data['genre'])
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Book('name', 'author', None, 'year', 'genre')
    window.show()
    sys.exit(app.exec())
