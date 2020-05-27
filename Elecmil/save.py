from tkinter import *

# Top level window
window = Tk()

# Option menu variable
optionVar = StringVar()
optionVar.set("Red")

# Create a option menu
option = OptionMenu(window, optionVar, "Red", "Blue", "White", "Black")
option.grid()

# Create button with command
def show():
    print("Selected value :", optionVar.get())

btnShow = Button(window, text="Show", command=show)
btnShow.grid()

window.mainloop()

root.mainloop()
