import tkinter as tk
import json
from pathlib import Path

version = '0.1.0'

BASE_DIR = Path(__file__).resolve().parent
JSON_PATH = BASE_DIR / 'data' / 'cost_table.json'

with open(JSON_PATH, encoding='utf-8') as f:
    table = json.load(f)

item1 = None
item2 = None
item3 = None
stage = 1
finished = False

buttons = {}
stage_labels = []

def valid(n):
    if finished:
        return False

    if stage == 1:
        return 8 <= n <= 10
    if stage == 2:
        return 7 <= n <= 11
    if stage == 3:
        return 1 <= n <= 12
    return False


def update_buttons():
    for n, btn in buttons.items():

        if finished:
            btn.config(state='disabled', bg='#dddddd')
            continue

        if valid(n):
            btn.config(state='normal', bg='#ffd966')
        else:
            btn.config(state='disabled', bg='#dddddd')


def press(n):
    global item1, item2, item3, stage, finished

    if not valid(n):
        return

    if stage == 1:
        item1 = n
        stage = 2

    elif stage == 2:
        item2 = n
        stage = 3

    elif stage == 3:
        item3 = n
        stage = 1

        data = table[str(item1)][str(item2)][str(item3)]

        if data['remainder'] == 0:
            stack_text = f"{data['stacks']}s"
        else:
            stack_text = f"{data['stacks']}s + {data['remainder']}"

        result.set(
            f"{data['cost']}\n{stack_text}"
        )

        finished = True

    update_display()
    update_buttons()


def undo():
    global item1, item2, item3, stage, finished

    if finished:
        finished = False
        item3 = None
        stage = 3

    elif item3 is not None:
        item3 = None
        stage = 3

    elif item2 is not None:
        item2 = None
        stage = 2

    elif item1 is not None:
        item1 = None
        stage = 1

    result.set('')
    update_display()
    update_buttons()


def clear():
    global item1, item2, item3, stage, finished

    item1 = None
    item2 = None
    item3 = None

    stage = 1
    finished = False

    result.set('')
    update_display()
    update_buttons()


def update_stage_indicator():
    for i, lbl in enumerate(stage_labels):

        if finished:
            lbl.config(bg='#dddddd')

        elif stage == i + 1:
            lbl.config(bg='#ffd966')

        else:
            lbl.config(bg='#f0f0f0')


def update_display():
    display.set(f"{item1 or '_'} × {item2 or '_'} × {item3 or '_'}")
    update_stage_indicator()


root = tk.Tk()
root.title('books not calc')
root.resizable(False, False)

display = tk.StringVar()
result = tk.StringVar()

update_display()



tk.Label(root, textvariable=display, font=('Arial',14)).grid(
    row=1, column=0, columnspan=4, pady=(10,5)
)

tk.Frame(root, height=2, bg='black').grid(
    row=2, column=0, columnspan=4, sticky='ew', padx=10, pady=5
)

stage_frame = tk.Frame(root)
stage_frame.grid(row=0, column=0, columnspan=4, pady=(10,5))

item_names = ['emr cost', 'eye cost', 'need eyes']

for i in range(3):
    lbl = tk.Label(
        stage_frame,
        text=item_names[i],
        width=10,
        font=('Roboto', 8),
        relief='solid',
        bd=1
    )
    lbl.grid(row=0, column=i, padx=2)
    stage_labels.append(lbl)

update_stage_indicator()


tk.Label(
    root,
    textvariable=result,
    font=('Arial',14),
    height=2,
    width=12
).grid(row=3, column=0, columnspan=4, pady=5)


numbers = [
    [10,11,12],
    [7,8,9],
    [4,5,6],
    [1,2,3]
]

for r, row in enumerate(numbers):
    for c, n in enumerate(row):

        btn = tk.Button(
            root,
            font=('Consolas', 10),
            text=str(n),
            width=6,
            height=2,
            command=lambda x=n: press(x)
        )

        btn.grid(row=r+4, column=c)
        buttons[n] = btn


tk.Button(
    root,
    font=('Consolas', 10),
    text='←',
    width=6,
    height=2,
    command=undo
).grid(row=4, column=3, columnspan=1, sticky='ns')


tk.Button(
    root,
    font=('Consolas', 10),
    text='C',
    width=6,
    height=2,
    command=clear
).grid(row=5, column=3, rowspan=3, sticky='ns')


update_buttons()

root.mainloop()