import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.current_input = '0'
        self.previous_input = ''
        self.operator = ''
        self.reset_next = False
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Calculator')
        self.setFixedSize(360, 600)
        self.setStyleSheet('background-color: #1c1c1e;')

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 20, 10, 10)
        main_layout.setSpacing(0)

        # 디스플레이
        self.display = QLabel('0')
        self.display.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.display.setFont(QFont('Arial', 64, QFont.Light))
        self.display.setStyleSheet('color: white; padding: 10px 20px 10px 10px;')
        self.display.setMinimumHeight(160)
        main_layout.addWidget(self.display)

        # 버튼 그리드
        grid = QGridLayout()
        grid.setSpacing(10)

        buttons = [
            ('AC', 0, 0, 'func'),  ('±', 0, 1, 'func'),  ('%', 0, 2, 'func'),  ('÷', 0, 3, 'op'),
            ('7',  1, 0, 'num'),   ('8',  1, 1, 'num'),   ('9',  1, 2, 'num'),  ('×', 1, 3, 'op'),
            ('4',  2, 0, 'num'),   ('5',  2, 1, 'num'),   ('6',  2, 2, 'num'),  ('-', 2, 3, 'op'),
            ('1',  3, 0, 'num'),   ('2',  3, 1, 'num'),   ('3',  3, 2, 'num'),  ('+', 3, 3, 'op'),
            ('0',  4, 0, 'zero'),  ('.',  4, 2, 'num'),   ('=',  4, 3, 'eq'),
        ]

        for btn_data in buttons:
            text, row, col, btn_type = btn_data
            btn = QPushButton(text)
            btn.setFont(QFont('Arial', 28, QFont.Normal))
            btn.setCursor(Qt.PointingHandCursor)

            if btn_type == 'func':
                style = '''
                    QPushButton {
                        background-color: #a5a5a5;
                        color: black;
                        border-radius: 40px;
                        min-height: 80px;
                    }
                    QPushButton:pressed { background-color: #d4d4d2; }
                '''
            elif btn_type == 'op':
                style = '''
                    QPushButton {
                        background-color: #ff9f0a;
                        color: white;
                        border-radius: 40px;
                        min-height: 80px;
                    }
                    QPushButton:pressed { background-color: #ffcc80; }
                '''
            elif btn_type == 'eq':
                style = '''
                    QPushButton {
                        background-color: #ff9f0a;
                        color: white;
                        border-radius: 40px;
                        min-height: 80px;
                    }
                    QPushButton:pressed { background-color: #ffcc80; }
                '''
            elif btn_type == 'zero':
                style = '''
                    QPushButton {
                        background-color: #333335;
                        color: white;
                        border-radius: 40px;
                        min-height: 80px;
                        text-align: left;
                        padding-left: 30px;
                    }
                    QPushButton:pressed { background-color: #636366; }
                '''
            else:
                style = '''
                    QPushButton {
                        background-color: #333335;
                        color: white;
                        border-radius: 40px;
                        min-height: 80px;
                    }
                    QPushButton:pressed { background-color: #636366; }
                '''

            btn.setStyleSheet(style)
            btn.clicked.connect(lambda checked, t=text: self.on_button_click(t))

            if text == '0':
                grid.addWidget(btn, row, col, 1, 2)
            else:
                grid.addWidget(btn, row, col)

        main_layout.addLayout(grid)
        self.setLayout(main_layout)

    def on_button_click(self, text):
        # 숫자 입력
        if text.isdigit() or text == '.':
            if self.reset_next:
                self.current_input = text
                self.reset_next = False
            else:
                if text == '.' and '.' in self.current_input:
                    return
                if self.current_input == '0' and text != '.':
                    self.current_input = text
                else:
                    self.current_input += text
            self.update_display(self.current_input)

        # AC 버튼
        elif text == 'AC':
            self.current_input = '0'
            self.previous_input = ''
            self.operator = ''
            self.reset_next = False
            self.update_display('0')

        # 부호 변환
        elif text == '±':
            if self.current_input != '0':
                if self.current_input.startswith('-'):
                    self.current_input = self.current_input[1:]
                else:
                    self.current_input = '-' + self.current_input
                self.update_display(self.current_input)

        # 퍼센트
        elif text == '%':
            value = float(self.current_input) / 100
            self.current_input = self.format_result(value)
            self.update_display(self.current_input)

        # 연산자
        elif text in ('+', '-', '×', '÷'):
            self.previous_input = self.current_input
            self.operator = text
            self.reset_next = True

        # 등호
        elif text == '=':
            if self.operator and self.previous_input:
                result = self.calculate(
                    float(self.previous_input),
                    float(self.current_input),
                    self.operator
                )
                self.current_input = self.format_result(result)
                self.update_display(self.current_input)
                self.operator = ''
                self.previous_input = ''
                self.reset_next = True

    def calculate(self, a, b, op):
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '×':
            return a * b
        elif op == '÷':
            if b == 0:
                self.update_display('오류')
                return 0
            return a / b
        return 0

    def format_result(self, value):
        if value == int(value):
            return str(int(value))
        return str(round(value, 10)).rstrip('0')

    def update_display(self, text):
        # 글자 수에 따라 폰트 크기 조절
        if len(text) > 9:
            self.display.setFont(QFont('Arial', 36, QFont.Light))
        elif len(text) > 6:
            self.display.setFont(QFont('Arial', 48, QFont.Light))
        else:
            self.display.setFont(QFont('Arial', 64, QFont.Light))
        self.display.setText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())