import os
import nltk
import random
from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
import tkinter.font as tkFont
from pickle import load
from nltk.util import ngrams
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import numpy as np

root = Tk()
root.title("Archinator") 
root.iconbitmap("hnet.com-image.ico")
root.geometry("500x519")
fontExample = tkFont.Font(family="Arial", size=10, weight="bold", slant="italic")

my_img1 = ImageTk.PhotoImage(Image.open("start_screen.png"))
my_img2 = ImageTk.PhotoImage(Image.open("card_plus_background.png"))
my_img3 = ImageTk.PhotoImage(Image.open("deck_list_colored.png"))
# my_img4 = ImageTk.PhotoImage(Image.open("construction.png"))  

# Folder Paths
card_path = "../data/cards/"
deck_path = "../data/decks/cleaner/"

my_ngrams = load(open('../models/ngrams', 'rb'))
my_lstm = load_model('../models/model.h5')
my_tokenizer = load(open('../models/tokenizer.pkl', 'rb'))

my_label = Label(root, image=my_img1)
my_label.pack() # Remember to keep this on a seperate line or else you will get an error

choices = {"Demon Hunter", "Druid", "Hunter", "Mage", "Neutral", "Paladin", "Priest", "Rogue", "Shaman", "Warlock", "Warrior"}
classes = ["demonhunter", "druid", "hunter", "mage", "paladin", "priest", "rogue", "shaman", "warlock", "warrior"]
types = ["spell", "minion", "weapon"]
choose = {"HERO", "SPELL", "MINION", "WEAPON"}

# This is only used for the generate section 
first_push = 0  

# We are generating random decks from all expansions
deck_format = "'Format': 'Wild', "  
deck_size_limit = 30

# Dictionaries for different card attributes
# The key is the card's name and the value is the specific attribute
card_type = {}
card_class = {}
card_mana = {}
card_rarity = {}
card_text = {} # Modified card text that is without special symbols
card_text2 = {} # Exact card text that came from our data
card_attack = {}
card_health = {}

aggressive_decks = deck_path + "AggroDecks.txt"
combo_decks = deck_path + "ComboDecks.txt"
control_decks = deck_path + "ControlDecks.txt"
midrange_decks = deck_path + "MidrangeDecks.txt"

def gen_feats(deck):
        features = {}
        for d in deck:
            features["contains-" + d.lower()] = 1
        return features
    
def gen_card_info(deck, arch):
    d_list = []
    for d in deck:
        cards = d.replace("': ", " : ")
        cards = cards.split(", '")
        length = len(cards)
        d_string = cards[0][1:] + ", " + cards[1] + ", " 
        i = 2
        
        if length > 5:
            while i < length:
                cname = str(cards[i].split(" : ")[0])
                c = "Name : " + cname + ", "
                m = "Mana : " + str(card_mana.get(cname)) + ", "
                t = "Text : " + str(card_text.get(cname)) + ", "
                a = "Attack : " + str(card_attack.get(cname)) + ", "
                h = "Health : " + str(card_health.get(cname)) + ", "
                d_string += c + m + t + a + h
                i += 1
                
            d_list.append(d_string[:-1])
        
    tok_list = [(nltk.word_tokenize(x), arch) for x in d_list]
    return tok_list
            
def native_bayes_classifier(): 
    global whatarch  
    global cardarch
    
    deck_archetypes = [aggressive_decks, combo_decks, control_decks, midrange_decks]

    aggro, combo, control, mid = "", "", "", ""

    for deck in deck_archetypes:
        with open(deck, 'r') as d:
            if deck == aggressive_decks:
                aggro = [(nltk.word_tokenize(x[0:-1]), "aggro") for x in d if len(x) > 100] 
                d.seek(0) # Start of the file
                c_aggro = d.readlines()
                c_aggro = gen_card_info(c_aggro, "aggro")
            elif deck == combo_decks:
                combo = [(nltk.word_tokenize(x[0:-1]), "combo") for x in d if len(x) > 100]
                d.seek(0)
                c_combo = d.readlines()
                c_combo = gen_card_info(c_combo, "combo")
            elif deck == control_decks:
                control = [(nltk.word_tokenize(x[0:-1]), "control") for x in d if len(x) > 100]
                d.seek(0)
                c_control = d.readlines()
                c_control = gen_card_info(c_control, "control")
            else:
                mid = [(nltk.word_tokenize(x[0:-1]), "mid") for x in d if len(x) > 100]
                d.seek(0)
                c_mid = d.readlines()
                c_mid = gen_card_info(c_mid, "mid")
                
    arch_decks = [*aggro, *combo, *control, *mid] # Join lists
    card_decks = [*c_aggro, *c_combo, *c_control, *c_mid] # Join lists
    random.Random(10).shuffle(arch_decks)
    random.Random(10).shuffle(card_decks)

    # Partitioning
    test_archdecks = [x for x in arch_decks[0:200]]  
    devtest_archdecks = [x for x in arch_decks[200:400]]  
    train_archdecks = [x for x in arch_decks[400:]]
    
    ctest_archdecks = [x for x in card_decks[0:200]]  
    cdevtest_archdecks = [x for x in card_decks[200:400]]  
    ctrain_archdecks = [x for x in card_decks[400:]]    

    # Generating feature sets
    test_feats = [(gen_feats(d), c)  for (d,c) in test_archdecks]  
    devtest_feats = [(gen_feats(d), c) for (d,c) in devtest_archdecks]  
    train_feats = [(gen_feats(d), c) for (d,c) in train_archdecks] 
    
    ctest_feats = [(gen_feats(d), c)  for (d,c) in ctest_archdecks]  
    cdevtest_feats = [(gen_feats(d), c) for (d,c) in cdevtest_archdecks]  
    ctrain_feats = [(gen_feats(d), c) for (d,c) in ctrain_archdecks]
    
    # Training...
    whatarch = nltk.NaiveBayesClassifier.train(train_feats)  
    cardarch = nltk.NaiveBayesClassifier.train(ctrain_feats)  

    # Testing...
    accuracy = nltk.classify.accuracy(whatarch, test_feats)
    accuracy2 = nltk.classify.accuracy(cardarch, ctest_feats)  
    #print("Accuracy score: ", accuracy)
    #print("Accuracy score: ", accuracy2)

    # aa: real deck aggro, guessed aggro
    # ao: real deck aggro, guessed combo
    # ac: real deck aggro, guessed control
    # am: real deck aggro, guessed mid

    # oo: real deck combo, guessed combo
    # oa: real deck combo, guessed aggro
    # oc: real deck combo, guessed control
    # om: real deck combo, guessed mid

    # cc: real deck control, guessed control
    # ca: real deck control, guessed aggro
    # co: real deck control, guessed combo
    # cm: real deck control, guessed mid

    # mm: real deck mid, guessed mid
    # ma: real deck mid, guessed aggro
    # mc: real deck mid, guessed control
    # mo: real deck mid, guessed combo
    """ aa, ao, ac, am = [], [], [], [] 
    oo, oa, oc, om = [], [], [], [] 
    cc, ca, co, cm = [], [], [], []
    mm, ma, mc, mo = [], [], [], []
    for (deck, auth) in cdevtest_archdecks:
        guess = whatarch.classify(gen_feats(deck))
        if auth == "aggro" and guess == "aggro":
            aa.append((auth, guess, deck))
        elif auth == "aggro" and guess == "combo":
            ao.append((auth, guess, deck))
        elif auth == "aggro" and guess == "control":
            ac.append((auth, guess, deck))
        elif auth == "aggro" and guess == "mid":
            am.append((auth, guess, deck))
        elif auth == "combo" and guess == "combo":
            oo.append((auth, guess, deck))
        elif auth == "combo" and guess == "aggro":
            oa.append((auth, guess, deck))
        elif auth == "combo" and guess == "control":
            oc.append((auth, guess, deck))
        elif auth == "combo" and guess == "mid":
            om.append((auth, guess, deck))
        elif auth == "control" and guess == "control":
            cc.append((auth, guess, deck))
        elif auth == "control" and guess == "aggro":
            ca.append((auth, guess, deck))
        elif auth == "control" and guess == "combo":
            co.append((auth, guess, deck))
        elif auth == "control" and guess == "mid":
            cm.append((auth, guess, deck))
        elif auth == "mid" and guess == "mid":
            mm.append((auth, guess, deck))
        elif auth == "mid" and guess == "aggro":
            ma.append((auth, guess, deck))
        elif auth == "mid" and guess == "combo":
            mo.append((auth, guess, deck))
        elif auth == "mid" and guess == "control":
            mc.append((auth, guess, deck))
            
    auth_guess_list = [aa, ao, ac, am, oo, oa, oc, om, cc, ca, co, cm, mm, ma, mc, mo]
    for x in auth_guess_list:
        if len(x) > 0:  
            auth, guess, deck = random.choice(x)
            print("real=%-8s guess=%-8s" % (auth, guess))
            print(" ".join(deck))
            print("-------")
        else:
            print("No guesses were made for this list")
            print("-------")
    print() """ 

    #whatarch.show_most_informative_feats_all(40)
    #cardarch.show_most_informative_feats_all(40)
    
def card_library_creator():
    classes_and_neutral = classes + ["neutral"]
    for c in classes_and_neutral:
        class_file = card_path + c + ".txt"
        with open(class_file, "r", encoding="utf8") as cf:
            cards = cf.readlines()
            for x in cards:
                values = x.replace("': ", " : ")
                values = values.split(", '")
                name = ""
                cardclass = ""
                rarity = ""
                cardtype = ""
                mana = ""
                text = ""
                text2 = ""
                attack = ""
                health = ""
        
                for v in values:
                    if "name : " in v:
                        name = v
                        name = name.split(" : ")[-1][1:-1]
                    elif "cardClass : " in v:
                        cardclass = v
                        cardclass = cardclass.split(" : ")[-1][1:-1]
                        if cardclass == "DEMONHUNTER":
                            cardclass = "Demon Hunter"
                        else:
                            cardclass = cardclass.lower().capitalize()
                    elif "rarity : " in v:
                        rarity = v
                        rarity = rarity.split(" : ")[-1][1:-1]
                    elif "cost : " in v:
                        mana = v
                        mana = mana.split(" : ")[-1]
                    elif "text : " in v:
                        text2 = v
                        text2 = text2.split(" : ")[-1][1:-1]
                        text = text2.replace("<b>", "").replace("</b>", "")
                    elif "attack : " in v:
                        attack = v
                        attack = attack.split(" : ")[-1]
                    elif "health : " in v:
                        health = v
                        health = health.split(" : ")[-1]
                    elif "type : " in v:
                        cardtype = v
                        cardtype = cardtype.split(" : ")[-1][1:-1]
                        
                card_type[name] = cardtype
                card_class[name] = cardclass
                card_mana[name] = mana
                card_rarity[name] = rarity
                card_text[name] = text
                card_text2[name] = text2
                card_attack[name] = attack
                card_health[name] = health

def deck_classification(deck, classifier):
    tokenized_deck = gen_feats(nltk.word_tokenize(deck))
    classify_deck = classifier.classify(tokenized_deck).upper()
    
    newline = "\n"
    
    str_classify = "The best archetype for this is: " + classify_deck + "\n"
    line = "-------------------------------------------------------\n"
    
    aggro_prob = classifier.prob_classify(tokenized_deck).prob('aggro')
    combo_prob = classifier.prob_classify(tokenized_deck).prob('combo')
    control_prob = classifier.prob_classify(tokenized_deck).prob('control')
    mid_prob = classifier.prob_classify(tokenized_deck).prob('mid')
    
    str_aggro = "P(Aggro | Deck) = " + str(aggro_prob) + "\n"
    str_combo = "P(Combo | Deck) = " + str(combo_prob) + "\n"
    str_control = "P(Control | Deck) = " + str(control_prob) + "\n"
    str_mid = "P(Midrange | Deck) = " + str(mid_prob) + "\n"
    
    display = newline + str_classify + line + str_aggro + str_combo + str_control + str_mid
    
    return display

def analyze_card(mana, name, attack, health, text_box, tkvar, var):
    cardtext = text_box.get("1.0",END)
    cardclass = tkvar.get()
    cardtype = var.get()
    
    if cardclass == "Pick a class":
        messagebox.showerror("Missing Info!", "Please select a class for your card.")
        return
    elif cardtype == "Pick a type":
        messagebox.showerror("Missing Info!", "Please select a type for your card.")
        return
    
    if cardtype == "HERO":
        if mana.get() == "Mana: " or name.get() == "Name: " or health.get() == "Health: ":
            messagebox.showwarning("Missing Info!", "Fill out all of the card info! \n" + 
                                   "The attack section should be empty.")
            return
        elif attack.get() != "Attack: ":
            messagebox.showwarning("Remove Info!", "Please remove info! \n" + 
                                   "The attack section should be empty.")
            return
    elif cardtype == "MINION": 
        if mana.get() == "Mana: " or name.get() == "Name: " or attack.get() == "Attack: " or health.get() == "Health: ":
            messagebox.showwarning("Missing Info!", "Fill out all of the card info! \n" + 
                                "The card text section is optional.")
            return
    elif cardtype == "SPELL":
        if mana.get() == "Mana: " or name.get() == "Name: ":
            messagebox.showwarning("Missing Info!", "Fill out all of the card info! \n" + 
                                   "The attack and health section should be empty.")
            return
        elif attack.get() != "Attack: " or health.get() != "Health: ":
            messagebox.showwarning("Remove Info!", "Please remove info! \n" + 
                                   "The attack and health section should be empty.")
            return
    else: 
        if mana.get() == "Mana: " or name.get() == "Name: " or attack.get() == "Attack: " or health.get() == "Health: ":
            messagebox.showwarning("Missing Info!", "Fill out all of the card info! \n" + 
                                "The card text section is optional.")
            return
    
    n = "Name : " + name.get().replace("Name: ", "") + ", "
    n_d = "Name : " + name.get().replace("Name: ", "") + "\n"
    m = "Mana : " + mana.get().replace("Mana: ", "") + ", "
    m_d = "Mana : " + mana.get().replace("Mana: ", "") + "\n"
    t = "Text : " + cardtext + ", "
    t_d = "Text : " + cardtext + "\n"
    a = "Attack : " + attack.get().replace("Attack: ", "") + ", "
    a_d = "Attack : " + attack.get().replace("Attack: ", "") + "\n"
    h = "Health : " + health.get().replace("Health: ", "") + ", "
    h_d = "Health : " + health.get().replace("Health: ", "") + "\n"
    cf = "Class : " + cardclass + ", " + deck_format + ", "
    cf_d = "Class : " + cardclass + "\n" + deck_format + "\n"
    
    card_to_analyze = cf + n + m + t + a + h
    card_to_display = cf_d + n_d + m_d + t_d + a_d + h_d
    
    display = deck_classification(card_to_analyze, cardarch)

    card_to_display += display
    
    messagebox.showinfo("Your " + cardclass + " deck", card_to_display)
    
    
def analyze_deck(text_box, tkvar):
    if tkvar.get() == "Pick a class":
        messagebox.showerror("Missing Info!", "Please select a class for your deck.")
        return
    
    user_list = text_box.get("1.0",'end-1c').replace("\n", " : ").split(" : ")
    list_len = len(user_list)
    deck_class = tkvar.get()
    deck_to_analyze = "'Class': " + "'" + deck_class + "', " + deck_format
    deck_to_display = ""
    deck_size = 0
    i = 0
    
    if list_len % 2 != 0:
        messagebox.showerror("Incorrect Formatting!", "Something is wrong with your deck's format")
        return
    
    while i < list_len:
        cname = user_list[i]
        
        if not card_type.has_keys(cname) or cname != "Arcane Golem":
            messagebox.showerror("Unknown Card!", cname + " is not a recognized card.")
            return
        
        copies = user_list[i+1].strip()
        cards = ""
        
        if copies.isdigit():
            copies = int(copies)
            rarity = card_rarity.get(cname)
            
            if (rarity == "LEGENDARY" and copies == 1) or (rarity != "LEGENDARY" and copies <= 2):
                cclass = card_class.get(cname)
                
                if cclass == deck_class or cclass == "Neutral" or cname == "Arcane Golem":
                    deck_size += copies
                    deck_to_analyze += "'" + cname + "'" + " : " + str(copies) + ", "
                    deck_to_display += cname + " : " + str(copies) + "\n"
                else:
                    messagebox.showerror("Wrong class!", str(cname) + " is not a " + str(deck_class) + " class card. \n" +
                                          "It is a " + str(cclass) + " class card.")
                    return
            else:
                if rarity == "LEGENDARY":
                    n = "1"
                else:
                    n = "2"
                    messagebox.showerror("Too many copies!", "The max number of copies for " + cname + " is " + n)
                    return
        else:
           messagebox.showerror("Number missing!", "Please write a number for " + cname)
           return
        
        i += 2
    
    if deck_size > deck_size_limit:
        this_many = str(deck_size - deck_size_limit)
        messagebox.showerror("Too many cards!", "Your deck is too big. Remove " + this_many + " cards.")
        return
    elif deck_size < deck_size_limit:
        this_many = str(deck_size_limit - deck_size)
        messagebox.showerror("Too few cards!", "Your deck is missing cards. Add " + this_many + " more cards.")
        return
    
    deck_to_analyze = deck_to_analyze[0:-2] # Getting rid of the last comma
    
    display = deck_classification(deck_to_analyze, whatarch)
    
    deck_to_display += display
    
    response = messagebox.showinfo("Your " + deck_class + " deck", deck_to_display)

def analyze_random_deck():
    deck_list = {}
    deck_size = 0
    random_class = random.choice(classes)
    
    random_file = card_path + random_class + ".txt"
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
        rarity = ""
        i = 0
        
        while card_name == "" or rarity == "":
            if "name': " in values[i]:
                card_name = values[i]
                card_name = card_name.split("name': ")[-1][1:-1]
            elif "rarity" in values[i]:
                rarity = values[i]
                
            i += 1
        
        if card_name in deck_list.keys():
            if "LEGENDARY" not in rarity and deck_list.get(card_name) < 2:
                updated_entry = {card_name: deck_list.get(card_name) + 1}
                deck_list.update(updated_entry)
                deck_size += 1
        else:
            if "LEGENDARY" not in rarity:
                random_number = random.randint(1,2)
                deck_list[card_name] = random_number
                deck_size += random_number
            else:
                deck_list[card_name] = 1
                deck_size += 1
    
    deck_class = random_class.capitalize()
    deck_to_display = ""
    deck_to_analyze = "'Class': " + "'" + deck_class + "', " + deck_format
    
    if random_class == "demonhunter": 
        deck_to_analyze = "'Class': " + "'Demon Hunter', " + deck_format
    
    for entry in deck_list:
        deck_to_display += entry + " : " + str(deck_list.get(entry)) + "\n"
        deck_to_analyze += "'" + entry + "'" + " : " + str(deck_list.get(entry)) + ", "
        
    deck_to_analyze = deck_to_analyze[0:-2] # Getting rid of the last comma
    
    display = deck_classification(deck_to_analyze, whatarch)
    
    deck_to_display += display
    
    response = messagebox.showinfo("Random " + deck_class + " deck", deck_to_display)
            
def analyze_generated():
    return

def generate_card(Class, mana, Type, attack, health, text_box):
    global first_push

    if first_push == 1:
        mana.delete(0, 'end')
        mana.insert(0, "Mana: ")
        
        Class.delete(0, 'end')
        Class.insert(0, "Class: ")
        
        Type.delete(0, 'end')
        Type.insert(0, "Type: ")
        
        attack.delete(0, 'end')
        attack.insert(0, "Attack: ")
        
        health.delete(0, 'end')
        health.insert(0, "Health: ")
        
        text_box.delete('1.0', END)
    
    if mana.get() == "Mana: ":
        mana.insert(END, str(random.randint(1, 10)))
    if Class.get() == "Class: ":
        Class.insert(END, random.choice(classes).capitalize())
    if Type.get() == "Type: ":
        Type.insert(END, random.choice(types).capitalize())
    
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

    if generation_type.get() != 3:

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
    else:
        # LSTM generation
        pred = []
        encoded = my_tokenizer.texts_to_sequences([inpt_str.lower()])[0]
        encoded = pad_sequences([encoded], maxlen=10, truncating='pre')

        yhat = my_lstm.predict(encoded, verbose=0)
        for probs in yhat:
            index = np.argmax(probs)
            if index != 0:
                pred.append(int(index))
        pred = my_tokenizer.sequences_to_texts([pred])

        if Type.get()[6:].lower() == "minion" or Type.get()[6:].lower() == "weapon":
            if extra_info == 0 and len(pred) >=2:
                attack.insert(END, pred[0])
                health.insert(END, pred[1])
                text_box.insert('1.0', " ".join(pred[2:]))
            elif extra_info == 1 and len(pred) >= 1:
                health.insert(END, pred[0])
                text_box.insert('1.0', " ".join(pred[1:]))
            else:
                text_box.insert('1.0', " ".join(pred))
        else:
            text_box.insert('1.0', " ".join(pred))

    first_push = 1 # The button has been pushed

    return
    
def deck_page():
    global my_label
    global button_card
    global button_generate
    global first_push
    
    my_label.pack_forget()
    my_label = Label(root, image=my_img3)
    my_label.pack()
    
    first_push = 0
    
    text_box = Text(root, height=20, width=25)
    text_box.place(x=160,y=120)
    text_box.configure(font=fontExample)
    
    tkvar = StringVar(root)
    tkvar.set('Pick a class')
    popupMenu = OptionMenu(root, tkvar, *choices)
    popupMenu.place(x=23, y=225)
    popupMenu.configure(font=fontExample)
    
    button_deck = Button(root, text="Analyze Deck", command=lambda: 
                                                 analyze_deck(text_box, tkvar))
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
        
def card_page():
    global my_label
    global button_deck
    global button_generate
    global button_card
    global first_push
    
    my_label.pack_forget()
    my_label = Label(root, image=my_img2)
    my_label.pack()
    
    first_push = 0
    
    mana = Entry(root, width=10, borderwidth=5)
    mana.insert(0, "Mana: ")
    mana.place(x=105, y=75)
    mana.configure(font=fontExample)

    name = Entry(root, width=35, borderwidth=5)
    name.insert(0, "Name: ")
    name.place(x=125, y=260)
    name.configure(font=fontExample)

    attack = Entry(root, width=10, borderwidth=5)
    attack.insert(0, "Attack: ")
    attack.place(x=105, y=405)
    attack.configure(font=fontExample)

    health = Entry(root, width=10, borderwidth=5)
    health.insert(0, "Health: ")
    health.place(x=325, y=405)
    health.configure(font=fontExample)

    text_box = Text(root, height=5, width=24)
    text_box.place(x=170, y=315)
    text_box.configure(font=fontExample)
    
    tkvar = StringVar(root)
    tkvar.set('Pick a class')
    popupMenu = OptionMenu(root, tkvar, *choices)
    popupMenu.place(x=15, y=7)
    popupMenu.configure(font=fontExample)
    
    var = StringVar(root)
    var.set('Pick a type')
    dropMenu = OptionMenu(root, var, *choose)
    dropMenu.place(x=375, y=7)
    dropMenu.configure(font=fontExample)
    
    button_deck = Button(root, text="Check Deck List", bg='#567', fg='White', command=deck_page)
    button_deck.place(x=5, y=465)
    button_deck.configure(font=fontExample)
    
    button_card = Button(root, text="Analyze Card", command=lambda: 
                            analyze_card(mana,name,attack,health,text_box,tkvar,var))
    button_card.place(x=200, y=465)
    button_card.configure(font=fontExample)
    
    button_generate = Button(root, text="Generate A Card", bg='#567', fg='White', command=generate_page)
    button_generate.place(x=382, y=465)
    button_generate.configure(font=fontExample)

def generate_page():
    global my_label
    global button_card
    global first_push
    
    my_label.pack_forget()
    my_label = Label(root, image=my_img2)
    my_label.pack()

    mana = Entry(root, width=10, borderwidth=5)
    mana.insert(0, "Mana: ")
    mana.place(x=105, y=75)

    Class = Entry(root, width=18, borderwidth=5)
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
generation_menu.add_radiobutton(label="LSTM", variable=generation_type, value=3)
menubar.add_cascade(label='Generator', menu=generation_menu)
root.config(menu=menubar)

card_library_creator()
native_bayes_classifier()
root.mainloop()