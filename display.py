import PySimpleGUI as pyg

## This is the display that shows the texts we input
pyg.theme('DarkAmber')
# Stuff inside your window

layout = [[pyg.Text('Text Entry:'), pyg.Text(size=(100, 1), key='-OUTPUT-')],
          [pyg.Text('Word Count:'), pyg.Text(size=(3,1), key='-WORDCOUNT-')],
          [pyg.Input(key='-IN-')],
          [pyg.Button('A'), pyg.Button('E'), pyg.Button('I'), pyg.Button('O'), pyg.Button('U'), pyg.Button(' ')],
          [pyg.Button('Enter'), pyg.Button('Clear'), pyg.Button('Exit')]]

window = pyg.Window('Display', layout)

text_entered = ''
while True:
    event, values = window.read()
    print(event, values)
    if event == pyg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Clear':
        text_entered = ''
    if event in 'AEIOU ':
        text_entered = values['-IN-']
        text_entered += event
    if event == 'Enter':
        text_entered = values['-IN-']
        window['-OUTPUT-'].update(text_entered)
        window['-WORDCOUNT-'].update(len(values['-IN-'].split()))

    window['-IN-'].update(text_entered)

window.close()


