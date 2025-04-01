import sys
import re
import warnings
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5 import uic

warnings.filterwarnings("ignore", category=DeprecationWarning)

class FormValidationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("form.ui", self)
        self.phone_input.setInputMask("+62 999 9999 9999;")
        self.save_button.clicked.connect(self.validate_and_save)
        self.clear_button.clicked.connect(self.clear_fields)
        self.setShortcut("Q", self.close)

    def setShortcut(self, key, function):
        from PyQt5.QtWidgets import QShortcut
        from PyQt5.QtGui import QKeySequence
        shortcut = QShortcut(QKeySequence(key), self)
        shortcut.activated.connect(function)

    def validate_and_save(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Validation Error", "Name cannot be empty!")
            return
        if any(char.isdigit() for char in name):
            QMessageBox.warning(self, "Validation Error", "Name must not contain numbers!")
            return

        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_pattern, self.email_input.text()):
            QMessageBox.warning(self, "Validation Error", "Please enter a valid email address!")
            return

        try:
            age = int(self.age_input.text())
            if age < 18 or age > 100:
                QMessageBox.warning(self, "Validation Error", "Age must be between 18 and 100!")
                return
        except ValueError:
            QMessageBox.warning(self, "Validation Error", "Age must be a numeric value!")
            return

        phone = self.phone_input.text().replace(" ", "")
        if len(phone) != 13 or not phone.startswith("+62"):
            QMessageBox.warning(self, "Validation Error", "Phone number must be a 13-digit number starting with +62 (e.g., +62 819 1810 2198)!")
            return

        if not self.address_input.toPlainText().strip():
            QMessageBox.warning(self, "Validation Error", "Address cannot be empty!")
            return

        if not self.gender_combo.currentText():
            QMessageBox.warning(self, "Validation Error", "Please select a gender!")
            return

        if not self.education_combo.currentText():
            QMessageBox.warning(self, "Validation Error", "Please select an education level!")
            return

        QMessageBox.information(self, "Success", "Form submitted successfully!")
        self.clear_fields()

    def clear_fields(self):
        self.name_input.clear()
        self.email_input.clear()
        self.age_input.clear()
        self.phone_input.clear()
        self.address_input.clear()
        self.gender_combo.setCurrentIndex(0)
        self.education_combo.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FormValidationApp()
    window.show()
    sys.exit(app.exec_())