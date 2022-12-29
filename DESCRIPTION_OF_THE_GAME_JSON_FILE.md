# Description of the Python Adventure Game Engine JSON file

The JSON file contains sections that let you combine items and rooms to interact each other.

The **sections** that can be considered as *main* sections is the followings:

  * *init*;
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

**author_contact** is the way to contact the game JSON file author’s. It could be an URL or an e-mail. It’s simple a text field and it’s optional.

**author_github** is the Github profile URL of the game JSON file author’s. It’s an optional field.

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

  * id;

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

