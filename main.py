import tkinter as tk
import pInstance as pi
import pCreate as pc

root = tk.Tk()

root.title("llm-update")

root.geometry("1000x800")

name_var=tk.StringVar()
query_var=tk.StringVar()

global_fact_list = []

p = pi.plInstance("master", "./kb.pl", save=False)
original_database = str(p)

# defining a function that will
# get the name and password and 
# print them on the screen
def get_content():
 
    name=name_var.get()
    statements=statements_entry.get("1.0", "end-1c")
     
    #print("Username : " + name)
    #print("Statements : " + statements)

    p.set_user(name)
    # Sample input
    input_statements = "\nUsername: " + name + "\nInput:\n"+statements

    test, _ = pc.create_new_facts(input_statements, "./kb.pl")
    tst_string = ""
    for item in test:
        tst_string = tst_string + item + ".\n"

    output_entry.delete("1.0", tk.END)
    output_entry.insert(tk.END, tst_string.strip())

def add_to_database():
    fact_str = output_entry.get("1.0", "end-1c")
    fact_str = fact_str.replace(".", "")
    facts = fact_str.split("\n")
    while '' in facts:
        facts.remove('')

    output_entry.delete('1.0', tk.END)
    for fact in facts:
        global_fact_list.append(fact)
        new_entry.insert(tk.END, fact + "\n")
        p.assert_fact(fact)

def query_pl():
    q=query_var.get()
    if q == "":
        return
    result = p.query(q, recent=False)
    result_entry.delete("1.0", tk.END)
    if type(result) == list:
        for item in result:
            item_str = str(item)
            result_entry.insert(tk.END, item_str + "\n")
    else:
        result_str = str(result)
        result_entry.insert(tk.END, result_str + "\n")

def query_recent():
    q=query_var.get()
    if q == "":
        return
    result = p.query(q, recent=True)
    result_entry.delete("1.0", tk.END)
    if type(result) == list:
        for item in result:
            item_str = str(item)
            result_entry.insert(tk.END, item_str + "\n")
    else:
        result_str = str(result)
        result_entry.insert(tk.END, result_str + "\n")

def reset():
    for fact in global_fact_list:
        p.retract(fact)

    name_var.set("")
    query_var.set("")
    statements_entry.delete("1.0", tk.END)
    output_entry.delete("1.0", tk.END)
    new_entry.delete("1.0", tk.END)
    result_entry.delete("1.0", tk.END)


# creating a label for 
# description using widget Label
description_label = tk.Label(root, text = 'Description', font=('calibre',14, 'bold'))

# creating description using widget Label 
description_text = tk.Label(root, text = """Input a username and a list of statements to generate into prolog statements.""", font=('calibre',14, 'bold'))

clear_btn=tk.Button(root,text = 'Clear', command = reset)

# creating a label for 
# name using widget Label
name_label = tk.Label(root, text = 'Username', font=('calibre',14, 'bold'))
  
# creating a entry for input
# name using widget Entry
name_entry = tk.Entry(root, textvariable=name_var, font=('calibre',14,'normal'))
  
# creating a label for statements
statements_label = tk.Label(root, text = 'Statements', font = ('calibre',14,'bold'))
  
# creating a textbox for statements
statements_entry=tk.Text(root, height = 5, font = ('calibre',14,'normal'))

# creating a scrollbar for statement
scroll = tk.Scrollbar(root) 
statements_entry.configure(yscrollcommand=scroll.set) 
scroll.config(command=statements_entry.yview) 
  
# creating a button using the widget 
# Button that will call the generate_content function 
sub_btn=tk.Button(root,text = 'Generate', command = get_content)

# creating a label for output
output_label = tk.Label(root, text = 'Prolog Output', font = ('calibre',14,'bold'))
  
# creating a textbox for output
output_entry=tk.Text(root, height = 5, font = ('calibre',14,'normal'))

# creating a scrollbar for output
output_scroll = tk.Scrollbar(root) 
output_entry.configure(yscrollcommand=output_scroll.set) 
output_scroll.config(command=output_entry.yview) 

# creating a button using the widget 
# Button that will call the add_to_database function 
app_btn=tk.Button(root,text = 'Add to Database', command = add_to_database)

# creating a label for output
kb_label = tk.Label(root, text = 'Original KB', font = ('calibre',14,'bold'))

# creating a textbox for output
kb_entry=tk.Text(root, height = 10, font = ('calibre',14,'normal'))
kb_entry.insert(tk.END, original_database)
kb_entry.config(state=tk.DISABLED)

# creating a scrollbar for output
kb_scroll = tk.Scrollbar(root) 
kb_entry.configure(yscrollcommand=kb_scroll.set) 
kb_scroll.config(command=kb_entry.yview) 

# creating a label for output
new_label = tk.Label(root, text = 'Added Prolog', font = ('calibre',14,'bold'))

# creating a textbox for output
new_entry=tk.Text(root, height = 5, font = ('calibre',14,'normal'))

# creating a scrollbar for output
new_scroll = tk.Scrollbar(root) 
new_entry.configure(yscrollcommand=new_scroll.set) 
new_scroll.config(command=new_entry.yview) 

# creating a label for output
query_label = tk.Label(root, text = 'Query', font = ('calibre',14,'bold'))

# creating a entry for input
# name using widget Entry
query_entry = tk.Entry(root, textvariable=query_var, font=('calibre',14,'normal'))

# creating a button using the widget 
# Button that will call the add_to_database function 
query_btn=tk.Button(root,text = 'Query', command = query_pl)

# creating a button using the widget 
# Button that will call the add_to_database function 
query_recent_btn=tk.Button(root,text = 'Query Recent', command = query_recent)

# creating a label for output
result_label = tk.Label(root, text = 'Result', font = ('calibre',14,'bold'))

# creating a textbox for output
result_entry=tk.Text(root, height = 5, font = ('calibre',14,'normal'))

# creating a scrollbar for output
result_scroll = tk.Scrollbar(root) 
result_entry.configure(yscrollcommand=result_scroll.set) 
result_scroll.config(command=result_entry.yview) 

  
# placing the label and entry in
# the required position using grid
# method
description_label.grid(row=0,column=0, sticky = "NWE", pady = 2)
description_text.grid(row=0,column=1, sticky = "NWE", pady = 2, padx=20)
clear_btn.grid(row=0,column=2)
name_label.grid(row=1,column=0, sticky = "NWE", pady = 2, padx=20)
name_entry.grid(row=1,column=1, sticky = "NWE", pady = 2)
statements_label.grid(row=2,column=0, sticky = "NWE", pady = 2, padx=20)
statements_entry.grid(row=2,column=1, sticky = "NSWE", pady = 2)
scroll.grid(row=2,column=2, sticky = "NWS", pady = 7)
sub_btn.grid(row=3,column=1)
output_label.grid(row=4,column=0, sticky = "NWE", pady = 2, padx=20)
output_entry.grid(row=4,column=1, sticky = "NWE", pady = 2)
output_scroll.grid(row=4,column=2, sticky = "NWS", pady = 7)
app_btn.grid(row=5,column=1)
kb_label.grid(row=6,column=0, sticky = "NWE", pady = 2, padx=20)
kb_entry.grid(row=6,column=1, sticky = "NWE", pady = 2)
kb_scroll.grid(row=6,column=2, sticky = "NWS", pady = 7)
new_label.grid(row=7,column=0, sticky = "NWE", pady = 2, padx=20)
new_entry.grid(row=7,column=1, sticky = "NWE", pady = 2)
new_scroll.grid(row=7,column=2, sticky = "NWS", pady = 7)
query_label.grid(row=8,column=0, sticky = "NWE", pady = 2, padx=20)
query_entry.grid(row=8,column=1, sticky = "NWE", pady = 2)
query_btn.grid(row=9,column=1)
query_recent_btn.grid(row=10,column=1)
result_label.grid(row=11,column=0, sticky = "NWE", pady = 2, padx=20)
result_entry.grid(row=11,column=1, sticky = "NWE", pady = 2)
result_scroll.grid(row=11,column=2, sticky = "NWS", pady = 7)


root.mainloop()