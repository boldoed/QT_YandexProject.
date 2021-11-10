from sqlite3.dbapi2 import Cursor
import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow

from project_db import ProjectDB


# VSE_RASHODI = []


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('project.ui', self)

        # self.database = ProjectDB('QT_Project_db.db')
        self.connection = sqlite3.connect('QT_Project_db.db')
        self.cursor = self.connection.cursor()
        self.information_k = 0
        self.popolnenie_btn.clicked.connect(self.popolnit_func)
        # self.balance.setText(f'     Остаток средств: {self.balance_value} руб.')
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
    
    '''
    информация о приложении
    '''
    def information(self):
        self.information_k += 1
        if self.information_k % 2 != 0:
            self.information_text.show()
        else:
            self.information_text.hide()

    def rashod_func(self):
        self.form = AddRashod()
        self.form.exec_()

    def popolnit_inf(self):
        self.form = AddPopolnenia(self)
        self.form.exec_()

    def popolnit_func(self):
        self.form = AddElemZ(self)
        self.form.exec_()

    # сколько потрачено за месяц (сумма)
    # def get_month_spent_sum(self):
    #     elems = self.database.get_month_spent()
    #     return sum([item.get_sum() for item in elems])

    # сколько заработано за месяц (сумма)
    # def get_month_earned_sum(self):
    #     items = self.database.get_month_earned()
    #     return sum([elem.get_sum() for elem in items])


    # обновление главного окна
    # def update_main_window(self):
    #     self.budget_label.setText(
    #         '     Остаток средств:' +
    #         f'{self.get_month_earned_sum() - self.get_month_spent_sum()} руб.')

    #     self.popolnenie.setText(
    #         f'     Зачисления: {self.get_month_earned_sum()} руб.')

    #     self.rashod.setText(
    #         f'     Расходы: {self.get_month_spent_sum()} руб.')





class AddRashod(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('add_rashodi.ui', self)
        self.connection = sqlite3.connect('QT_Project_db.db')
        self.cursor = self.connection.cursor()
        self.addr.clicked.connect(self.add_elem)
        self.update_rashod()

    def add_elem(self):
        self.form = AddElem(self)
        self.form.exec_()
        if self.form.ok_pressed:
            self.update_rashod()
            self.update_category_rashod()
        
    '''
    обновляет/отображает список расходов
    '''
    def update_rashod(self):
        self.rashod_spisok = ''
        self.spisok_rashodov = self.cursor.execute("""SELECT * FROM rashodi""").fetchall()
        for i in self.spisok_rashodov:
            self.rashod_spisok += (str(', '.join([str(j) for j in i][1:])) + '\n')
        if self.rashod_window.toPlainText() != self.rashod_spisok:
            self.rashod_window.setText('')
            self.rashod_window.setText(self.rashod_spisok)

    def update_category_rashod(self):
        self.category_rashod_dict = {}
        self.category_rashod_dict_str = ''
        for i in self.spisok_rashodov:
            if i[-1] not in self.category_rashod_dict:
                self.category_rashod_dict[i[-1]] = [i[1:-1]]
            else:
                categoryes = self.category_rashod_dict.get(i[-1])
                categoryes.append(i[1:-1])
        for key, value in self.category_rashod_dict.items():
            value = " \n ".join([str(i) for i in value])  
            self.category_rashod_dict_str += f'''---{key}--- \n {value} \n'''
        self.categories_window.setText(self.category_rashod_dict_str)
 

class AddElem(QDialog):
    def __init__(self, MyWidget):
        super().__init__()
        uic.loadUi('add_elem.ui', self)
        self.connection = sqlite3.connect('QT_Project_db.db')
        self.cursor = self.connection.cursor()
        self.main_window = MyWidget
        self.ok_btn.clicked.connect(self.close_rashod)
        self.cancel_btn.clicked.connect(self.close)
        self.ok_pressed = False

    def close_rashod(self):
        self.name_ = self.name_edit.text()
        self.summa_ = self.summa_edit.value()
        self.cat_ = self.cat_edit.currentText()
        self.date_ = self.date_edit.text()
        rashod_inf = []
        if self.name_ != '':
            rashod_inf.append(str(self.name_))
        if self.summa_ != 0:
            rashod_inf.append(int(str(self.summa_)))
        rashod_inf.append(self.date_)
        rashod_inf.append(self.cat_)
        if len(rashod_inf) == 4:
            self.cursor.execute(f"""INSERT INTO rashodi(name, summa, date, category)
            VALUES(?, ?, ?, ?)""", rashod_inf)
            self.connection.commit()
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