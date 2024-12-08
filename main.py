import sys
import sqlite3
from PyQt6 import QtWidgets, uic

class CoffeeApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.load_coffee_data()

    def load_coffee_data(self):
        conn = sqlite3.connect('coffee.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coffee")
        coffee_records = cursor.fetchall()

        for record in coffee_records:
            self.listWidget.addItem(f"ID: {record[0]}, Название: {record[1]}, "
                                    f"Степень обжарки: {record[2]}, "
                                    f"Тип: {record[3]}, Вкус: {record[4]}, "
                                    f"Цена: {record[5]}, Объем: {record[6]}")

        conn.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())