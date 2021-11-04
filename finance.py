import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QInputDialog


VSE_RASHODI = []


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('project.ui', self)
        self.balance_value = 0
        self.information_k = 0
        self.popolnenie_btn.clicked.connect(self.popolnit_func)
        self.balance.setText(f'     Остаток средств: {self.balance_value} руб.')
        self.Information_btn.clicked.connect(self.information)
        self.information_text.hide()
        self.information_text.setText('Эта программа поможет вам следить за своими финансами, а также правильно ими распоряжаться.')
        self.rashod_btn.clicked.connect(self.rashod_func)
        self.popolnenie_inf_btn.clicked.connect(self.popolnit_inf)

    #def popolnit(self):
    #    summa, ok_pressed = QInputDialog.getInt(self, "Пополнение", "Введите сумму пополнения:", 0)

    #    if ok_pressed:
    #        self.balance_value += summa
    #        self.balance.setText(f'     Остаток средств: {self.balance_value} руб.')
    

    def information(self):
        self.information_k += 1
        if self.information_k % 2 != 0:
            self.information_text.show()
        else:
            self.information_text.hide()

    def rashod_func(self):
        self.form = AddRashod()
        self.form.exec_()
        # if self.form.form.ok_pressed:
        #     print(self.form.form.name_edit.text())

    def popolnit_inf(self):
        self.form = AddPopolnenia(self)
        self.form.exec_()

    def popolnit_func(self):
        self.form = AddElemZ(self)
        self.form.exec_()


class AddRashod(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('add_rashodi.ui', self)
        self.addr.clicked.connect(self.add_elem)


    def add_elem(self):
        self.form = AddElem(self)
        self.form.exec_()
        if self.form.ok_pressed:
            print(self.form.name_edit.text())


class AddElem(QDialog):
    def __init__(self, MyWidget):
        super().__init__()
        uic.loadUi('add_elem.ui', self)
        self.main_window = MyWidget
        self.ok_btn.clicked.connect(self.qwerty)
        self.cancel_btn.clicked.connect(self.close)
        self.ok_pressed = False

    def qwerty(self):
        self.ok_pressed = True
        self.close()



class AddElemZ(QDialog):
    def __init__(self, MyWidget):
        super().__init__()
        uic.loadUi('add_elem_z.ui', self)
        self.main_window = MyWidget


class AddPopolnenia(QDialog):
    def __init__(self, MyWidget):
        super().__init__()
        uic.loadUi('add_popolnenia.ui', self)
        self.main_window = MyWidget


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())