from tkinter import *

from main import start_data_mining, movie_recommendation, get_length_itemsets


def start_data_mining_gui():
    start_data_mining(gui_result_area=res_list)


def get_length_itemsets_gui(itemset_length):
    res_list.delete(0, END)
    get_length_itemsets(int(itemset_length), gui_result_area=res_list)


def movie_recommendation_gui():
    pass


# Importing movie list
global movies
movies = list(open("unique.txt").readlines())
brackets = '{}'
movies = [item.translate(brackets).strip() for item in movies]

global resmovies
resmovies = []
global param
param = []

home = Tk()
home.title("Movie Recommender - by IVAP")
home.iconbitmap("GUI\icon.ico")
home.geometry('1250x750+0+0')
home.configure(bg="#4a7fbe")

textspace = LabelFrame(home, bg="#4a7fbe", bd=0)
textspace.pack(pady=30)
ttl = Label(
    textspace,
    text="Movie Recommender",
    bg="#4a7fbe",
    fg="#FFFFFF",
    font=("Times New Roman", int(55.0), 'bold'))
ttl.grid(column=0, row=0)
sub = Label(
    textspace,
    text="What will you watch today? Tell us a movie that you like, and we'll suggest you something nice",
    bg="#4a7fbe",
    fg="#000000",
    font=("Times New Roman", int(22.0), 'bold', 'italic'))
sub.grid(column=0, columnspan=2, row=1)
start = Button(
    textspace,
    text="Start Mining",
    font=("Times New Roman", int(15.0), "bold"),
    fg="#000000",
    bg="#FFFFFF",
    pady=2,
    padx=2,
    command=lambda: start_data_mining_gui())
start.grid(column=1, row=0)

errors = LabelFrame(home, bd=0)
errors.pack()
searchbar = LabelFrame(home, bg="#FFFFFF", bd=0)
searchbar.pack()

maxl = 700
instructions = Label(
    searchbar,
    text="You can get a movie suggestion based on the desired length of the itemset or based on a title",
    bg="#FFFFFF",
    fg="#000000",
    font=("Times New Roman", int(15.0)),
    pady=20,
    wraplength=maxl)
instructions.grid(row=0, column=0, columnspan=2)


# FUNCTIONS
def lookup(*arg):
    conf.config(state=DISABLED)
    resmovies = list(movie_recommendation_gui(';'.join(param)))


# Update the listbox
def update(data):
    my_list.delete(0, END)
    for item in data:
        my_list.insert(END, item)


# Update entry box with listbox clicked
def fillandsend(e):
    intitle.delete(0, END)
    intitle.insert(0, my_list.get(ANCHOR))
    param.append(my_list.get(ANCHOR))
    searching.config(text=param)


# Create function to check entry vs listbox
def check(e):
    typed = intitle.get()
    if typed == '':
        data = movies
    else:
        data = []
        for item in movies:
            if typed.lower() in item.lower():
                data.append(item)
    update(data)


def cancel():
    # res_list.delete(0, END)
    intitle.delete(0, END)
    itset.delete(0, END)
    searching.config(text="")
    param[:] = []


def resupdate(data):
    # Clear the listbox
    res_list.delete(0, END)
    # Add to listbox
    for item in data:
        res_list.insert(END, item)


def reset():
    res_list.delete(0, END)
    # intitle.delete(0, END)
    searching.config(text="")
    param[:] = []
    conf.config(state=ACTIVE)


# Searchbar Elements
sbar = LabelFrame(searchbar, bg="#FFFFFF", bd=0)
sbar.grid(row=1, column=0, padx=5, pady=5)
in_set_len = Label(
    sbar,
    text="Length of the Itemset to visualize",
    font=("Times New Roman", int(10.0)),
    width=30,
    bg="#FFFFFF")
in_set_len.grid(row=0, column=0, padx=5)
itset = Entry(
    sbar,
    font=("Times New Roman", int(10.0)),
    width=10,
    bg="#4a7fbe")
itset.insert(END, '1')
itset.grid(row=0, column=1, padx=5, pady=5)
conf_itemset = Button(
    sbar,
    text="Confirm",
    font=("Times New Roman", int(10.0)),
    width=10,
    bg="#4a7fbe",
    command=lambda: get_length_itemsets_gui(itset.get()))
conf_itemset.grid(row=0, column=2, padx=2)
intitle = Entry(
    sbar,
    width=30,
    bg="#FFFFFF",
    font=("Times New Roman", int(10.0)))
intitle.insert(END, 'Select a movie from the list')
intitle.grid(row=1, column=0, padx=2)
btnclear = Button(
    sbar,
    text="Clear",
    font=("Times New Roman", int(10.0)),
    width=10,
    bg="#FFFFFF",
    command=cancel)
btnclear.grid(row=1, column=1, padx=2)
conf = Button(
    sbar,
    text="Confirm",
    font=("Times New Roman", int(10.0)),
    width=10,
    bg="#FFFFFF",
    command=lookup)
conf.grid(row=1, column=2, padx=2)

# Create a listbox in a frame to use the scrollbar
listcontainer = LabelFrame(searchbar)
listcontainer.grid(row=2, column=0, pady=5)
# scrollbar
barleft = Scrollbar(listcontainer, orient=VERTICAL)
barleft.pack(side=RIGHT, fill=Y)

my_list = Listbox(
    listcontainer,
    font=("Times New Roman", int(10.0)),
    width=60,
    bd=0,
    yscrollcommand=barleft)
my_list.pack()
barleft.config(command=my_list.yview)
# list features
update(movies)
my_list.bind("<<ListboxSelect>>", fillandsend)
intitle.bind("<KeyRelease>", check)

# Research results header
query = LabelFrame(searchbar, bd=0, bg="#FFFFFF")
query.grid(row=1, column=1)
info = Label(
    query,
    text="Your results: ",
    font=("Times New Roman", int(10.0)),
    bg="#FFFFFF")
info.grid(row=0, column=0)
searching = Label(
    query,
    font=("Times New Roman", int(10.0)),
    width=35,
    wraplength=300,
    bg="#FFFFFF")
searching.grid(row=1, column=0)

# scrollbar + result box
results = LabelFrame(searchbar, bd=0)
results.grid(row=2, column=1, padx=20)
sgs = Label(
    results,
    text="We suggest you ",
    bg="#FFFFFF")
info.grid(row=3, column=0)
bar = Scrollbar(results, orient=VERTICAL)
bar.pack(side=RIGHT, fill=Y)
orbar = Scrollbar(results, orient=HORIZONTAL)
orbar.pack(side=BOTTOM, fill=X)
res_list = Listbox(
    results,
    font=("Times New Roman", int(10.0)),
    width=50,
    bg="#FFFFFF",
    yscrollcommand=bar,
    xscrollcommand=orbar)
res_list.pack()
bar.config(command=res_list.yview)
orbar.config(command=res_list.xview)

bottombuttons=LabelFrame(searchbar, bd=0, bg="#FFFFFF")
bottombuttons.grid(row=3, column=1)

# clear results button
clear = Button(
    bottombuttons,
    text="Clear Results",
    font=("Times New Roman", int(10.0)),
    bg="#FFFFFF",
    command=reset)
clear.grid(row=0, column=0, padx=5)

# try new suggestions button
try_again = Button(
    bottombuttons,
    text="Generate new suggestions",
    font=("Times New Roman", int(10.0)),
    bg="#4a7fbe",
    command=reset)
try_again.grid(row=0, column=1, pady=10, padx=5)

home.mainloop()
