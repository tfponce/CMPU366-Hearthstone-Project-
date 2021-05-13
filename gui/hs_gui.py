import os
import random
from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
import tkinter.font as tkFont
from pickle import load
from nltk.util import ngrams

root = Tk()
root.title("Archinator") 
root.iconbitmap("hnet.com-image.ico")
root.geometry("500x519")
fontExample = tkFont.Font(family="Arial", size=10, weight="bold", slant="italic")

#root.config(bg='brown')

my_img1 = ImageTk.PhotoImage(Image.open("start_screen.png"))
my_img2 = ImageTk.PhotoImage(Image.open("card_plus_background.png"))
my_img3 = ImageTk.PhotoImage(Image.open("deck_list_colored.png"))
my_img4 = ImageTk.PhotoImage(Image.open("construction.png"))

# Folder Paths
card_path = "../data/cards/"
deck_path = "../data/decks/cleaner/"

my_ngrams = load(open('../models/ngrams', 'rb'))

my_label = Label(root, image=my_img1)
my_label.pack() # Remember to keep this on a seperate line or else you will get an error

classes = ["demonhunter", "druid", "hunter", "mage", "paladin", "priest", "rogue", "shaman", "warlock", "warrior"]
types = ["spell", "minion", "weapon"]
    
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

def analyze_random_deck():
    deck_list = {}
    deck_size = 0
    deck_size_limit = 30
    random_choice = random.choice(classes)
    
    random_file = card_path + random_choice + ".txt"
    neutral_file = card_path + "neutral.txt" 
    
    random_and_neutral = [random_file, neutral_file]
    
    #os.chdir(card_path)
    
    for item in random_and_neutral:
        with open(item, 'r', encoding='utf-8') as card_file:
            if item == random_file:
                class_cards = card_file.readlines()
            else:
                neutral_cards = card_file.readlines()
    
    class_cards.extend(neutral_cards) # List that contains class and neutral cards
    
    while deck_size < deck_size_limit:
        random_card = random.choice(class_cards)
        values = random_card.split(", '")
        card_name = ""
        card_rarity = ""
        i = 0
        
        while card_name == "" or card_rarity == "":
            if "name': " in values[i]:
                card_name = values[i]
                card_name = card_name.split("name': ")[-1][1:-1]
                #print(card_name)
            elif "rarity" in values[i]:
                #print(values[i])
                card_rarity = values[i]
                
            i += 1
        
        if card_name in deck_list.keys():
            if "LEGENDARY" not in card_rarity and deck_list.get(card_name) < 2:
                updated_entry = {card_name: deck_list.get(card_name) + 1}
                deck_list.update(updated_entry)
                deck_size += 1
        else:
            if "LEGENDARY" not in card_rarity:
                random_number = random.randint(1,2)
                deck_list[card_name] = random_number
                deck_size += random_number
            else:
                deck_list[card_name] = 1
                deck_size += 1
            
    final_list = ""
    
    for entry in deck_list:
        final_list += entry + " : " + str(deck_list.get(entry)) + "\n"
    
    response = messagebox.showinfo("Random " + random_choice.capitalize() + " deck", final_list)
            

def analyze_generated():
    return

def generate_card(Class, mana, Type, attack, health, text_box):
    if mana.get() == "Mana: ":
        mana.insert(END, str(random.randint(1, 10)))
    if Class.get() == "Class: ":
        Class.insert(END, random.choice(classes))
    if Type.get() == "Type: ":
        Type.insert(END, random.choice(types))
    
    extra_info = 0

    inpt_str = Class.get()[7:] + mana.get()[5:] + Type.get()[5:]
    if attack.get() != "Attack: ":
        extra_info += 1

        inpt_str = inpt_str + attack.get()[7:]
        if health.get() != "Health: ":
            extra_info += 1

            inpt_str = inpt_str + health.get()[7:]
    
    if extra_info == 0:
        tokens = inpt_str.lower().split()
    elif extra_info == 1:
        tokens = inpt_str.lower().split()[1:]
    else:
        tokens = inpt_str.lower().split()[2:]

    ngram_size = generation_type.get() + 1

    ngram_dict = {1:[], 2:[], 3:[]} 
    ngram_dict[ngram_size] = list(ngrams(tokens, ngram_size))[-1]

    pred = {1:[], 2:[], 3:[]}
    count = 0
    curNgram = ngram_dict[ngram_size]

    while count < 40:
        for each in my_ngrams[ngram_size+1]:
            if each[0][:-1] == curNgram:

                pred[ngram_size].append(each[0][-1])

                curNgram = curNgram[1:] + (each[0][-1], )

                break

        if len(pred[ngram_size]) == count:
            pred[ngram_size].append(my_ngrams[ngram_size+1][0][0][-1])
            curNgram = curNgram[1:] + (my_ngrams[ngram_size+1][0][0][-1], )
        count +=1
        if curNgram[-1] == "</s>":
            break

    text_box.delete('1.0', END)

    if Type.get()[6:].lower() == "minion" or Type.get()[6:].lower() == "weapon":
        if extra_info == 0 and len(pred[ngram_size]) >= 2:
            # Remove begining attack and health and ending </s> tage and join predicted text
            text = " ".join(pred[ngram_size][2:(len(pred[ngram_size]) - 1)])

            attack_text = pred[ngram_size][0]
            health_text = pred[ngram_size][1]

            attack.insert(END, attack_text)
            health.insert(END, health_text)
        elif extra_info == 1 and len(pred[ngram_size]) >= 1:
            # Remove begining health and ending </s> tage and join predicted text
            text = " ".join(pred[ngram_size][1:(len(pred[ngram_size]) - 1)])

            health_text = pred[ngram_size][0]
            health.insert(END, health_text)
        else:
            # Remove ending </s> tage and join predicted text
            text = " ".join(pred[ngram_size][0:(len(pred[ngram_size]) - 1)])
    else:
        # Remove ending </s> tage and join predicted text
        text = " ".join(pred[ngram_size][0:(len(pred[ngram_size]) - 1)])

    text_box.insert('1.0', text)

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
    
    button_random = Button(root, text="Analyze Random Deck", command=analyze_random_deck)
    button_random.place(x=172, y=20)
    button_random.configure(font=fontExample)
    
    button_card = Button(root, text="Single Card Check", bg='#567', fg='White', command=card_page)
    button_card.place(x=185, y=465)
    button_card.configure(font=fontExample)
    
    button_generate = Button(root, text="Generate A Card", bg='#567', fg='White', command=generate_page)
    button_generate.place(x=382, y=465)
    button_generate.configure(font=fontExample)
    
    text_box = Text(root, height=20, width=25)
    text_box.place(x=160,y=120)
    text_box.configure(font=fontExample)
    
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
    
    button_deck = Button(root, text="Check Deck List", bg='#567', fg='White', command=deck_page)
    button_deck.place(x=5, y=465)
    button_deck.configure(font=fontExample)
    
    button_card = Button(root, text="Analyze Card", command=lambda: 
                                analyze_card(mana,name,attack,health,text_box))
    button_card.place(x=200, y=465)
    button_card.configure(font=fontExample)
    
    button_generate = Button(root, text="Generate A Card", bg='#567', fg='White', command=generate_page)
    button_generate.place(x=382, y=465)
    button_generate.configure(font=fontExample)

def generate_page():
    global my_label
    global button_card
    
    my_label.pack_forget()
    my_label = Label(root, image=my_img2)
    my_label.pack()

    mana = Entry(root, width=10, borderwidth=5)
    mana.insert(0, "Mana: ")
    mana.place(x=105, y=75)

    Class = Entry(root, width=15, borderwidth=5)
    Class.insert(0, "Class: ")
    Class.place(x=125, y=260)

    Type = Entry(root, width=15, borderwidth=5)
    Type.insert(0, "Type: ")
    Type.place(x=265, y=260)

    attack = Entry(root, width=10, borderwidth=5)
    attack.insert(0, "Attack: ")
    attack.place(x=105, y=405)

    health = Entry(root, width=10, borderwidth=5)
    health.insert(0, "Health: ")
    health.place(x=325, y=405)

    text_box = Text(root, height=5, width=24)
    text_box.place(x=170, y=315)
    
    mana.configure(font=fontExample)
    Class.configure(font=fontExample)
    Type.configure(font=fontExample)
    attack.configure(font=fontExample)
    health.configure(font=fontExample)
    text_box.configure(font=fontExample)
    
    button_deck = Button(root, text="Check Deck List", bg='#567', fg='White', command=deck_page)
    button_deck.place(x=5, y=465)
    button_deck.configure(font=fontExample)
    
    button_card = Button(root, text="Single Card Check", bg='#567', fg='White', command=card_page)
    button_card.place(x=165, y=465)
    button_card.configure(font=fontExample)

    button_generate = Button(root, text="Generate Card", command=lambda: 
                                                generate_card(Class,mana,Type,attack,health,text_box))
    button_generate.place(x=202, y=10)
    button_generate.configure(font=fontExample)
    
    button_analyze = Button(root, text="Analyze Generated Card", command=analyze_generated)
    button_analyze.place(x=335, y=465)
    button_analyze.configure(font=fontExample)

button_deck = Button(root, text="Check Deck List", relief="raised", command=deck_page)
button_deck.place(x=5, y=465)
button_deck.configure(font=fontExample)

button_card = Button(root, text="Single Card Check", relief="raised", command=card_page)
button_card.place(x=190, y=465)
button_card.configure(font=fontExample)

button_generate = Button(root, text="Generate A Card", relief="raised", command=generate_page)
button_generate.place(x=382, y=465)
button_generate.configure(font=fontExample)

menubar = Menu(root)
generation_type = IntVar()
generation_type.set(1)

generation_menu = Menu(menubar)
generation_menu.add_radiobutton(label="Bigram",  variable=generation_type, value=0)
generation_menu.add_radiobutton(label="Trigram", variable=generation_type, value=1)
generation_menu.add_radiobutton(label="Fourgram", variable=generation_type, value=2)
menubar.add_cascade(label='Generator', menu=generation_menu)
root.config(menu=menubar)

root.mainloop()