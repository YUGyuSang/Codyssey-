import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class Calculator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.current_input = '0'
        self.previous_input = ''
        self.operator = ''
        self.reset_next = False

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            return None
        return a / b

    def negative_positive(self):
        if self.current_input != '0':
            if self.current_input.startswith('-'):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
        return self.current_input

    def percent(self):
        value = float(self.current_input) / 100
        self.current_input = self.format_result(value)
        return self.current_input

    def input_number(self, num):
        if self.reset_next:
            self.current_input = num
            self.reset_next = False
        else:
            if self.current_input == '0' and num != '.':
                self.current_input = num
            else:
                self.current_input += num
        return self.current_input

    def input_dot(self):
        if self.reset_next:
            self.current_input = '0.'
            self.reset_next = False
        elif '.' not in self.current_input:
            self.current_input += '.'
        return self.current_input

    def set_operator(self, op):
        self.previous_input = self.current_input
        self.operator = op
        self.reset_next = True

    def equal(self):
        if not self.operator or not self.previous_input:
            return self.current_input

        a = float(self.previous_input)
        b = float(self.current_input)

        if self.operator == '+':
            result = self.add(a, b)
        elif self.operator == '-':
            result = self.subtract(a, b)
        elif self.operator == 'x':
            result = self.multiply(a, b)
        elif self.operator == '/':
            result = self.divide(a, b)
            if result is None:
                self.reset()
                return 'Error'
        else:
            return self.current_input

        self.current_input = self.format_result(result)
        self.operator = ''
        self.previous_input = ''
        self.reset_next = True
        return self.current_input

    def format_result(self, value):
        # 보너스 과제: 소수점 6자리 이하 반올림
        if value == int(value):
            return str(int(value))
        rounded = round(value, 6)
        return str(rounded).rstrip('0').rstrip('.')


class CalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.calc = Calculator()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Calculator')
        self.setFixedSize(360, 600)
        self.setStyleSheet('background-color: #1c1c1e;')

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 20, 10, 10)
        main_layout.setSpacing(0)

        self.display = QLabel('0')
        self.display.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.display.setFont(QFont('Arial', 64, QFont.Light))
        self.display.setStyleSheet('color: white; padding: 10px 20px 10px 10px;')
        self.display.setMinimumHeight(160)
        main_layout.addWidget(self.display)

        grid = QGridLayout()
        grid.setSpacing(10)

        buttons = [
            ('AC', 0, 0, 'func'), ('+/-', 0, 1, 'func'), ('%', 0, 2, 'func'), ('/', 0, 3, 'op'),
            ('7',  1, 0, 'num'),  ('8',   1, 1, 'num'),  ('9', 1, 2, 'num'),  ('x', 1, 3, 'op'),
            ('4',  2, 0, 'num'),  ('5',   2, 1, 'num'),  ('6', 2, 2, 'num'),  ('-', 2, 3, 'op'),
            ('1',  3, 0, 'num'),  ('2',   3, 1, 'num'),  ('3', 3, 2, 'num'),  ('+', 3, 3, 'op'),
            ('0',  4, 0, 'zero'), ('.',   4, 2, 'num'),  ('=', 4, 3, 'eq'),
        ]

        for btn_data in buttons:
            text, row, col, btn_type = btn_data
            btn = QPushButton(text)
            btn.setFont(QFont('Arial', 28, QFont.Normal))
            btn.setCursor(Qt.PointingHandCursor)

            if btn_type == 'func':
                style = 'QPushButton { background-color: #a5a5a5; color: black; border-radius: 40px; min-height: 80px; } QPushButton:pressed { background-color: #d4d4d2; }'
            elif btn_type in ('op', 'eq'):
                style = 'QPushButton { background-color: #ff9f0a; color: white; border-radius: 40px; min-height: 80px; } QPushButton:pressed { background-color: #ffcc80; }'
            elif btn_type == 'zero':
                style = 'QPushButton { background-color: #333335; color: white; border-radius: 40px; min-height: 80px; text-align: left; padding-left: 30px; } QPushButton:pressed { background-color: #636366; }'
            else:
                style = 'QPushButton { background-color: #333335; color: white; border-radius: 40px; min-height: 80px; } QPushButton:pressed { background-color: #636366; }'

            btn.setStyleSheet(style)
            btn.clicked.connect(lambda checked, t=text: self.on_button_click(t))

            if text == '0':
                grid.addWidget(btn, row, col, 1, 2)
            else:
                grid.addWidget(btn, row, col)

        main_layout.addLayout(grid)
        self.setLayout(main_layout)

    def on_button_click(self, text):
        if text.isdigit():
            result = self.calc.input_number(text)
            self.update_display(result)
        elif text == '.':
            result = self.calc.input_dot()
            self.update_display(result)
        elif text == 'AC':
            self.calc.reset()
            self.update_display('0')
        elif text == '+/-':
            result = self.calc.negative_positive()
            self.update_display(result)
        elif text == '%':
            result = self.calc.percent()
            self.update_display(result)
        elif text in ('+', '-', 'x', '/'):
            self.calc.set_operator(text)
        elif text == '=':
            result = self.calc.equal()
            self.update_display(result)

    def update_display(self, text):
        # 보너스 과제: 글자 수에 따라 폰트 크기 자동 조절
        length = len(text)
        if length > 9:
            size = 36
        elif length > 6:
            size = 48
        else:
            size = 64
        self.display.setFont(QFont('Arial', size, QFont.Light))
        self.display.setText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = CalculatorUI()
    ui.show()
    sys.exit(app.exec_())