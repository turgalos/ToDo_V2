from PyQt6.QtCore import Qt, QSize, QLine
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, \
    QDialog, QVBoxLayout, QComboBox, QToolBar, QHeaderView
from PyQt6.QtGui import QAction, QIcon, QColor, QFont
import sys
import sqlite3


class DatabaseConnection:
    def __init__(self, database_file="todos.db"):
        self.database_file = database_file

    def connect(self):
        connection = sqlite3.connect(self.database_file)
        return connection


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To-do App V2")
        self.setMinimumSize(550, 500)

        add_todo_action = QAction(QIcon("icons/add.png"), "Add Todo", self)
        add_todo_action.triggered.connect(self.insert)

        edit_action = QAction(QIcon("icons/edit.png"), "Edit", self)
        edit_action.triggered.connect(self.edit)

        delete_action = QAction(QIcon("icons/delete.png"), "Delete", self)
        delete_action.triggered.connect(self.delete)

        move_up_action = QAction(QIcon("icons/up_arrow.png"), "Move up", self)
        move_up_action.triggered.connect(self.move_up)

        move_down_action = QAction(QIcon("icons/down_arrow.png"), "Move down", self)
        move_down_action.triggered.connect(self.move_down)

        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_action.triggered.connect(self.search)

        toolbar = QToolBar()
        toolbar.setMovable(True)
        toolbar.setFixedHeight(150)
        self.addToolBar(toolbar)
        toolbar.setIconSize(QSize(60, 60))
        toolbar.addAction(add_todo_action)
        toolbar.addAction(edit_action)
        toolbar.addAction(delete_action)
        toolbar.addAction(move_up_action)
        toolbar.addAction(move_down_action)
        toolbar.addAction(search_action)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(("Id", "Description", "Label", "Priority", "Note"))
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # self.table.setColumnWidth(0, 20)
        # self.table.setColumnWidth(1, 200)
        self.table.verticalHeader().setVisible(False)
        header_font = QFont()
        header_font.setPointSize(10)
        header_font.setBold(True)
        text_font = QFont()
        text_font.setPointSize(10)
        self.table.horizontalHeader().setFont(header_font)
        self.table.setFont(text_font)
        self.setCentralWidget(self.table)

        #TODO:
        #dodać tabelkę obok todosów na ściągę calli?

    def load_table(self):
        connection = DatabaseConnection().connect()
        result = connection.execute("SELECT * FROM todos")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                if column_number == 0:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if column_number == 3:
                    if data.lower() == 'low':
                        item.setBackground(QColor(144, 238, 144))
                    elif data.lower() == 'medium':
                        item.setBackground(QColor(255, 255, 102))
                    elif data.lower() == 'high':
                        item.setBackground(QColor(255, 99, 71))
                self.table.setItem(row_number, column_number, item)
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def move_up(self):
        pass

    def move_down(self):
        pass

    def delete(self):
        index = todo_app.table.currentRow()
        id_to_del = todo_app.table.item(index, 0).text()
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM todos WHERE id = ?",(id_to_del, ))
        connection.commit()
        cursor.close()
        connection.close()
        todo_app.load_table()



class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Todo")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.description = QLineEdit()
        self.description.setPlaceholderText("Description")
        layout.addWidget(self.description)

        self.label = QComboBox()
        labels = ["", "Work", "Private", "Other"]
        self.label.addItems(labels)
        layout.addWidget(self.label)

        self.priority = QComboBox()
        priorties = ["", "Low", "Medium", "High"]
        self.priority.addItems(priorties)
        layout.addWidget(self.priority)

        self.note = QLineEdit()
        self.note.setPlaceholderText("Note")
        layout.addWidget(self.note)

        button = QPushButton("Submit")
        button.clicked.connect(self.add_todo)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_todo(self):
        description = self.description.text().capitalize()
        label = self.label.itemText(self.label.currentIndex())
        priority = self.priority.itemText(self.priority.currentIndex())
        note = self.note.text().capitalize()

        # print(description, label, priority, note)
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO todos (description, label, priority, note) VALUES (?, ?, ?, ?)",
                       (description, label, priority, note))
        connection.commit()
        cursor.close()
        connection.close()
        todo_app.load_table()

        self.close()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Todo")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Description:"))
        self.description = QLineEdit()
        layout.addWidget(self.description)

        layout.addWidget(QLabel("Label:"))
        self.label = QComboBox()
        labels = ["", "Work", "Private", "Other"]
        self.label.addItems(labels)
        layout.addWidget(self.label)

        layout.addWidget(QLabel("Priority:"))
        self.priority = QComboBox()
        priorties = ["", "Low", "Medium", "High"]
        self.priority.addItems(priorties)
        layout.addWidget(self.priority)

        layout.addWidget(QLabel("Note:"))
        self.note = QLineEdit()
        layout.addWidget(self.note)
        layout.addWidget(QLabel())

        button = QPushButton("Search")
        button.clicked.connect(self.search)
        layout.addWidget(button)

        self.setLayout(layout)

    def search(self):

        description = self.description.text().capitalize()
        label = self.label.itemText(self.label.currentIndex())
        priority = self.priority.itemText(self.priority.currentIndex())
        note = self.note.text().capitalize()

        conditions = []
        values = []

        if description:
            conditions.append("description LIKE ?")
            values.append(f"%{description}%")
        if label:
            conditions.append("label = ?")
            values.append(label)
        if priority:
            conditions.append("priority = ?")
            values.append(priority)
        if note:
            conditions.append("note LIKE ?")
            values.append(f"%{note}%")

        if conditions:
            query = "SELECT * FROM todos WHERE " + " AND ".join(conditions)
            # print(f"query: {query}")

            connection = DatabaseConnection().connect()
            cursor = connection.cursor()
            result = cursor.execute(query, tuple(values))
            todo_app.table.clearSelection()

            for row in result:
                items = todo_app.table.findItems(str(row[0]), Qt.MatchFlag.MatchFixedString)
                for item in items:
                    todo_app.table.item(item.row(), 1).setSelected(True)

            cursor.close()
            connection.close()

        self.close()

class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Todo")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        self.index = todo_app.table.currentRow()
        self.id = todo_app.table.item(self.index, 0).text()

        layout = QVBoxLayout()

        self.description = QLineEdit()
        self.description.setText(todo_app.table.item(self.index, 1).text())
        layout.addWidget(self.description)

        self.label = QComboBox()
        labels = ["", "Work", "Private", "Other"]
        self.label.addItems(labels)
        current_label = todo_app.table.item(self.index, 2).text()
        self.label.setCurrentText(current_label)
        layout.addWidget(self.label)

        self.priority = QComboBox()
        priorties = ["", "Low", "Medium", "High"]
        self.priority.addItems(priorties)
        current_priority = todo_app.table.item(self.index, 3).text()
        self.priority.setCurrentText(current_priority)
        layout.addWidget(self.priority)

        self.note = QLineEdit()
        self.note.setText(todo_app.table.item(self.index, 4).text())
        layout.addWidget(self.note)

        button = QPushButton("Submit")
        button.clicked.connect(self.edit_todo)
        layout.addWidget(button)

        self.setLayout(layout)

    def edit_todo(self):
        description = self.description.text().capitalize()
        label = self.label.itemText(self.label.currentIndex())
        priority = self.priority.itemText(self.priority.currentIndex())
        note = self.note.text().capitalize()

        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("UPDATE todos SET description = ?, label = ?, priority  = ?, note=? WHERE id = ?",
                       (description, label, priority, note, self.id))
        connection.commit()
        cursor.close()
        connection.close()
        todo_app.load_table()

        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    todo_app = MainWindow()
    todo_app.show()
    todo_app.load_table()
    sys.exit(app.exec())
