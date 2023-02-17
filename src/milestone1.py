import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt6 import uic, QtCore
#from PyQt6 import QIcon, QPixmap
import psycopg2

qtCreatorFile = "milestone1App.ui" #file name
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class milestone1(QMainWindow):
    def __init__(self):
        super(milestone1, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.load_state_list()
        self.ui.stateList.currentTextChanged.connect(self.state_changed)
        self.ui.cityList.itemSelectionChanged.connect(self.city_changed)
        self.ui.bname.textChanged.connect(self.get_business_names)
        self.ui.businesses.itemSelectionChanged.connect(self.display_business_city)

    def execute_query(self, sql_str):
        try:
            #conn = psycopg2.connect("dbname='milestone1db' user='postgres' host='localhost' password='mustafa'")
            conn = psycopg2.connect("dbname='milestone1db' user='postgres' host='localhost'")
        except:
            print("Unable to connect to the database!")
            return []
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit() #we will wait until the query execution is completed
        result = cur.fetchall()
        conn.close()
        return result

    def load_state_list(self):
        self.ui.stateList.clear()
        sql_str = "SELECT distinct state FROM business ORDER BY state;"
        try:
            result = self.execute_query(sql_str)
            for row in result:
                self.ui.stateList.addItem(row[0])
        except Exception as e:
            print("Query failed!")
            print(e)
            return
        self.ui.stateList.setCurrentIndex(-1)
        self.ui.stateList.clearEditText()

    def state_changed(self):
        if not self.ui.stateList.currentIndex() >= 0: #ensure we have a valid index
            return
        state = self.ui.stateList.currentText()
        sql_str = "SELECT distinct city FROM business WHERE state = '" + state + "' ORDER BY city;"
        result = self.execute_query(sql_str)
        try:
            self.ui.cityList.clear()
            for row in result:
                self.ui.cityList.addItem(row[0])
        except:
            print("Query failed while updating cities!")
        for i in reversed(range(self.ui.businessTable.rowCount())):
            self.ui.businessTable.removeRow(i)
        sql_str = "SELECT name, city, state FROM business WHERE state = '" + state + "' ORDER BY name"
        try:
            result = self.execute_query(sql_str)
            style = "::section {""background-color: #f3f3f3; }"
            self.ui.businessTable.horizontalHeader().setStyleSheet(style)
            self.ui.businessTable.setColumnCount(len(result[0]))
            self.ui.businessTable.setRowCount(len(result))
            self.ui.businessTable.setHorizontalHeaderLabels(["Business Name", "City", "State"])
            self.ui.businessTable.resizeColumnsToContents()
            self.ui.businessTable.setColumnWidth(0, 300)
            self.ui.businessTable.setColumnWidth(1, 100)
            self.ui.businessTable.setColumnWidth(2, 50)
            for index, row in enumerate(result):
                for col_count in range(len(result[0])):
                    self.ui.businessTable.setItem(index, col_count, QTableWidgetItem(row[col_count]))
        except:
            print("Query failed while updating businesses!")

    def city_changed(self):
        if self.ui.stateList.currentIndex() < 0 or len(self.ui.cityList.selectedItems()) <= 0:
            return
        state = self.ui.stateList.currentText()
        city = self.ui.cityList.selectedItems()[0].text()
        sql_str = "SELECT name, city, state FROM business WHERE state = '" + state + "' AND city = '" + city + "' ORDER BY name;"
        for i in reversed(range(self.ui.businessTable.rowCount())):
            self.ui.businessTable.removeRow(i)
        try:
            result = self.execute_query(sql_str)
            style = "::section {""background-color: #f3f3f3; }"
            self.ui.businessTable.horizontalHeader().setStyleSheet(style)
            self.ui.businessTable.setColumnCount(len(result[0]))
            self.ui.businessTable.setRowCount(len(result))
            self.ui.businessTable.setHorizontalHeaderLabels(["Business Name", "City", "State"])
            self.ui.businessTable.resizeColumnsToContents()
            self.ui.businessTable.setColumnWidth(0, 300)
            self.ui.businessTable.setColumnWidth(1, 100)
            self.ui.businessTable.setColumnWidth(2, 50)
            for index, row in enumerate(result):
                for col_count in range(len(result[0])):
                    self.ui.businessTable.setItem(index, col_count, QTableWidgetItem(row[col_count]))
        except:
            print("Query failed while updating businesses!")

    def get_business_names(self):
        self.ui.businesses.clear()
        business_name = self.ui.bname.text()
        sql_str = "SELECT name FROM business WHERE name LIKE '%" + business_name + "%' ORDER BY name;"
        print(sql_str)
        try:
            result = self.execute_query(sql_str)
            for row in result:
                self.ui.businesses.addItem(row[0])
        except:
            print("Query failed while updating business names!")

    def display_business_city(self):
        if len(self.ui.businesses.selectedItems()) < 1:
            self.ui.bcity.setText("")
            return
        business_name = self.ui.businesses.selectedItems()[0].text()
        sql_str = "SELECT city FROM business WHERE name = '" + business_name + "';"
        try:
            result = self.execute_query(sql_str)
            self.ui.bcity.setText(result[0][0])
        except:
            print("Query failed while updating business cities!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = milestone1()
    window.show()
    sys.exit(app.exec())

