import PySimpleGUI as sg
from PIL import Image
import glob, os


def batchProcessImages(windows_size=(100,100)):
    # os.chdir("/mydir")
    for file in glob.glob("*.png"):
        im = Image.open(file)
        im = im.resize(windows_size)
        # print(file)
        im.save("processed/"+file)


class Gesture:
    def __init__(self):
        self.state = 0
        self.use_caps = False
        # vowels
        self.state0dict = {'SW': 'u', 'SE': 'a', 'S': 'e', 'NW': 'i', 'N': 'CAP', 'NE': 'o', 'UP': '?', 'DOWN': '!'}
        # rest of letters
        self.state1dict = {'SW': 'h', 'SE': 'n', 'S': 't', 'NW': 'd', 'N': 'r', 'NE': 's', 'UP': '?', 'DOWN': '!'}
        self.state2dict = {'SW': 'y', 'SE': 'c', 'S': 'l', 'NW': 'w', 'N': 'f', 'NE': 'm', 'UP': '?', 'DOWN': '!'}
        self.state3dict = {'SW': 'k', 'SE': 'p', 'S': 'g', 'NW': 'x', 'N': 'e', 'NE': 'b', 'UP': '?', 'DOWN': '!'}
        self.state4dict = {'SW': ',', 'SE': 'j', 'S': 'q', 'NW': ':', 'N': '\'', 'NE': 'z', 'UP': '?', 'DOWN': '!'}
        self.list_dict = [self.state0dict, self.state1dict, self.state2dict, self.state3dict, self.state4dict]
        self.state_map = {'DL': 2, 'UL': 1, 'DR': 4, 'UR': 3}

    def swipeDetect(self, start, end):
        # This function defines swiping patterns from starting and ending point
        if start is end:
            return "Tap"

        if start == 4:
            if end == 0:
                return "SW"
            if end == 1:
                return "S"
            if end == 2:
                return "SE"
            if end == 6:
                return "NW"
            if end == 7:
                return "N"
            if end == 8:
                return "NE"
        elif start == 6 and end == 4:
            return "DR"
        elif start == 0 and end == 4:
            return "UR"
        elif start == 8 and end == 4:
            return "DL"
        elif start == 2 and end == 4:
            return "UL"
        elif (start == 8 and end == 6) or (start == 5 and end == 3) or (start == 2 and end == 0):
            return "L"
        elif start == 1 and end == 7:
            return "UP"
        elif start == 7 and end == 1:
            return "DOWN"
        else:
            return

    def swipeTrigger(self, start, end):
        # This function defines mapping from swiping to letters
        swipe_command = self.swipeDetect(start, end)

        if swipe_command is None:
            print('unknown command')
        elif swipe_command in self.state_map.keys():
            self.state = self.state_map[swipe_command]
        elif swipe_command == "L":
            return "DEL"
        elif swipe_command == "Tap" and self.state == 0:
            return " "
        elif self.state is not 0 and swipe_command == "Tap":
            self.state = 0
        elif self.list_dict[self.state][swipe_command] == 'CAP':
            self.use_caps = True
        else:
            output = self.list_dict[self.state][swipe_command]
            self.state = 0
            if self.use_caps is True:
                output = output.upper()
            self.use_caps = False
            return output

        return


def analyseGesture(input_segment, graph_size):
    return getSegment(input_segment[0], graph_size), getSegment(input_segment[1], graph_size)


def getSegment(point_coordinate, graph_size):
    x, y = point_coordinate
    if x < graph_size[0] / 3.0:
        # on the left side
        if y < graph_size[1] / 3.0:
            return 0
        elif y < graph_size[1] / 3.0 * 2.0:
            return 3
        else:
            return 6
    elif x < graph_size[0] / 3.0 * 2.0:
        # in the middle
        if y < graph_size[1] / 3.0:
            return 1
        elif y < graph_size[1] / 3.0 * 2.0:
            return 4
        else:
            return 7
    else:
        if y < graph_size[1] / 3.0:
            return 2
        elif y < graph_size[1] / 3.0 * 2.0:
            return 5
        else:
            return 8


def main():
    # obj = tk.Tk() # Creates a tkinter object
    # label = tk.Label(obj, text="This is a text button")

    # print(sg.Window.get_screen_size())
    # w, h = sg.Window.get_screen_size()

    interactive_size = (200, 200)
    graph_size = (800, 800)
    layout = [[sg.Text('Text Entry:'), sg.Text(size=(150, 1), key='-OUTPUT-')],
              [sg.Text('Word Count:'), sg.Text(size=(3,1), key='-WORDCOUNT-')],
              [sg.Graph(canvas_size=interactive_size, graph_bottom_left=(0, 0), graph_top_right=interactive_size,
                        enable_events=True, drag_submits=True, key="-INTER-", change_submits=True,
                        background_color='lightblue')]]

    window = sg.Window(title="Fig Binger", layout=layout)
    window.finalize()
    # graph = window["-GRAPH-"]
    interactive_graph = window["-INTER-"]

    # process image before we load them
    batchProcessImages(windows_size=interactive_size)



    interactive_graph.DrawImage(filename="processed/" + "lowercase_state0.png", location=(0, interactive_size[1]))

    # ---===--- Loop taking in user input --- #
    dragging = False
    start_point = end_point = prior_rect = None

    gesture = Gesture()

    text_entered = ''
    tail = '.png'

    while True:
        # this block processes the motion
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'End':
            break
        if event is None:
            break
        if event == "-INTER-":
            x, y = values["-INTER-"]
            if not dragging:
                start_point = (x, y)
                dragging = True

            else:
                end_point = (x, y)
        if event == 'Count':
            window['-WORDCOUNT-'].update(len(text_entered.split()))
        elif event.endswith('+UP'):  # The drawing has ended because mouse up

            # info = window["info"]
            # info.update(value=f"grabbed rectangle from {start_point} to {end_point}")

            gesture_segment = (start_point, end_point)

            # clear all the buffer
            start_point, end_point = None, None  # enable grabbing a new rect
            dragging = False
            prior_rect = None

            # return the segments
            output_gesture = analyseGesture(gesture_segment, interactive_size)
            print("start", output_gesture[0], "end", output_gesture[1])

            output_string = gesture.swipeTrigger(output_gesture[0], output_gesture[1])

            name_prefix = "uppercase_" if gesture.use_caps else "lowercase_"
            state_png_name = "processed/" + name_prefix + "state" + str(gesture.state) + ".png"
            interactive_graph.DrawImage(filename=state_png_name, location=(0, interactive_size[1]))

            if output_string is None:
                continue
            elif output_string == 'DEL':
                if text_entered == '':
                    continue
                else:
                    text_entered = text_entered[:-1]
            else:
                text_entered += output_string


        window['-OUTPUT-'].update(text_entered)
        # Gesture.swipeDetect(output_gesture[0], output_gesture[1])
    window.close()


main()
