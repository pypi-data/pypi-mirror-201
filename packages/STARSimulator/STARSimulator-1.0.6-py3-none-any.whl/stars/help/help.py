from gui.widgetfactory import create_box_layout, create_cell, create_table, create_widget
from constants import HELP_TABS, HELP_TITLE
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
import csv
import os
from typing import List
import sys

# must be ran in sbumips directory (this is bc PYTHONPATH is weird in terminal)
sys.path.append(os.getcwd())


def create_tab(rows: List[str], header: List[str]) -> QTableWidget:
    '''Returns a table with csv row values inserted.'''
    table = create_table(len(rows), len(rows[0]), header, stretch_last=True)
    for row, values in enumerate(rows):
        for i, text in enumerate(values):
            table.setItem(row, i, create_cell(
                (text.strip().replace('\\n', '\n'))))
    if not header:
        table.horizontalHeader().setVisible(False)
    table.resizeColumnsToContents()
    table.resizeRowsToContents()

    return table


def create_search(table: QTableWidget) -> QWidget:
    def search_function(text: str) -> None:
        for row in range(table.rowCount()):
            column = table.item(row, 0)
            table.setRowHidden(row, not column.text().startswith(text))
    text_entry = QLineEdit()
    text_entry.textChanged.connect(search_function)

    return create_widget(create_box_layout(direction=QBoxLayout.TopToBottom,
                                           sections=[text_entry, table]))


class HelpWindow(QMainWindow):

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle(HELP_TITLE)
        self.window = QTabWidget()
        self.window.setStyleSheet(app.style_sheet)
        for name, properties in HELP_TABS.items():
            with open(properties['filename']) as f:
                if properties['type'] == 'table':
                    rows = [row for row in csv.reader(f)]
                    table = create_tab(rows, properties.get('header', []))
                    self.window.addTab(create_search(table), name)
                elif properties['type'] == 'text':
                    text = QTextEdit()
                    text.setReadOnly(True)
                    text.setPlainText(f.read())
                    self.window.addTab(text, name)
                elif properties['type'] == 'markdown':
                    text = QTextEdit()
                    text.setReadOnly(True)
                    text.setMarkdown(f.read())
                    self.window.addTab(text, name)
        self.setCentralWidget(self.window)

        self.show()
        self.resize(1080, 480)
    
    def update_theme(self) -> None:
        self.window.setStyleSheet(self.app.style_sheet)

if __name__ == "__main__":
    app = QApplication()
    window = HelpWindow(app)
    app.exec_()
