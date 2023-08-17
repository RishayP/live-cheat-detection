import PySimpleGUI as sg
import time

sg.theme('DarkAmber')

layout = [
    [sg.Text("With your own knowledge, type the answer to the following question:")],
    [sg.Text("Explain the concept of the Industrial Revolution and its impact on society.")],
    # [sg.Text("How does the architecture of urban environments affect community interactions and mental well-being?")],
    [sg.MLine(size=(40, 20), key='-ML1-'), sg.MLine(size=(40, 20), key='-ML2-')],
    [sg.B('Cancel')]
]

layout2 = [
    [sg.MLine(size=(80, 20), key='-ML3-')],
]

# Create main window
window = sg.Window('Text Copy', layout, finalize=True)

# List to hold the dictionaries
history_list = [{'timestamp': time.time(), 'state': ""}]

prev_input = ""
prev_cursor_position = None
prev_mouse_position = None

# Event loop for the main window
while True:
    event, values = window.read(timeout=0.1)

    if event == sg.WINDOW_CLOSED:
        break

    if event == 'PopUp':
        timestamp2 = time.time()

        # Find the most recent state at the given timestamp
        state_found = None
        for item in reversed(history_list):
            if item['timestamp'] < timestamp2:
                state_found = item['state']
                break

        # Create the PopUp window and show the state
        if state_found is not None:
            window2 = sg.Window('Pop Up', layout2, finalize=True)
            window2['-ML3-'].update(state_found)
            window2.read(timeout=2000)
            window2.close()

    if history_list[-1]['state'] != values['-ML2-']:
        history_list.append({
            'timestamp': time.time(),
            'state': values['-ML2-']
        })

    if event == 'Cancel':
        break

    # Update right-hand side from left-hand side
    left_text = values['-ML1-']
    window['-ML2-'].update(left_text)

    # Input use
    current_input = values['-ML1-']
    if current_input != prev_input:
        print("Input changed: ", current_input)
        prev_input = current_input

    # Cursor use
    cursor_position = window['-ML1-'].Widget.index('insert')
    if cursor_position != prev_cursor_position:
        print("Cursor position changed: ", cursor_position)
        prev_cursor_position = cursor_position

    # Mouse use
    mouse_position = window['-ML1-'].Widget.winfo_pointerxy()
    if mouse_position != prev_mouse_position:
        print("Mouse position changed: ", mouse_position)
        prev_mouse_position = mouse_position

    # Check if any input is ready to be shown

window.close()

print(history_list)

copy_paste_list = []

# Find the time it takes for the first 5 letters to be typed

time_difference = 0
start_time = None

for i in range(1, len(history_list)):
    if len(history_list[i]['state']) - len(history_list[i-1]['state']) > 10:
        copy_paste_length = len(history_list[i]['state']) - len(history_list[i-1]['state'])
        copy_paste_found = False
        for j in range(len(history_list[i-1]['state'])):
            if history_list[i-1]['state'][:j] == history_list[i]['state'][:j]:
                continue
            else:
                copied_text = history_list[i]['state'][j-1:j-1+copy_paste_length]
                print("Before: " + history_list[i]['state'][j-1])
                print("Copied: " + copied_text)
                print("After: " + history_list[i]['state'][j-1+copy_paste_length])
                copy_paste_found = True
                break
        if not copy_paste_found:
            print("Cheating detected! Timestamp difference:", history_list[i]['timestamp'] - history_list[i-1]['timestamp'])
            print("The following was copy pasted: " + history_list[i]['state'][len(history_list[i-1]['state']):])
    else:
        print("No cheating detected. State:", history_list[i]['state'])
    if (len(history_list)>5):
        time_difference = history_list[i-4]['timestamp'] - history_list[i]['timestamp']
        if time_difference > 10:
            print("Cheating detected! Time taken:", time_difference)
    