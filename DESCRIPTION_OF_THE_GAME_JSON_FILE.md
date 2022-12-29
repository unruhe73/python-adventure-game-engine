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

**values** let you define some enviroment variable, for example a name or a characters sequence for a safe combination. In the example game you have two safes in two different rooms.

In the example game we have:

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

**id** is a unique string identifier of the room. You cannot have two or more rooms with the same ID. Better if you avoid spaces in the *id*.

**name** is the name of the room. For example: kitchen, toilet, outside, and so on. You can choose it as you wish and it’s the name the engine shows to the user to say: "You are in the **name**...".

**init_state** is the starting state of the room. The room has a state, it’s a string ID. You can choose "0", "1", "2" and so on or you can give any name you wish. Why do I need a state for the room? Well, because the room description can change. How can it change? Suppose you use an item that destroy the whole room with all the items inside, so you have to change the description.

**description** is a complex string used to describe the room, but it can also contains more descriptions. Why a complex string? Because you can add into the description a brief description of the items you see in the room and, of course, if an a item is collected it’s not in the room anymore. You can add this runtime description using the **ID string of the item** into curly brackets. If you want to focus on the usable items in the room that can always be there you can write the item name between asterisks. Here an example of a complex description:

    "description": "In this room there is {egg_room_01} a microwave *oven* {blue_crystal_room_01}. {flyer_room_01}"

In this case there are three removable items:

 1. egg_room_01;
 2. blue_crystal_room_01;
 3. flyer_room_01.

What does it mean `{egg_room_01}`? It’s a string that is defined into the related item. You’re seeing it in the **Items Section**. And, as said, **oven** has a bold output to focus user on it, like to say: "play a bit with the oven, use it".

The description can have multiple content because of its state. If you want to define a multiple description you need to associate the state and its description in this way:

          "description": {
              "0": "In this room there is a lot unsense things {cylinder_room_03}.",
              "1": "In this room there is nothing. Everything has burnt because of an explosion."
          }

When the room is in the state "0" the description is: "In this room there is a lot unsense things {cylinder_room_03}.". Of course, in placed of "{cylinder_room_03}" you are going to get the item description defined in the item section.

If the state is "1" then you are going to get: "In this room there is nothing. Everything has burnt because of an explosion.".

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

The **items section** is an array that contains all the items properties.

  * id;

# winning_conditions Section

This is an item that specifies how the user can win the game. It defines the room in which user has to stay currently and the list of items ID he had to collect. This information in specified by:

  * current_room;
  * collected_items.

In the example game you have:

      "winning_conditions": {
          "current_room": "room_06",
          "collected_items": ["blue_crystal_room_01", "white_crystal_room_02", "coins_room_04", "yellow_crystal_room_12"]
      }

This means that you need to collect the three crystals and the coins and than you need to go to room_06.

