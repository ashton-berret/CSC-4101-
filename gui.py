import tkinter as tk
from parse import *
from lexer import *

def parse_code():
    input_code = code_entry.get("1.0", "end-1c") #gets the code from the textbox 
    tokens = lexer.tokenize(input_code)
    parser = Parser(tokens)
    try:
        parser.run_parser()
        result_label.config(text="Parsing Complete", fg="green")
    except RuntimeError as e:
        result_label.config(text=str(e), fg="red")

root = tk.Tk() #creates main window 
root.title("Code Parser")

code_label = tk.Label(root, text="Enter code:") 
code_label.pack() 

code_entry = tk.Text(root, height=10)
code_entry.pack()

parse_button = tk.Button(root, text="Parse", command=parse_code)
parse_button.pack()

result_label = tk.Label(root, text="") 
result_label.pack() 

root.mainloop() #loop that waits for things like button clicking and updates the gui