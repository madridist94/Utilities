import re
import PySimpleGUI as sg
import pyperclip

def extract_articles(text):
    regex = r"(?<!\d)[1-9]{1}[0-9]{5,7}(?!\d)"
    return re.findall(regex, text)

def main():
    sg.theme("DarkAmber")

    layout = [
        [sg.Text("Введите текст с артикулами:")],
        [sg.Multiline(size=(60, 10), key="-INPUT-")],
        [sg.Button("Вставить текст", key="-PASTE-"), sg.Button("Извлечь артикулы"), sg.Button("Очистить")],
        [sg.Text("Артикулы через запятую:")],
        [sg.Multiline(size=(60, 5), key="-OUTPUT1-")],
        [sg.Button("Копировать", key="-COPY1-")],
        [sg.Text("Артикулы в столбик:")],
        [sg.Multiline(size=(60, 5), key="-OUTPUT2-")],
        [sg.Button("Копировать", key="-COPY2-")],
        

    ]

    window = sg.Window("Извлечение артикулов", layout, return_keyboard_events=True, use_default_focus=False)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
        if event == "Извлечь артикулы":
            articles = extract_articles(values["-INPUT-"])
            window["-OUTPUT1-"].update(", ".join(articles))
            window["-OUTPUT2-"].update("\n".join(articles))
        elif event == "-COPY1-":
            pyperclip.copy(window["-OUTPUT1-"].get())
        elif event == "-COPY2-":
            pyperclip.copy(window["-OUTPUT2-"].get())
        elif event == "Очистить":
            window["-INPUT-"].update("")
        elif event == "^V" or event == "^в" or event == "-PASTE-":
            current_text = window["-INPUT-"].get()
            new_text = pyperclip.paste()
            window["-INPUT-"].update(current_text + new_text)

    window.close()

if __name__ == "__main__":
    main()
