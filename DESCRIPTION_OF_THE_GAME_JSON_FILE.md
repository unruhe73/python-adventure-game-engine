# Description of the Python Adventure Game Engine JSON file

The JSON file contains sections that let you combine items and rooms to interact each other.

The **sections** that can be considered as *main* sections is the followings:

  * *game details*;
  * rooms;
  * items;
  * winning_conditions;
  * directions;
  * actions;
  * text.

# Game Details Section

The **game details section** is not really a section, but it’s composed by the following keys name:

  * name;
  * version;
  * license;
  * license_url;
  * author_name;
  * author_contact;
  * author_github;
  * release_date;
  * update_date;
  * replay_filename;
  * waiting_time;
  * show_countdown;
  * get_new_action;
  * starting_room;
  * values.

In the example game JSON file you can find:

      "name": "The Example Adventure Game",
      "version": "1.0.1",
      "license": "Creative Commons BY-NC-ND 4.0",
      "license_url": "https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode",
      "author_name": "Giovanni Venturi",
      "author_contact": "https://kslacky.wordpress.com/",
      "author_github": "https://github.com/unruhe73",
      "release_date": "31 Oct 2022",
      "update_date": "29 Dec 2022",
      "replay_filename": "The_Example_Adventure_Game.replay",
      "waiting_time": "5",
      "show_countdown": "True",
      "get_new_action": "Enter Key",
      "starting_room": "room_01",
      "values": {
        "assigned_safe_combination": "COMEINHERE",
        "random_safe_combination": "%RANDOM(6)"
      }

**name** is the game name.

**version** is the game version.

**license** is the license of the game JSON file.

**license_url** is the URL where you can read the game JSON file license.

**author_name** is the author name of the game JSON file.

**author_contact** is the way to contact the game JSON file author’s. It could be an URL or an e-mail. It’s simple a text key and it’s optional.

**author_github** is the Github profile URL of the game JSON file author’s. It’s an optional key.

**author_name** is the author name of the game JSON file.

**release_date** is the release date of the game JSON file.

**update_date** is the update date of the game JSON file, for example if you add items, rooms, or fix some bug. You could have forgotten to specify how to get into a room from another one.

**replay_filename** is the replay filename. You can use **replay** command to replay a game that it will read this file.

When the engine describes the room you are inside then you can give a command. The game engine executes it and then before go on, it can move into another room or let you collect an item and so on. Anyway, after any action you required it can act in two possible ways:

 1. count for **waiting_time** seconds showing the countdown or not: it depends from the boolean value you assigned to **show_countdown**: *True* or *False*;
 2. ask to you to press **ENTER** key to continue playing.

How does it choose between 1 or 2? It depends from the value of **get_new_action**. If it is **Enter Key** the game engine wait for you, so you need to press **ENTER** key when you are ready to go on. If it is **countdown** it counts as told in point 1. If you remove the **get_new_action** line from the game JSON file, than it goes on with the method numer 1. He prefers the countdown as default choice.

**starting_room** is the room from where the game begins. It has to contain a **room ID** as defined next.

**values** let you define some enviroment variable, for example a name or a characters sequence for a safe combination. In the example game JSON file you have two safes in two different rooms.

In the example game JSON file we have:

      "values": {
        "assigned_safe_combination": "COMEINHERE",
        "random_safe_combination": "%RANDOM(6)"
      }

Well, **assigned_safe_combination** and **random_safe_combination** are generic variable names the game is using in descriptions and safe combination you could call as you wish, also **var1** and **var2** so, in this case, it can be:

      "values": {
        "var1": "COMEINHERE",
        "var2": "%RANDOM(6)"
      }

Remember to replace that new names in the whole game JSON file.

**COMEINHERE** it’s just text. You can fill it as you wish, you can also replace with *MY_TEXT*.

**%RANDOM(6)** it’s an engine function. It means: give me a sequence of 6 random characters (numbers and upper case letters).

# Rooms Section

The **rooms section** is an array that contains all the properties of the defined rooms.

The keys contained in a room are:
  * id;
  * name;
  * init_state;
  * description;
  * items;
  * north;
  * south;
  * west;
  * east.

**id** is a unique string identifier for the room. You cannot have two or more rooms with the same ID. Better if you avoid blank spaces in the *id* key, use the "**_**" character in place of the blank space one. Look at the example game JSON file in the directory *games*.

**name** is the name of the room. For example: kitchen, toilet, outside, and so on. You can choose it as you wish and it’s the name the engine shows to the user to say: "You are in the **kitchen**/**toilet**/**outside**...".

**init_state** is the starting state of the room. The room has a state, it’s a string ID. You can choose "0", "1", "2" and so on or you can give any name you wish. Why do I need a state for the room? Well, because the room description can change. How can it be changed? Suppose you use an item that destroy the whole room with all the items inside, so you have to change the description.

**description** is a complex string used to describe the room, but it can also contains more descriptions. Why a complex string? Because you can add into the description a brief description of the items you see in the room and, of course, if an a item is collected it’s not in the room anymore. You can add this runtime description using the **ID string of the item** into curly brackets. If you want to focus on the usable items in the room that can always be there you can write the item name between asterisks. Here an example of a complex description:

    "description": "In this room there is {egg_room_01} a microwave *oven* {blue_crystal_room_01}. {flyer_room_01}"

In this case there are three removable items:

 1. egg_room_01;
 2. blue_crystal_room_01;
 3. flyer_room_01.

What does it mean `{egg_room_01}`? It’s a string that is defined into the related item. You’re getting more details about it in the **Items Section**. And, as said, **oven** has a bold output to focus user on it, like to say: "play a bit with the oven, use it".

The description can have multiple content because of its state. If you want to define a multiple description you need to associate the state and its description in this way:

          "description": {
              "0": "In this room there is a lot unsense things {cylinder_room_03}.",
              "1": "In this room there is nothing. Everything has burnt because of an explosion."
          }

When the room is in the state "0" the description is: "In this room there is a lot unsense things {cylinder_room_03}.". Of course, in placed of "{cylinder_room_03}" you are getting the item description defined in the related item section.

If the state is "1" then you are getting: "In this room there is nothing. Everything has burnt because of an explosion.".

**items** is an array that contains the items id presents in the room. Also if you have just one item the key **items** is an array. An array is defined with its items into a square brackets and separated by a comma. If I don’t have any item in the room then the **items** key is not present.

**north**, **south**, **west** and **east** contains a string. This string is *none* if you can’t move in that direction, but if you can then the string refers to the new room string ID.

Well, but moving in a direction could have a condition. Consider you have a door in the north direction. You can move to the north just if the door is open. How do you describe this situation? Just have a look at the example:

          "north": {
              "if_item_id": "door_room_09",
              "if_state": "0",
              "go_to": "room_10",
              "failed_because": "There's a closed door."
          },

The condition is related to the item *door_room_09*, if the item is in state "0" you can move to the north and then go to the room *room_10*. If the *door_room_09* is not in state "0" than the user that want to move to the north is getting the message: "There's a closed door".

Here a quite basic example of a room definition:

        {
            "id": "room_01",
            "name": "kitchen",
            "init_state": "0",
            "description": "In this room there is {egg_room_01} a microwave *oven* {blue_crystal_room_01}. {flyer_room_01}",
            "items": ["egg_room_01", "oven_room_01", "blue_crystal_room_01", "flyer_room_01"],
            "north": "none",
            "south": "none",
            "west": "room_02",
            "east": "none"
        }

Of course, each room definition after the closing curly bracket need a comma if there is another room definition.

Here a more complex example of a room description:

        {
            "id": "room_09",
            "name": "smaller studio",
            "description": "You are in a small studio, there is a *door* in front of you and a *safe* on the wall. {key_room_09}",
            "items": ["safe_room_09", "door_room_09"],
            "north": {
              "if_item_id": "door_room_09",
              "if_state": "0",
              "go_to": "room_10",
              "failed_because": "There's a closed door."
            },
            "south": "none",
            "west": "room_08",
            "east": "none"
        }

And here you are another one with the multi description:

        {
            "id": "room_03",
            "name": "storage closet",
            "init_state": "0",
            "description": {
              "0": "In this room there is a lot unsense things {cylinder_room_03}.",
              "1": "In this room there is nothing. Everything has burnt because of an explosion."
            },
            "items": ["cylinder_room_03"],
            "north": "none",
            "south": "room_02",
            "west": "room_05",
            "east": "room_04"
          }

# Items Section

The **items section** is an array that contains all the items properties. It’s the more complex JSON structure of the whole project. There are lots of keys and sub keys.

  * id;
  * name;
  * when_included_in_the_room;
  * init_state;
  * describe_act:
      * state;
      * text;
      * new_state;
  * catch_act:
      * state;
      * text;
      * destination
      * can_catch_if: *if_item_id*, *in_state*, *else_cant_catch_reason_state*;
      * new_state;
  * pull_act:
      * state;
      * text;
      * new_state;
  * push_act:
      * state;
      * text;
      * new_state;
  * open_act:
      * state;
      * text;
      * new_state;
  * close_act:
      * state;
      * text;
      * new_state;

A general consideration. A *state* can be just one state and in this case is just a string, but can be also a set of states, so you need to define an array with a square brackets.

**id** is a string ID that has to be unique as item ID in the whole game JSON file. You can choose a sequence of letters, numbers and use "_" instead of blank spaces.

**name** is the sequence string user cas use to act on it.

**when_included_in_the_room** is a text description added to the room description when the item is still available in the room and in the room description is referred with curly brackets as said in the **Rooms Section**.

**init_state** is the starting state of the item. It’s a numeber or also a sequence of text, letters and "_" to identify this item state.

**describe_act** it could be just a text used when user request a description of the item or it can be more complex adding the keys:

 1. state;
 2. text;
 3. new_state.

In this case, *state* means that the *text* description is associated to the item state *state* and after the user got the description the item state move to *new_state* and than looking again the item the user should get a different description, so be careful to remember to associate a *new_state* just if needed. If you don’t need to assign a new state for your item than do not declare this *key* use just *state* and *text*. If you need always the same description for the item simply assign the text to *describe_act*.

Well, you can have also the *if_there_is_item* key into a *describe_act* key. Look at this:

        "if_there_is_item": [
          {
            "if_item_id": "egg_room_01",
            "has_destination": "room",
            "than_append_description": "There is an {name} inside."
          }

You’re describing an oven and inside the over there could be an egg or not. If the egg is inside the oven, well more precisely if the egg_room_01 item is still part of the room, as specified by the *has_destination* key, when you ask an oven description you're getting also the information:

`There is an {name} inside.`

And `{name}` is replaced by the *name* key of the egg_room_01 item ID.

**catch_act** is the same as **describe_act** but related to the **catch** action. If you assign to the key just a string the item is not moved into the inventory. To move into the inventory or move into the inventory and keep it also in the room you need to specify an array with array items as following:

          "catch_act": [
            {
              "state": ["0", "1"]
              "text": "Got it! I like it. Oh, it's very cold.",
              "destination": "inventory"
              "new_room_description_status": "2"
              "new_state": "2"
            }
          ]

*state* is the state in which the item is to catch it.

*text* is text message for when you got the item and *destination* specify where to put the item:

 1. inventory;
 2. room_and_inventory;
 3. destroyed.

The **fist case** tells to the engine to move the item from the room to the inventory. This is the standard behaviour a user could want.

The **second case** tells to the engine to add the item to the inventory but to keep it also into the room. This could happen with coins, for example, you get some coins but lots of them stay in the room.

The **third case** tells to the engine to remove the item from the room because the catch action destroied it. This could happen if you try to cacth a fragile eggs, for example. It doesn’t stay in the room and it doesn’t go into the inventory.

If *destination* key is absent the item stay in the room. This key is optional.

If there is also a *new_room_description_status* key than the related room where the item is in is changing the status and will change the description too. For example an explotion destoy the room:

          "catch_act": [
            {
              "text": "Got it! But what's happening? It's going to... explode! [3] I thrown it away right in time!",
              "destination": "destroyed",
              "new_room_description_status": "1"
            }
          ]

Did you notice the **number** into the square brackets? In this case the text on the left ot the opened square bracket is printed out at once. The text on the right of the closed square bracket is printed out 3 seconds later. It’s 3 seconds because that is the number. Change it in the *text* key and you're waiting a different time.

If *new_state* key is present then after the action the item move to the new state.

If *death* key is present than after you get the item you're going to die if it’s "True". The other value, as is it’s a boolean, is "False" and in this case you stay alive and you don’t need to specify *death* key to say it’s "False", simply don’t use this key.

As extention you can have a condition to execute a catch action on the item. This condition is defined by the sub keys:

 1. if_item_id;
 2. in_state;
 3. else_cant_catch_reason_state.

The *if_item_id* is the subject item of the condition, *in_state* is its state and *else_cant_catch_reason_state* is a text with which the *catch* action replies if the if_item_id item ID is not in the state *in_state*. For example, you can’t grab a key inside a safe if the safe is not open. You have first to open the safe, maybe get a description of the opened safe and than you can get the key.

**pull_act** is the same as **describe_act** but related to the **pull** action.

**push_act** is the same as **describe_act** but related to the **push** action.

**open_act** is the same as **describe_act** but related to the **open** action. And you can get more reactions from the open action according to the item state. The open action can move to a new state for the item too with the *new_state* key. Here an example:

          "open_act": [
            {
              "state": "0",
              "text": "It's already open."
            },
            {
              "state": "1",
              "text": "You've opened it.",
              "new_state": "0"
            }
          ]

Of course, not always the *new_state* is available.

**close_act** is the same as **describe_act** but related to the **close** action. And you can get more reactions from the close action according to the item state. The close action can move to a new state for the item too with the *new_state* key. Here an example:

          "close_act": [
            {
              "state": "0",
              "text": "You've closed it.",
              "new_state": "1"
            },
            {
              "state": "1",
              "text": "You've already closed it."
            }
          ]

Of course, not always the *new_state* is available.

**use_act** is the part where you describe the items interation. it’s referred to verb *use* and all its synonymous defined in the subsection **use_verb** of the **actions** section. You can use a single item or you can use it with some other items. To define inside an item definition the action related to use this item on its own you could define something like this:

          "use_act": {
            "use_alone": [
              {
                "text": "It's very sharp, maybe I need to use it with something else."
              }
            ]
          }

Of course the *use_alone* is a list because when you’re using an item you could change its state. When you don’t specify status it means that each time you’re using that item you’re getting always the same reply defined in *text*.

When you’re using an item with another by default the engine is using the item in the room with an item you have in your inventory. To define interactions with more items you need to specify the *text* for each secondary item in the definition of the item you’re describing using *use_with*. For example:

        "use_with": [
          {
            "item": "mummy_room_07",
            "text": "Ops, it seems like to cut a human body. I should stop doing this."
          },
          {
            "item": "electric_window_room_05",
            "text": "Oh, my, I can't take my hands off the bars anymore. [3] Aaaaaaahhhhhhhhhhh!",
            "death": "True"
          }
        ]

This define the use of the current item with the *mummy_room_07* item ID and with the *electric_window_room_05* item ID. As you can see the use wit the *electric_window_room_05* item ID you getting as result the death of the character because *death* is **True**. And in the definition of *text* you can see a number into square brackets. As you can immagine this text is going to be divided in the part before the square brackets and the part after the square brackets. The first part is going to be printed at once, after a delay of 3 seconds (the number in the square brackets) it’s going to be printed the second part.

You can define the word to separare the two items in the subsection *use_with* in **actions** section.

For example you can give the command:

`use item1 with item1`

or:

`use item1 inside item1`

or:

`use item1 over item1`

or:

`use item1 into item1`

As defined in the example game JSON file.

Here an example of an item definition where you can see also the case of a set of states for the *describe_act* and for the *catch_act*:

        {
            "id": "egg_room_01",
            "name": "egg",
            "when_included_in_the_room": "an *egg* into",
            "init_state": "0",
            "describe_act": [
              {
                "state": "0",
                "text": "It's just a fragile egg. I'm not sure I need it.",
                "new_state": "1"
              },
              {
                "state": ["1", "2"],
                "text": "I can see something on its surface. A blue line, maybe. It's too dark to say. I could try to...",
                "new_state": "2"
              }
            ],
            "catch_act": [
              {
                "state": ["0", "1"],
                "text": "I'm not sure I need it. Do you think I need it? Maybe I get more details if..."
              },
              {
                "state": "2",
                "text": "Ops, I just broke it, oh my!",
                "destination": "destroyed",
                "can_catch_if": {
                  "if_item_id": "oven_room_01",
                  "in_state": "0",
                  "else_cant_catch_reason_state": "1"
                }
              }
            ],
            "pull_act": [
              {
                "state": "0",
                "text": "Do I really have to pull it?",
                "new_state": "2"
              },
              {
                "state": "2",
                "text": "Ops, I just broke it, oh my!",
                "destination": "destroyed"
              }
            ],
            "push_act": [
              {
                "state": "0",
                "text": "I'm not sure I have to push it. Do I have?",
                "new_state": "2"
              },
              {
                "state": "2",
                "text": "Ops, I just broke it, oh my!",
                "destination": "destroyed"
              }
            ]
          }

# winning_conditions Section

This is an item that specifies how the user can win the game. It defines the room in which user has to stay currently and the list of items ID he had to collect. This information in specified by:

  * current_room;
  * collected_items.

In the example game JSON file you have:

      "winning_conditions": {
          "current_room": "room_06",
          "collected_items": ["blue_crystal_room_01", "white_crystal_room_02", "coins_room_04", "yellow_crystal_room_12"]
      }

This means that you need to collect the three crystals and the coins and than you need to go to room_06.

# Directions Section

It’s just the words to use for the moving actions. It should alway be:

      "directions": {
          "north": ["north", "up"],
          "south": ["south", "down"],
          "west": ["west", "left"],
          "east": ["east", "right"]
      }

So to move to the **north** you can use *north* or *up* word, but you can add as many as you wish, or translate in another language. Remember you can translate just the square brackets contents.

# Actions Section

This section define the action verbs with the words you can use.

      "actions": {
          "catch": ["catch", "get", "grab", "take", "bring"],
          "close": ["close"],
          "describe": ["describe", "descr", "d", "examine", "look"],
          "help": ["help", "h", "?"],
          "inventory": ["inventory", "list", "i", "inv"],
          "open": ["open"],
          "pull": ["pull"],
          "push": ["push", "press", "p"],
          "quit": ["exit", "x", "quit", "bye", "b", "q", "\\q"],
          "use_verb": ["use"],
          "use_with": ["with", "in", "on", "into", "inside", "over"]
      }

For example, **catch** let you collect items from rooms. So, to collect an item, you can use the following verbs followed by the item name:

  * catch;
  * get;
  * grab;
  * take;
  * bring.

Of course, the key verbs list is self-explanatory:

  * catch;
  * close;
  * describe;
  * open;
  * pull;
  * push;
  * use_verb.

And the user has to use the items in list of each *key* verb to act on the items:

`open door`, `close door`, `examine egg`, `describe egg`, `d egg`, `push oven`, `use key with door`, `get egg`, `catch egg` and so on.

While an item is in the room you can describe it using the describe key list. If you get an item from a room it will be moved into your inventory and to describe it you need to add *inventory* key between the verb and the item:

`describe inventory crystal`

or:

`d i crystal`.

In case you have more items that starts with the same name you can get a description specifying the full inventory name:

`d i white crystal`

or

`d i blue crystal`.

**quit** let you exit from the game. The "\\q" sequence has to be typed with just one "**\\**": `\q`.

You can quit the game also using **CTRL + C** keys combination.

**help** gives you the list of the available action verbs.

**inventory** give you the list of all the items in your inventory, that is all the collected items from the visited rooms.

**use_with** is not an action verb, but is the word that let you use two items together: *use item1 with item2*.

# Text Section

It’s a list of sentences used in the game. You have them in the game JSON file because you can translate it in another language. Of course the keys **has not to be translated**. And they are all sentences needed by the game engine for any game JSON file. Use always the example game JSON file to produce your own game.

      "text": {
          "assignment_value_error_for_key": "key not found in JSON *values* list.",
          "cant_create_replay_file": "Replay file can't be created!",
          "cant_find_it_into_inventory": "I can't find any {item} into the inventory.",
          "cant_read_replay_file": "Sorry, I can't read replay file.",
          "cant_replay_during_game": "Sorry, I can't replay a game during a started game play.",
          "direction_not_available": "Sorry, but I can't move in that direction.",
          "dont_understand": "Sorry, I don't understand.",
          "error_in_action_output_text_bacause_of_square": "*** There is an error in the description action in the JSON file.",
          "error_in_the_description_room": "*** There is an error in the description room parameters in the JSON file.",
          "game_author_name": "Game Author Name",
          "game_author_contact": "Game Author Contact",
          "game_author_github": "Game Author Github Profile",
          "game_license": "Game License",
          "game_license_url": "Game License URL",
          "game_release_date": "Game Release Date",
          "game_update_date": "Game Last Update Date",
          "help_actions": "You can use the following actions:",
          "help_directions": "You can move from a room to another using the following directions:",
          "i_cant_move_it": "I can't move it.",
          "i_dont_know_what_to_do": "I don't know what to do.",
          "if_can_catch_bad_configuration": "'if_can_catch' has a bad configuration.",
          "if_can_catch_if_is_defined_state_cant_be_empty": "If 'can_catch_if' is defined the related state can't be empty. 'if_can_catch' setting rejected!",
          "i_cant_catch_it": "Sorry but I can't catch it.",
          "i_got_confused_about_direction": "I got confused about direction, maybe you have a corrupted JSON file?",
          "i_havent_got": "I haven't got",
          "inventory_is_empty": "At the moment your inventory is empty.",
          "inventory_list_is_composed_by": "Your inventory is composed by the following items:",
          "item_not_found": "I can't find any",
          "just_a_moment": "Just a moment",
          "nothing_happened": "Nothing happened.",
          "press_enter_to_continue": "Press ENTER key to continue...",
          "quitting_game": "Bye bye, see you soon!",
          "show_countdown_doesn_t_match": "'show_countdown' parameter doesn't match boolean value 'True' or 'False'",
          "replaying_game": "OK, now I start replaying last game you played...",
          "syntax_error_with_use_action": "There is a syntax error using USE action. Try: USE <item> {with <item>}",
          "there_is_a_wall": "There is a wall.",
          "there_is_also": "There is also",
          "type_a_combination_to_open": "Type a combination to get opened.",
          "what_to_describe": "What object from the scene or inventory do I have to describe? Specify it.",
          "wrong_combination": "Wrong combination.",
          "you_are_dead": "I'm so sorry, but you're just dead.",
          "you_are_into_the": "You are into the",
          "you_cant_catch_it": "Sorry, but you can't catch it.",
          "you_cant_open_it": "Sorry, but you can't open it.",
          "you_need_item_xyz": "Sorry, you need",
          "you_won": "Congratulations, you won!",
          "your_combination": "Your combination"
      }
