with open('clean_cards_file.txt', 'r') as card_file:
    cards = card_file.readlines()

cardClasses = {
    "'DEMONHUNTER'" : [],
    "'DRUID'" : [],
    "'HUNTER'" : [],
    "'MAGE'" : [],
    "'NEUTRAL'" : [],
    "'PALADIN'" : [],
    "'PRIEST'" : [],
    "'ROGUE'" : [],
    "'SHAMAN'" : [],
    "'WARLOCK'" : [],
    "'WARRIOR'" : [],
}    


for line in cards:
    if 'classes' in line:
        for c in cardClasses: # Iterate over the keys
            if c in line and not c == "'NEUTRAL'":
                cardClasses.get(c).append(line)
    else:
        for c in cardClasses: 
            if c in line and not "'HERO_SKINS'" in line:
                cardClasses.get(c).append(line)
                break
            
            
for c in cardClasses:
    name = c.replace("'", '')
    filename = name.lower() + ".txt"
    input_file = open(filename, "w")
    input_file.writelines(cardClasses.get(c))
    input_file.close()  