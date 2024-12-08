import sys
import sqlite3

from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QWidget


class Window(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)

    def update_result(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        result = cur.execute("SELECT * FROM films WHERE id=?",
                             (item_id := self.spinBox.text(),)).fetchall()
        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        # Если запись не нашлась, то не будем ничего делать
        if not result:
            self.statusBar().showMessage('Ничего не нашлось')
            return
        else:
            self.statusBar().showMessage(f"Нашлась запись с id = {item_id}")
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}
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