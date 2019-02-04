
from tkinter import *

def foo(event):
    print("Event:", event)

root = Tk()
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

board_frame = Frame(root)
board_frame.grid(row=0, column=0, sticky=N+S+E+W)

buttons = []

# Board has 4 rows and 4 cols, configure them all with weight=1
for i in range(4):
    board_frame.rowconfigure(i, weight=1)
    board_frame.columnconfigure(i, weight=1)

fgs = ["black", "white"]
bgs = ["#F8D193", "#131313"]
c = 0

# Add
for i in range(4):
    c ^= 1
    for j in range(4):
        b = Label(board_frame, text=str(i*4+j), fg=fgs[c], bg=bgs[c])
        c ^= 1
        b.grid(row=i, column=j, sticky=N+S+E+W)
        b.bind("<Button-1>", foo)
        buttons.append(b)

root.mainloop()




"""





from tkinter import *

#Create & Configure root 
root = Tk()
Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)

#Create & Configure frame 
frame=Frame(root)
frame.grid(row=0, column=0, sticky=N+S+E+W)

for i in range(4):
    frame.rowconfigure(i, weight=1)
    frame.columnconfigure(i, weight=1)

#Create a 5x10 (rows x columns) grid of buttons inside the frame
for row_index in range(4):
    for col_index in range(4):
        btn = Button(frame) #create a button inside frame 
        btn.grid(row=row_index, column=col_index, sticky=N+S+E+W)  

root.mainloop()
"""