# Description of the Python Adventure Game Engine JSON file

The JSON file contains sections that let you combine items and rooms to interact each other.

The **sections** that can be considered as *main* sections is the followings:

  * init;
  * rooms;
  * items;
  * winning_conditions;
  * directions;
  * actions;
  * text.

The **init section** is composed by:

  * name:
  * version;
  * license;
  * license_url;
  * author;
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
      "version": "1.0",
      "license": "Creative Commons BY-NC-ND 4.0",
      "license_url": "https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode",
      "author": "Giovanni Venturi",
      "release_date": "31 Oct 2022",
      "update_date": "20 Dec 2022",
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

**author** is the author of the game JSON file.

**release_date** is the release date of the game JSON file.

**update_date** is the update date of the game JSON file, for example if you add items, rooms, or fix some bug. You could have forgotten to specify how to get into a room from another one.

**replay_filename** is the replay filename. You can use **replay** command to replay a game that it will read this file.

When the engine describe the room you are inside than you can give a command, it execute the command and than before go on moving in another room, after he collected an item, after any action you required it can act in two ways:

 1. count for **waiting_time** seconds showing the countdown or not: it depends from the boolean value you assigned to **show_countdown**: *True* or *False*;
 2. ask to you to press **ENTER** key to continue playing.

How does it choose 1 or 2? It depends from the value of **get_new_action**. If it is **Enter Key** the game engine wait for you, so you need to press **ENTER** key when you are ready to go on. If it is **countdown** it count as told in point 1. If you remove the **get_new_action** line from the game JSON file, than it go on with the method numer 1. He prefers the countdown.

**starting_room** is the room from where the game begins. It has to contain a **room ID** as defined next.

**values** let you define some enviroment variable, for example a name or a characters sequence for a safe combination. In the example game you have two safes in two different rooms.

In the example game we have:

      "values": {
        "assigned_safe_combination": "COMEINHERE",
        "random_safe_combination": "%RANDOM(6)"
      }

Well, **assigned_safe_combination** and **random_safe_combination** are generic variable names the game is using in descriptions and safe combination you could call as you wish, also **var1** and **var2** so to have:

      "values": {
        "var1": "COMEINHERE",
        "var2": "%RANDOM(6)"
      }

Remember to replace that in the whole game JSON file.

**COMEINHERE** it’s just text. You can fill it as you wish.

**%RANDOM(6)** it’s an engine function. It means: give me a sequence of 6 random characters (numbers and upper case letters).
