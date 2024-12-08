import sys
import sqlite3

from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QWidget


class Window(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.update_result()
        self.pushButton_2.clicked.connect(self.exit)
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.pushButton_3.clicked.connect(self.save_results)

    def item_changed(self, item):
        self.modified[self.titles[item.column()]] = item.text()

    def save_results(self):
        if self.modified:
            cur = self.con.cursor()
            que = "UPDATE coffee SET\n"
            que += ", ".join([f"{key}='{self.modified.get(key)}'" for key in self.modified.keys()])
            que += " WHERE id = ?"

            current_item = self.tableWidget.currentItem()
            if current_item is None:
                QMessageBox.warning(self, "Ошибка", "Нет выбранной ячейки для обновления.")
                return

            row = current_item.row()
            record_id = self.tableWidget.item(row, 0).text()

            cur.execute(que, (record_id,))
            self.con.commit()
            self.modified.clear()
            QMessageBox.information(self, "Успех", "Запись успешно обновлена!")

    def exit(self):
        self.close()
        self.a = CoffeeApp()
        self.a.show()

    def update_result(self):
        self.con = sqlite3.connect('coffee.sqlite')
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM coffee").fetchall()
        self.tableWidget.setRowCount(len(result))
        if not result:
            self.statusBar().showMessage('Ничего не нашлось')
            return

        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}


class CoffeeApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.load_coffee_data()
        self.a = Window()
        self.pushButton.clicked.connect(self.open)

    def open(self):
        self.close()
        self.a.show()

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
