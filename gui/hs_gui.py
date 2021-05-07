from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
import tkinter.font as tkFont

root = Tk()
root.title("Hearthstone GUI") # Name to be decided on later
root.iconbitmap("hnet.com-image.ico")
root.geometry("500x500")
fontExample = tkFont.Font(family="Arial", size=10, weight="bold", slant="italic")

#root.config(bg='brown')

my_img1 = ImageTk.PhotoImage(Image.open("start_screen.png"))
my_img2 = ImageTk.PhotoImage(Image.open("card_plus_background.png"))
my_img3 = ImageTk.PhotoImage(Image.open("deck_list_colored.png"))
my_img4 = ImageTk.PhotoImage(Image.open("construction.png"))

my_label = Label(root, image=my_img1)
my_label.pack() # Remember to keep this on a seperate line or else you will get an error
    
def analyze_card(mana, name, attack, health, text_box):
    #print("text stuff: " + str(type(text_box.get("1.0",END))) + "END")
    card_text = text_box.get("1.0",END)
    if mana.get() == "Mana: " or name.get() == "Name: " or attack.get() == "Attack: " or health.get() == "Health: ":
        #button_analyze_card = Button(root, text="Analyze Card", state=DISABLED)
        response = messagebox.showwarning("Missing Info!", "Fill out all of the card info!")
    else:
        if card_text == "\n":
            card_text = "VANILLA" 
        # This is where we need to write the code that actually analyzes the card 
    
def analyze_deck():
    return

def analyze_generated():
    return
    
def deck_page():
    global my_label
    global button_card
    global button_generate
    
    my_label.pack_forget()
    my_label = Label(root, image=my_img3)
    my_label.pack()
    
    button_deck = Button(root, text="Analyze Deck", command=analyze_deck)
    button_deck.place(x=5, y=465)
    button_deck.configure(font=fontExample)
    
    button_card = Button(root, text="Single Card Check", command=card_page)
    button_card.place(x=180, y=465)
    button_card.configure(font=fontExample)
    
    button_generate = Button(root, text="Generate A Card", command=generate_page)
    button_generate.place(x=382, y=465)
    button_generate.configure(font=fontExample)
    
def card_page():
    global my_label
    global button_deck
    global button_generate
    global button_card
    
    my_label.pack_forget()
    my_label = Label(root, image=my_img2)
    my_label.pack()
    
    mana = Entry(root, width=10, borderwidth=5)
    mana.insert(0, "Mana: ")
    mana.place(x=105, y=75)

    name = Entry(root, width=35, borderwidth=5)
    name.insert(0, "Name: ")
    name.place(x=125, y=260)

    attack = Entry(root, width=10, borderwidth=5)
    attack.insert(0, "Attack: ")
    attack.place(x=105, y=405)

    health = Entry(root, width=10, borderwidth=5)
    health.insert(0, "Health: ")
    health.place(x=325, y=405)

    text_box = Text(root, height=5, width=24)
    text_box.place(x=170, y=315)
    
    mana.configure(font=fontExample)
    name.configure(font=fontExample)
    attack.configure(font=fontExample)
    health.configure(font=fontExample)
    text_box.configure(font=fontExample)
    
    button_deck = Button(root, text="Check Deck List", command=deck_page)
    button_deck.place(x=5, y=465)
    button_deck.configure(font=fontExample)
    
    button_card = Button(root, text="Analyze Card", command=lambda: 
                                analyze_card(mana,name,attack,health,text_box))
    button_card.place(x=200, y=465)
    button_card.configure(font=fontExample)
    
    button_generate = Button(root, text="Generate A Card", command=generate_page)
    button_generate.place(x=382, y=465)
    button_generate.configure(font=fontExample)

def generate_page():
    global my_label
    global button_card
    global button_generate
    
    my_label.pack_forget()
    my_label = Label(root, image=my_img4)
    my_label.pack()
    
    button_deck = Button(root, text="Check Deck List", command=deck_page)
    button_deck.place(x=5, y=465)
    button_deck.configure(font=fontExample)
    
    button_card = Button(root, text="Single Card Check", command=card_page)
    button_card.place(x=165, y=465)
    button_card.configure(font=fontExample)
    
    button_generate = Button(root, text="Analyze Generated Card", command=analyze_generated)
    button_generate.place(x=335, y=465)
    button_generate.configure(font=fontExample)

button_deck = Button(root, text="Check Deck List", relief="raised", command=deck_page)
button_deck.place(x=5, y=465)
button_deck.configure(font=fontExample)

button_card = Button(root, text="Single Card Check", relief="raised", command=card_page)
button_card.place(x=190, y=465)
button_card.configure(font=fontExample)

button_generate = Button(root, text="Generate A Card", relief="raised", command=generate_page)
button_generate.place(x=382, y=465)
button_generate.configure(font=fontExample)

root.mainloop()