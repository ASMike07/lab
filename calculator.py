import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QGridLayout


class CalculatorWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Настраиваю свойства окна
        self.setWindowTitle("Calculator")
        self.setGeometry(100, 100, 300, 200)

        # Создаю элементы пользовательского интерфейса
        self.expression_label = QLabel()
        self.result_label = QLabel()

        self.num1_edit = QLineEdit()
        self.num2_edit = QLineEdit()

        self.add_button = QPushButton("+")
        self.sub_button = QPushButton("-")
        self.mult_button = QPushButton("*")
        self.div_button = QPushButton("/")

        # Добавляю все элементы пользовательского интерфейса в макет
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.expression_label, 0, 0, 1, 4)
        grid_layout.addWidget(self.num1_edit, 1, 0)
        grid_layout.addWidget(self.num2_edit, 1, 1)
        grid_layout.addWidget(self.add_button, 2, 0)
        grid_layout.addWidget(self.sub_button, 2, 1)
        grid_layout.addWidget(self.mult_button, 3, 0)
        grid_layout.addWidget(self.div_button, 3, 1)
        grid_layout.addWidget(self.result_label, 4, 0, 1, 4)
        self.setLayout(grid_layout)

        # Подключаю сигналы кнопок к функциям слотов
        self.add_button.clicked.connect(self.add_numbers)
        self.sub_button.clicked.connect(self.sub_numbers)
        self.mult_button.clicked.connect(self.mult_numbers)
        self.div_button.clicked.connect(self.div_numbers)

    # (введённые значения из num1_edit и num2_edit)
    def add_numbers(self):
        num1 = self.get_input_number(self.num1_edit)
        num2 = self.get_input_number(self.num2_edit)
        self.compute_result(num1 + num2)

    def sub_numbers(self):
        num1 = self.get_input_number(self.num1_edit)
        num2 = self.get_input_number(self.num2_edit)
        self.compute_result(num1 - num2)

    def mult_numbers(self):
        num1 = self.get_input_number(self.num1_edit)
        num2 = self.get_input_number(self.num2_edit)
        self.compute_result(num1 * num2)

    def div_numbers(self):
        num1 = self.get_input_number(self.num1_edit)
        num2 = self.get_input_number(self.num2_edit)
        if num2 == 0.0:
            self.result_label.setText("Error: Cannot divide by zero.")
        else:
            self.compute_result(num1 / num2)

    def get_input_number(self, edit):
        try:
            return float(edit.text())
        except ValueError:
            self.result_label.setText("Error: Invalid input.")
            return None

    def compute_result(self, result):
        if result is None:
            return

        if abs(result) > (10 ** 10):
            self.result_label.setText("Error: Result is too large.")
            return

        self.result_label.setText(f"Result: {result}")


def main():
    app = QApplication(sys.argv)
    calculator = CalculatorWindow()
    calculator.show()
    sys.exit(app.exec_())

# Проаеряю запуск как скрипт, вызываю функцию
if __name__ == "__main__":
    main()