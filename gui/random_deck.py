import random

# Folder Path
deck_path = "../data/decks/cleaner/"

aggressive_decks = deck_path + "AggroDecks.txt"
combo_decks = deck_path + "ComboDecks.txt"
control_decks = deck_path + "ControlDecks.txt"
midrange_decks = deck_path + "MidrangeDecks.txt"

deck_archetypes = [aggressive_decks, combo_decks, control_decks, midrange_decks]

random_archetype = random.choice(deck_archetypes)
print(random_archetype.replace(deck_path, "").replace("Decks.txt", ""))

with open(random_archetype, 'r', encoding="ISO-8859-1") as arch_file:
    arch_cards = arch_file.readlines()

random_deck = random.choice(arch_cards)
deck = random_deck.replace("': ", " : ")
deck = random_deck.replace('": ', " : ")
deck = deck.split(", '")

for d in deck:
    d = d.replace("': ", " : ")
    if ', "' in d:
        d = d.replace(', "', "\n")
    print(d)
