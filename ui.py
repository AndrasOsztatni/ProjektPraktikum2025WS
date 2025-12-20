import sys
from PyQt6.QtWidgets import (QApplication, QTableWidget, QTableWidgetItem, 
                             QCheckBox, QWidget, QHBoxLayout, QVBoxLayout, QHeaderView)
from PyQt6.QtCore import Qt


class AnalysisUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analysis Configuration")
        self.resize(1000, 300)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        # 1. Define Column Headers
        # Section 1: Opening Widths (1 col)
        # Section 2: Inputs (4 cols)
        # Section 3: Results (5 cols)
        # Section 4: Global Check (1 col)
        self.headers = ["Opening Widths", "in90", "in70", "in60", "in45", 
                        "FFT", "SFFT", "p(t)", "Powspec", "f(seg)", "Select All"]
        
        self.table = QTableWidget(4, len(self.headers))
        self.table.setHorizontalHeaderLabels(self.headers)
        
        # Opening Width Data
        widths = ["Width A", "Width B", "Width C", "Width D"]

        for row in range(4):
            # Section 1: Set Text
            self.table.setItem(row, 0, QTableWidgetItem(widths[row]))

            # Sections 2 & 3: Add Checkboxes (Columns 1 to 9)
            for col in range(1, 10):
                self.add_checkbox(row, col)

            # Section 4: The "Select All" Checkbox (Column 10)
            self.add_checkbox(row, 10, is_master=True)

        # UI Polish: Stretch columns to fit window
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(self.table)
        self.setLayout(layout)

    def add_checkbox(self, row, col, is_master=False):
        """Helper to center a checkbox in a table cell"""
        chk_widget = QWidget()
        chk_layout = QHBoxLayout(chk_widget)
        checkbox = QCheckBox()
        chk_layout.addWidget(checkbox)
        chk_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chk_layout.setContentsMargins(0, 0, 0, 0)
        
        if is_master:
            # Connect the 'Select All' logic
            checkbox.stateChanged.connect(lambda state: self.toggle_row(row, state))
            
        self.table.setCellWidget(row, col, chk_widget)

    def toggle_row(self, row, state):
        """Checks/Unchecks every box in the row based on the last column"""
        is_checked = (state == Qt.CheckState.Checked.value)
        for col in range(1, 10):
            # Access the checkbox inside the cell widget
            widget = self.table.cellWidget(row, col)
            checkbox = widget.findChild(QCheckBox)
            checkbox.setChecked(is_checked)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AnalysisUI()
    window.show()
    sys.exit(app.exec())

