# The Arch-inator
## Getting started 
First place the LSTM model in the models directory. Then change directory to the gui directory and run the hs_gui python script.
## The home screen
Once the application opens, you should see one menu item and three buttons. The menu item (generator) allows you to select which type of model should be used to generate cards. The buttons will take you to their respective section of the application.
## Checking a deck
This section analyzes decks and predicts which archetype they would best fit into. The easiest way to see this in action is to simply click the analyze random deck button which will first generate a random deck and show the results. If instead you have a deck list you would like to input you can do so in the middle text box, just be sure to also select the class of the deck on the left drop down. The decks should look something like this warlock deck:
{Murloc Tinyfin : 2
Wisp : 1
Abusive Sergeant : 2
Argent Squire : 2
Reliquary Seeker : 2
Voidwalker : 2
Dark Peddler : 2
Echoing Ooze : 2
Haunted Creeper : 2
Knife Juggler : 2
Hobgoblin : 2
Imp Gang Boss : 2
Defender of Argus : 2
Gormok the Impaler : 1
Imp-losion : 2
Sea Giant : 2}
## Checking a card
This section analyzes a card that you input. You need to input the class and type of the card with the drop down menus in the top. Then input the mana cost and card name in the respective boxes. Finally input any text, attack, and health information in their respective boxes. Then you can click the analyze card button in the bottom and see what archetype would likely benefit from having this card in their deck.
## Generating a card
This section generates a card's text from its cost, class, and type. You can directly input these inputs (as well as attack or both attack and health) then press the generate card button to generate the card's text. Note that any subsequent presses of the generate card button will generate the cost, class, and type randomly then generate the card's text based on that. If you want to generate another card from your own input simply go to one of the other sections and come back to this one afterwards.