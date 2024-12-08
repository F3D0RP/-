import sys
import sqlite3
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox, QWidget
from PyQt6 import QtWidgets, uic
from addEditCoffeeForm import Ui_Form
from main import Ui_MainWindow


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton_2.clicked.connect(self.exit)
        self.ui.tableWidget.itemChanged.connect(self.item_changed)
        self.ui.pushButton_3.clicked.connect(self.save_results)
        self.ui.pushButton.clicked.connect(self.adding_record)
        self.modified = {}
        self.update_result()

    def item_changed(self, item):
        self.modified[self.titles[item.column()]] = item.text()

    def adding_record(self):
        con = sqlite3.connect('release/data/coffee.sqlite')
        cur = con.cursor()

        name = self.ui.lineEdit.text()
        roast_degree = self.ui.lineEdit_2.text()
        grind_type = self.ui.lineEdit_3.text()
        flavor_description = self.ui.lineEdit_4.text()
        price = float(self.ui.lineEdit_5.text())
        package_volume = self.ui.lineEdit_6.text()
        cur.execute(
            'INSERT INTO coffee (name, roast_degree, grind_type, flavor_description, price, package_volume) VALUES (?,?,?,?,?,?)',
            (name, roast_degree, grind_type, flavor_description, price, package_volume)
        )
        con.commit()
        con.close()
        self.update_result()

    def save_results(self):
        if self.modified:
            con = sqlite3.connect('release/data/coffee.sqlite')
            cur = con.cursor()
            que = "UPDATE coffee SET "
            que += ", ".join([f"{key}='{self.modified.get(key)}'" for key in self.modified.keys()])
            que += " WHERE id = ?"

            current_item = self.ui.tableWidget.currentItem()
            if current_item is None:
                QMessageBox.warning(self, "Ошибка", "Нет выбранной ячейки для обновления.")
                return

            row = current_item.row()
            record_id = self.ui.tableWidget.item(row, 0).text()

            cur.execute(que, (record_id,))
            con.commit()
            self.modified.clear()
            QMessageBox.information(self, "Успех", "Запись успешно обновлена!")
            con.close()

    def exit(self):
        self.close()
        self.a = CoffeeApp()
        self.a.show()

    def update_result(self):
        con = sqlite3.connect('release/data/coffee.sqlite')
        cur = con.cursor()
        result = cur.execute("SELECT * FROM coffee").fetchall()
        self.ui.tableWidget.setRowCount(len(result))
        if not result:
            self.statusBar().showMessage('Ничего не нашлось')
            return

        self.ui.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.ui.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}
        con.close()


class CoffeeApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.load_coffee_data()
        self.a = Window()
        self.ui.pushButton.clicked.connect(self.open)

    def open(self):
        self.close()
        self.a.show()

    def load_coffee_data(self):
        conn = sqlite3.connect('release/data/coffee.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coffee")
        coffee_records = cursor.fetchall()

        for record in coffee_records:
            self.ui.listWidget.addItem(f"ID: {record[0]}, Название: {record[1]}, "
                                       f"Степень обжарки: {record[2]}, "
                                       f"Тип: {record[3]}, Вкус: {record[4]}, "
                                       f"Цена: {record[5]}, Объем: {record[6]}")

        conn.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())
