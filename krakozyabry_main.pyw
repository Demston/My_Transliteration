"""Перевод с эльфийского. Транслитерация букв. Лёгкий аналог всеми известного ПО."""

import tkinter as tk
import pystray
from PIL import Image
from pystray import MenuItem as Item
from krakozyabry_script import *
import keyboard


def make_menu(w):
    """Команды вырезать/копировать/вставить"""
    global the_menu
    the_menu = tk.Menu(w, tearoff=0)
    the_menu.add_command(label="Вырезать")
    the_menu.add_command(label="Копировать")
    the_menu.add_command(label="Вставить")
    the_menu.add_command(label="Удалить")


def show_menu(e):
    """Контекстное меню с перечнем команд"""
    w = e.widget
    the_menu.entryconfigure("Вырезать", command=lambda: w.event_generate("<<Cut>>"))
    the_menu.entryconfigure("Копировать", command=lambda: w.event_generate("<<Copy>>"))
    the_menu.entryconfigure("Вставить", command=lambda: w.event_generate("<<Paste>>"))
    the_menu.entryconfigure("Удалить", command=lambda: w.event_generate("<<Clear>>"))
    the_menu.tk.call("tk_popup", the_menu, e.x_root, e.y_root)


window = tk.Tk()  # Создадим окно и области под текст и кнопки
window.title('Перевод с эльфийского')
window.geometry('500x260-25-45')
window.resizable(False, False)
# window.iconphoto(tk.PhotoImage(file='icon.ico'))
frame_text_undo = tk.Frame(window, background='#EEEEEE')
frame_text_undo.place(relx=0.01, rely=0.03, relheight=0.38, relwidth=0.98)
frame_text_after = tk.Frame(window, background='#EEEEEE')
frame_text_after.place(relx=0.01, rely=0.43, relheight=0.38, relwidth=0.98)
frame_for_button = tk.Frame(window, background='#EEEEEE')
frame_for_button.place(relx=0.01, rely=0.83, relheight=0.15, relwidth=0.98)


def quit_window(icon, Item):
    """Скрыть окно в трей"""
    pass


def show_window(icon, Item):
    """Развернуть окно из трея"""
    icon.stop()
    window.after(0, window.deiconify)


def withdraw_window():
    """Отрисовка меню в трее"""
    window.withdraw()
    image = Image.open('icon.ico')
    menu = (Item('Перевод с эльфийского', show_window), Item('Справка', about))
    icon = pystray.Icon('icon.ico', image, 'Перевод с эльфийского', menu)
    icon.run_detached()


def about():
    """Окно с краткой информацией"""
    about_window = tk.Tk()
    about_window.geometry('300x150-5-45')
    about_window.title('Что это:')
    about_window.resizable(False, False)
    # about_window.iconphoto(False, tk.PhotoImage(file='icon.ico'))
    lb = tk.Label(about_window, text='\nПеревод с эльфийского.\nТранслитерация букв.\n\n'
                                     'Скопируй в буфeр текст, нажми Ctrl + C + Shift,\n'
                                     'вставь из буфера исправленный текст. Всё.\n'
                                     'Либо воспользуйся окном программы.\n\n'
                                     '          Demston ⓒ  2024      ')
    lb.pack()
    about_window.mainloop()


make_menu(window)  # Присваиваем окну меню "Вырезать/Скопировать/Вставить"

# Поля для ввода текста и скроллинг
text_field_1 = tk.Text(frame_text_undo)
scrollbar_1 = tk.Scrollbar(frame_text_undo)
scrollbar_1.config(command=text_field_1.yview)
text_field_1.config(yscrollcommand=scrollbar_1.set)
scrollbar_1.pack(side=tk.RIGHT, fill=tk.Y)
text_field_1.place(relheight=1, relwidth=1)
text_field_1.bind_class("Text", "<Button-3><ButtonRelease-3>", show_menu)
text_field_2 = tk.Text(frame_text_after)
scrollbar_2 = tk.Scrollbar(frame_text_after)
scrollbar_2.config(command=text_field_2.yview)
text_field_2.config(yscrollcommand=scrollbar_2.set)
scrollbar_2.pack(side=tk.RIGHT, fill=tk.Y)
text_field_2.place(relheight=1, relwidth=1)


def edit_copy():
    """Поправить текст, вставить в буфер обмена"""
    global text_field_1, text_field_2
    text_field_2.delete(0.0, tk.END)
    get_text = text_field_1.get(0.0, tk.END)
    window.clipboard_clear()
    text_field_2.insert(0.0, translation(get_text))
    window.clipboard_append(translation(get_text))


def paste_edit_copy():
    """Скопировать текст из буфера обмена, поправить, вставить назад в буфер"""
    global text_field_1, text_field_2
    text_field_1.delete(0.0, tk.END)
    text_field_2.delete(0.0, tk.END)
    get_text = window.clipboard_get()
    window.clipboard_clear()
    text_field_1.insert(0.0, get_text)
    text_field_2.insert(0.0, translation(get_text))
    window.clipboard_append(translation(get_text))


def clean():
    """Очистить поля для ввода текста"""
    global text_field_1, text_field_2
    text_field_1.delete(0.0, tk.END)
    text_field_2.delete(0.0, tk.END)


def p_e_c_for_keyboard():
    """Скопировать текст из буфера обмена, поправить, вставить назад в буфер.
    Для обработки с помощью горячих клавиш, прямо в тексте, вне окна программы."""
    get_text = window.clipboard_get()
    window.clipboard_clear()
    window.clipboard_append(translation(get_text))


# Кнопки. Назначение каждой видно, исходя из наименований.
knopka_1 = tk.Button(frame_for_button, height=100, width=15, text='Исправить/\nСкопировать', font='Arial 10',
                     command=edit_copy)
knopka_1.pack(side=tk.LEFT)
knopka_2 = tk.Button(frame_for_button, height=100, width=25, text='Вставить/Исправить/\nСкопировать', font='Arial 10',
                     command=paste_edit_copy)
knopka_2.pack(side=tk.LEFT)
knopka_3 = tk.Button(frame_for_button, height=100, width=10, text='Очистить', font='Arial 10', command=clean)
knopka_3.pack(side=tk.LEFT)
knopka_4 = tk.Button(frame_for_button, height=100, width=5, text='Х', font='Arial 11', command=quit)
knopka_4.pack(side=tk.LEFT)

keyboard.add_hotkey('Ctrl + c + Shift', p_e_c_for_keyboard)   # Клавиши для обработки текста в фоне

window.protocol('WM_DELETE_WINDOW', withdraw_window)  # Вызов меню из трея
window.mainloop()
