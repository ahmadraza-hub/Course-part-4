# gorgeous_calculator_with_history.py
# Install: pip install PyQt5


import sys
import math
import ast
import operator as op
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout,
    QLineEdit, QLabel, QPushButton, QSizePolicy, QListWidget, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# --- Safe math evaluator ---
ALLOWED_FUNCS = {
    'sqrt': math.sqrt,
    'log': math.log,
    'log10': math.log10,
    'exp': math.exp,
    'abs': abs,
    'round': round,
    'floor': math.floor,
    'ceil': math.ceil,
}

ALLOWED_NAMES = {
    'pi': math.pi,
    'e': math.e
}

ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
    ast.FloorDiv: op.floordiv,
}

class EvalVisitor(ast.NodeVisitor):
    def visit(self, node):
        if isinstance(node, ast.Expression):
            return self.visit(node.body)
        return super().visit(node)

    def visit_Constant(self, node):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Invalid constant")

    def visit_Num(self, node):
        return node.n

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_type = type(node.op)
        if op_type in ALLOWED_OPERATORS:
            return ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Operator {op_type} not allowed")

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        op_type = type(node.op)
        if op_type in ALLOWED_OPERATORS:
            return ALLOWED_OPERATORS[op_type](operand)
        raise ValueError("Unary operator not allowed")

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            fname = node.func.id
            if fname in ALLOWED_FUNCS:
                func = ALLOWED_FUNCS[fname]
                args = [self.visit(a) for a in node.args]
                return func(*args)
        raise ValueError(f"Function calls not allowed or unknown: {ast.dump(node)}")

    def visit_Name(self, node):
        if node.id in ALLOWED_NAMES:
            return ALLOWED_NAMES[node.id]
        raise ValueError(f"Name {node.id} is not allowed")

    def generic_visit(self, node):
        raise ValueError(f"Unsupported expression: {type(node).__name__}")

def safe_eval(expr: str):
    expr = expr.replace('×', '*').replace('÷', '/').replace('^', '**').replace('%', '/100').replace('√', 'sqrt')
    expr = _insert_implicit_mul(expr)
    node = ast.parse(expr, mode='eval')
    visitor = EvalVisitor()
    return visitor.visit(node)

def _insert_implicit_mul(s: str) -> str:
    out = []
    prev = ''
    for ch in s:
        if prev and (prev.isdigit() or prev == ')') and (ch.isalpha() or ch == '('):
            out.append('*')
        out.append(ch)
        prev = ch
    return ''.join(out)

# --- GUI ---
class GorgeousCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gorgeous Calculator — Ahmad's Assistant Edition")
        self.setFixedSize(600, 600)
        self._last_result = None
        self.history = []

        # Layout setup
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # Left panel - calculator
        calc_widget = QWidget()
        calc_layout = QVBoxLayout(calc_widget)
        calc_layout.setSpacing(15)
        calc_layout.setContentsMargins(14, 14, 14, 14)

        # Display
        self.preview = QLabel("")
        self.preview.setAlignment(Qt.AlignRight)
        self.preview.setFont(QFont('Segoe UI', 10))
        self.preview.setStyleSheet("color: rgba(255,255,255,0.75);")

        self.expr_display = QLineEdit()
        self.expr_display.setReadOnly(True)
        self.expr_display.setAlignment(Qt.AlignRight)
        self.expr_display.setFont(QFont('Segoe UI', 28, QFont.Bold))
        self.expr_display.setFixedHeight(80)

        calc_layout.addWidget(self.preview)
        calc_layout.addWidget(self.expr_display)

        # Buttons with gaps
        grid = QGridLayout()
        grid.setSpacing(12)

        buttons = [
            ('C', 0, 0), ('⌫', 0, 1), ('%', 0, 2), ('÷', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('×', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('±', 4, 0), ('0', 4, 1), ('.', 4, 2), ('=', 4, 3),
            ('(', 5, 0), (')', 5, 1), ('√', 5, 2), ('x²', 5, 3),
            ('1/x', 6, 0)
        ]

        self.buttons = {}
        for (text, r, c) in buttons:
            btn = QPushButton(text)
            btn.setProperty('btnText', text)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setFont(QFont('Segoe UI', 12, QFont.Medium))
            btn.clicked.connect(self.on_button_clicked)
            grid.addWidget(btn, r, c)
            self.buttons[text] = btn

        calc_layout.addLayout(grid)

        main_layout.addWidget(calc_widget, stretch=3)

        # Right panel - history
        self.history_list = QListWidget()
        self.history_list.setFont(QFont('Segoe UI', 10))
        self.history_list.setStyleSheet("""
            QListWidget {
                background: rgba(255,255,255,0.05);
                color: white;
                border-radius: 8px;
                padding: 8px;
            }
        """)
        main_layout.addWidget(self.history_list, stretch=1)

        # Style
        self.setStyleSheet(self.get_stylesheet())

    def get_stylesheet(self):
        return """
        QMainWindow {
            background: qlineargradient(x1:0 y1:0, x2:1 y2:1,
                        stop:0 #2b5876, stop:1 #4e4376);
        }
        QLabel {
            color: rgba(255,255,255,0.85);
        }
        QLineEdit {
            background: rgba(255,255,255,0.06);
            border: none;
            color: white;
            padding-right: 10px;
            border-radius: 10px;
        }
        QPushButton {
            border: none;
            border-radius: 12px;
            padding: 12px;
            background: rgba(255,255,255,0.07);
            color: white;
        }
        QPushButton[btnText="="] {
            background: qlineargradient(x1:0 y1:0, x2:0 y2:1, stop:0 #ff7b54, stop:1 #ff3d00);
            color: white;
            font-weight: 700;
        }
        """

    def on_button_clicked(self):
        sender = self.sender()
        key = sender.property('btnText')
        cur = self.expr_display.text()

        if key == 'C':
            self.expr_display.clear()
            self.preview.clear()
            return
        if key == '⌫':
            self.expr_display.setText(cur[:-1])
            return
        if key == '=':
            self.calculate()
            return
        if key == '±':
            if cur.startswith('-'):
                self.expr_display.setText(cur[1:])
            else:
                self.expr_display.setText('-' + cur)
            return
        if key == '√':
            self.expr_display.setText(cur + 'sqrt(')
            return
        if key == 'x²':
            self.expr_display.setText(cur + '**2')
            return
        if key == '1/x':
            self.expr_display.setText(cur + '1/(')
            return

        self.expr_display.setText(cur + key)

    def calculate(self):
        expr = self.expr_display.text().strip()
        if not expr:
            return
        try:
            result = safe_eval(expr)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.preview.setText(expr + " =")
            self.expr_display.setText(str(result))
            self._last_result = result
            self.add_to_history(expr, result)
        except Exception:
            self.preview.setText("Error")
            self.expr_display.setText("")

    def add_to_history(self, expr, result):
        entry = f"{expr} = {result}"
        self.history_list.insertItem(0, entry)  # newest at top
        self.history.append(entry)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = GorgeousCalculator()
    calc.show()
    sys.exit(app.exec_())
