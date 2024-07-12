from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout
import json
########

########
app = QApplication([])
win = QWidget()
win.setWindowTitle('Умные заметки')
win.resize(900,600)
########


########
notes = {'Правила футбола': {'текст': 'Длина игры: 90 минут с перерывом в середине игры',
         'тэги': ['Правила','Футбол']}}
# with open('f.json','w') as file:
#    json.dump(notes,file)
########
nad1 = QLabel('Список заметок')
nad2 = QLabel('Список тегов')

btn_create_note = QPushButton('Создать заметка')
btn_delete_note = QPushButton('Удалить заметку')
btn_save_note = QPushButton('Сохранить заметку')

btn_add_tag = QPushButton('Добавить к заметке')
btn_delete_tag = QPushButton('Открепить от заметки')
btn_search_tag = QPushButton('Искать заметки по тегу')

field_text = QTextEdit()
field_tag = QLineEdit()
field_tag.setPlaceholderText('Введите тег...')

list_tags = QListWidget()
list_notes = QListWidget()
##########


##########
cal1 = QVBoxLayout()
cal2 = QVBoxLayout()
h1 = QHBoxLayout()
h2 = QHBoxLayout()
h3 = QHBoxLayout()
h4 = QHBoxLayout()
glav = QHBoxLayout()

cal1.addWidget(field_text)

cal2.addWidget(nad1)
cal2.addWidget(list_notes)

h1.addWidget(btn_create_note)
h1.addWidget(btn_delete_note)
cal2.addLayout(h1)

h2.addWidget(btn_save_note)
cal2.addLayout(h2)

cal2.addWidget(nad2)
cal2.addWidget(list_tags)
cal2.addWidget(field_tag)

h3.addWidget(btn_add_tag)
h3.addWidget(btn_delete_tag)

h4.addWidget(btn_search_tag)
cal2.addLayout(h3)
cal2.addLayout(h4)

glav.addLayout(cal1)
glav.addLayout(cal2)
win.setLayout(glav)
##########

def add_note():
    note_name, result = QInputDialog.getText(win,'Добавить заметку','Название заметки')
    if result and note_name != '':
        notes[note_name] = {'текст': '', 'тэги': []}
        list_notes.addItem(note_name)


def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open('f.json','w') as file:
            json.dump(notes,file)
    else:
        print('Заметка для удаления не выбрана!')

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]['текст'] = field_text.toPlainText()
        with open('f.json','w') as file:
            json.dump(notes,file)
    else:
        print('Заметка для сохранения не выбрана!')

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]['тэги']:
            notes[key]['тэги'].append(tag)
            field_tag.clear()
            list_tags.addItem(tag)
        with open('f.json','w') as file:
            json.dump(notes,file)
    else:
        print('Заметка для сохранения тега не выбрана!')

def del_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]['тэги'].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]['тэги'])
        with open('f.json','w') as file:
            json.dump(notes,file)
    else:
        print('Заметка для удаления тега не выбрана!')

def search_tag():
    tag = field_tag.text()
    if btn_search_tag.text() == 'Искать заметки по тегу' and tag:
        notes_field = {}
        for note in notes:
            if tag in notes[note]['тэги']:
                notes_field[note] = notes[note]
        btn_search_tag.setText('Сбросить поиск')
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_field)
    elif btn_search_tag.text() == 'Сбросить поиск':
        list_notes.clear()
        list_tags.clear()
        field_tag.clear()
        list_notes.addItems(notes)
        btn_search_tag.setText('Искать заметки по тегу')
    else:
        pass

##########
def show_note():
    name = list_notes.selectedItems()[0].text()
    field_text.setText(notes[name]['текст'])
    list_tags.clear()
    list_tags.addItems(notes[name]['тэги'])

list_notes.itemClicked.connect(show_note)
##########

btn_create_note.clicked.connect(add_note)
btn_delete_note.clicked.connect(del_note)
btn_save_note.clicked.connect(save_note)

btn_add_tag.clicked.connect(add_tag)
btn_delete_tag.clicked.connect(del_tag)
btn_search_tag.clicked.connect(search_tag)
##########

win.show()
with open('f.json','r') as file:
    notes = json.load(file)
list_notes.addItems(notes)
app.exec()
