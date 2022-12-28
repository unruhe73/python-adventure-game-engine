# Python Adventure Game Engine

[![GitHub license](https://img.shields.io/badge/license-GPL-blue)](https://github.com/unruhe73/python-adventure-game-engine/blob/main/LICENSE)
[![Made with Python 3](https://img.shields.io/badge/python-3.x-powered)](https://www.python.org/)

This is a new project. An Adventure Game Engine written in Python. You can create an adevnture game just describing it in a JSON file and playing it with the python language running **main.py** file. Lots of things has to be included in the engine, lots of feature is going to be implemented. This is just a basic version. For example, a JSON GA validator method has to be written to avoid that a malformed game JSON file could produce a crash of the engine.

At the current state the JSON file structure can change and the example game JSON file is going to change its contents while new features will be added or bugs fixed.

# How to play the game
When you run **main.py** the game engine looks for JSON files into the **games** directory. If it finds just one file then the game will start, if it finds more than one game JSON file than you’re going to be asked for what game you want to play.

The game starts with a room description. Your characters has to act in this room. You can collect items, can use them with other items, can get more details about them and so on.

All the items that can be *used* are shown with **bold words** into the room description.

At the moment you have the following main verbs and words:

  * catch;
  * close;
  * describe;
  * help;
  * inventory;
  * open;
  * pull;
  * push;
  * quit;
  * use.

Of course there are **synonymous** and **alias** in the example game (you can change them as you wish or define new *synonymous* and *alias*) to get you more comfortable with an action and to let you use just one charecter to express a long verb, for example **d** stands for **describe** as defined in the example game, of course you can remove it if you prefer typing just **describe** word to get an item desription, also if I suggest don’t do it becase it’s a very recurring action verb.

This actions verbs can be defined as you wish, in English or in any other language, so you could translate the game and its verbs, the items description, the room descriptions and so on.

In the example game JSON file you will find the following **actions** section:

      "actions": {
          "catch": ["catch", "get", "grab", "take", "bring"],
          "close": ["close"],
          "describe": ["describe", "descr", "d"],
          "help": ["help", "h", "?"],
          "inventory": ["inventory", "list", "i", "inv"],
          "open": ["open"],
          "pull": ["pull"],
          "push": ["push", "press", "p"],
          "quit": ["exit", "x", "quit", "bye", "b", "q", "\\q"],
          "use_verb": ["use"],
          "use_with": ["with", "in", "on", "into", "inside", "over"]
      }

The **actions** section tells to the engine game what verbs can be used to collect an item, to close an item (for example a door), and so on. You can modify just the content placed into square parenthesis.

Just let me explain giving more details. Get focus, for example, on the verb “catch”. It is intended to collect items. In the example game you’re finding: **catch**, **get**, **grab**, **take**, **bring**.

This means that when you type:

`catch item`

or:

`get item`

or:

`grab item`

or:

`take item`

or:

`bring item`

You’re saying to the game engine that you want to collect the item and put it into your inventory. Of course you could translate these verbs in the language you can speak. Remember that you can translate just the words into square parenthesis, so the English **actions** section:

      "actions": {
          "catch": ["catch", "get", "grab", "take", "bring"],
          "close": ["close"],
          "describe": ["describe", "descr", "d"],
          "help": ["help", "h", "?"],
          "inventory": ["inventory", "list", "i", "inv"],
          "open": ["open"],
          "pull": ["pull"],
          "push": ["push", "press", "p"],
          "quit": ["exit", "x", "quit", "bye", "b", "q", "\\q"],
          "use_verb": ["use"],
          "use_with": ["with", "in", "on", "into", "inside", "over"]
      }

in Italian could become:

      "actions": {
          "catch": ["afferra", "raccogli", "colleziona", "prendi"],
          "close": ["chiudi"],
          "describe": ["descrivi", "descr", "d"],
          "help": ["aiuto", "?"],
          "inventory": ["inventario", "elenca", "i", "inv"],
          "open": ["apri"],
          "pull": ["tira"],
          "push": ["spingi", "premi", "p"],
          "quit": ["esci", "x", "ciao", "e", "c", "\\q"],
          "use_verb": ["usa"],
          "use_with": ["con", "in", "su", "sopra", "dentro"]
      }

You can get an item description using just the character “d”. For example:

`d crystal`

means you need a more detailed description of the crystal. The description of an item let you get the more detailed description (if it exists) of the item into the room. But how you can get the same description of the item you previously put into the inventory? Because you can basically describe just item that are part of the room. Simply specify the you are referring to the “inventory”:

`describe inventory crystal`

or the shortest:

`d i crystal`

You can get the list of the inventory items with one of the following words (I’m referring to the example game JSON file):

**inventory**, **list**, **i**, **inv**

But what happens when you collect more items with the same name? You can get a yellow crystal, a white crystal, a blue crystal and so on. Usually you have a single crystal in a room, but putting it into the inventory they can be more than one. In this case if you ask for the item lists you will get an unambiguous name. In the crystal example it could be:

`white crystal`

so to the describe exactly the white crystal you have to use **white crystal** as name. So the action will be:

`d i white crystal`

There is a special action into the list of actions, but it’s not really an action. It is the **use_with** list. It specifies how to tell to use an item **with** another. It’s so defined:

`"use_with": ["with", "in", "on", "into", "inside", "over"]`

the words into the square parenthesis can be translated. Anyway, this words are used between the two items name. For example:

`use key with door`

or:

`use key into door`

or:

`use key in door`

and so on.


# Moving from a room to another
A room is intended to be square, so it has four sides. You can move into another room with the direction actions defined in the **directions** section, so defined in the game JSON file:

      "directions": {
          "north": ["north", "up"],
          "south": ["south", "down"],
          "west": ["west", "left"],
          "east": ["east", "right"]
      }

So if you want to move in the room in front of you you can choose between the two words: **north** or **up**. You want to move back of you? Then you can use **south** or **down**.

The words on the left, as already said, can’t be translated. In Italian you can replace the **directions** section with the following one:

      "directions": {
          "north": ["nord", "su"],
          "south": ["sud", "giu"],
          "west": ["ovest", "sinistra"],
          "east": ["est", "destra"]
      }

# Replaying a game
Sometimes you need to replay a game. When you start playing a game, than a directory called **replays** is going to be created to save a replay. What is it a **replay** file? It’s the list of actions you performed in your last play. Included environment variable used to define safe combinations.

At the begining of the game you could replay the last game if it exists. You can’t replay a game if you started playing a new one because the last replay is going to replace it with the new playing actions. You can always save the **replays** directory somewhere to keep a backup of it to use when you want.

This feature is used to debug the game. With a replay I can repeat the same actions I did last time, in the same order, using the same commands, the same actions. But it can also be useful if the game is long and you want to stop playing at some time. Next time you can replay and than go on from there. Of course if you die during the game, replaying it you will die again.

# Writing a game JSON file
You can find the game JSON file description into the file [DESCRIPTION_OF_THE_GAME_JSON_FILE](DESCRIPTION_OF_THE_GAME_JSON_FILE.md).