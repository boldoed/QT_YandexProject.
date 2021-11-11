from sqlite3.dbapi2 import Cursor
import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow

from project_db import ProjectDB


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('project.ui', self)
        # подключение БД
        self.connection = sqlite3.connect('QT_Project_db.db')
        self.cursor = self.connection.cursor()
        self.information_k = 0
        self.Information_btn.clicked.connect(self.information)
        self.information_text.hide()
        self.information_text.setText('Эта программа поможет вам следить за своими финансами, а также правильно ими распоряжаться.')
        self.rashod_btn.clicked.connect(self.rashod_func)
        self.popolnenie_btn.clicked.connect(self.popolnit_func)
        # Обновляем главное окно
        self.update_main_window()
    
    '''
    информация о приложении
    '''
    def information(self):
        self.information_k += 1
        if self.information_k % 2 != 0:
            self.information_text.show()
        else:
            self.information_text.hide()

    '''
    вызывает окно расходов
    '''
    def rashod_func(self):
        self.form = AddRashod()
        self.form.exec_()
    
    '''
    вызывает окно доходов
    '''
    def popolnit_func(self):
        self.form = AddPopolnenia(self)
        self.form.exec_()

    '''
    сумма расходов
    '''
    def rashod_sum(self):
        vse_rashodi_list = []
        vse_rashodi = self.cursor.execute("""SELECT summa FROM rashodi""").fetchall()
        for i in vse_rashodi:
            vse_rashodi_list.append(int(str(i)[1:-2]))

        return sum(vse_rashodi_list)

    '''
    сумма доходов
    '''
    def dohod_sum(self):
        vse_dohodi_list = []
        vse_dohodi = self.cursor.execute("""SELECT summa FROM dohodi""").fetchall()
        for i in vse_dohodi:
            vse_dohodi_list.append(int(str(i)[1:-2]))
            
        return sum(vse_dohodi_list)

    '''
    обновление главного окна
    '''
    def update_main_window(self):
        self.balance.setText(
            f'     Остаток средств: {self.dohod_sum() - self.rashod_sum()} руб.')
        self.dohod.setText(
            f'     Зачисления: {self.dohod_sum()} руб.')

        self.rashod.setText(
            f'     Расходы: {self.rashod_sum()} руб.')





class AddRashod(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('add_rashodi.ui', self)
        # подключение БД
        self.connection = sqlite3.connect('QT_Project_db.db')
        self.cursor = self.connection.cursor()
        self.addr.clicked.connect(self.add_elem)
        self.update_rashod()
        self.update_category_rashod()

    '''
    вызывает окно добавления элемента
    '''
    def add_elem(self):
        self.form = AddElem(self)
        self.form.exec_()
        if self.form.ok_pressed:
            self.update_rashod()
            self.update_category_rashod()
            MyWidget().update_main_window()

        
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


    '''
    обновляет/отображает список расходов по категориям
    '''
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
        # подключение БД
        self.connection = sqlite3.connect('QT_Project_db.db')
        self.cursor = self.connection.cursor()
        self.main_window = MyWidget
        self.ok_btn.clicked.connect(self.add_rashod)
        self.cancel_btn.clicked.connect(self.close)
        self.ok_pressed = False

    '''
    добавляет расход в БД
    '''
    def add_rashod(self):
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


class AddPopolnenia(QDialog):
    def __init__(self, MyWidget):
        super().__init__()
        uic.loadUi('add_popolnenia.ui', self)
        # подключение БД
        self.connection = sqlite3.connect('QT_Project_db.db')
        self.cursor = self.connection.cursor()
        self.main_window = MyWidget
        self.addp.clicked.connect(self.add_elem_z)
        self.update_dohod()

    '''
    вызывает окно добавления элемента
    '''
    def add_elem_z(self):
        self.form = AddElemZ(self)
        self.form.exec_()
        if self.form.ok_pressed_z:
            self.update_dohod()
            MyWidget().update_main_window()
        
    '''
    обновляет/отображает список доходов
    '''
    def update_dohod(self):
        self.dohod_spisok = ''
        self.spisok_dohodov = self.cursor.execute("""SELECT * FROM dohodi""").fetchall()
        for i in self.spisok_dohodov:
            self.dohod_spisok += (str(', '.join([str(j) for j in i][1:])) + '\n')
        if self.dohod_window.toPlainText() != self.dohod_spisok:
            self.dohod_window.setText('')
            self.dohod_window.setText(self.dohod_spisok)


class AddElemZ(QDialog):
    def __init__(self, MyWidget):
        super().__init__()
        uic.loadUi('add_elem_z.ui', self)
        # подключение БД
        self.connection = sqlite3.connect('QT_Project_db.db')
        self.cursor = self.connection.cursor()
        self.main_window = MyWidget
        self.ok_btn_z.clicked.connect(self.add_dohod)
        self.cancel_btn_z.clicked.connect(self.close)
        self.ok_pressed_z = False

    '''
    добавляет доход в БД
    '''
    def add_dohod(self):
        self.name_ = self.name_edit_z.text()
        self.summa_ = self.summa_edit_z.value()
        self.date_ = self.date_edit_z.text()
        dohod_inf = []
        if self.name_ != '':
            dohod_inf.append(str(self.name_))
        if self.summa_ != 0:
            dohod_inf.append(int(str(self.summa_)))
        dohod_inf.append(self.date_)
        if len(dohod_inf) == 3:
            self.cursor.execute(f"""INSERT INTO dohodi(name, summa, date)
            VALUES(?, ?, ?)""", dohod_inf)
            self.connection.commit()
        self.ok_pressed_z = True
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())