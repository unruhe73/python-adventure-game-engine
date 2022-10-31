#!/usr/bin/env python3

from reading_json_game_file import ReadingJSONGameFile
from room import Room
from item import Item

import os
from time import sleep
import time

class PlayGame:
    def __init__(self):
        self.items = []
        self.rooms = []
        self.current_room = None
        self.won = False
        self.inventory_items = []
        self.special_char = '.'

        # parsing and loading game data
        game = ReadingJSONGameFile()
        self.game_data = game.getGameData()
        
        # assign the waiting to time you can read tha command output
        self.waiting_time = int(self.game_data['waiting_time'])
        self.assign_waiting_time(self.waiting_time)


        # create the Item object instances and add them to the 'items' list
        for i in self.game_data['items']:
           item = Item(i['id'], i['name'])
           try:
               init_state = i['init_state']
               item.set_init_state(init_state)
           # init_state is not always defined
           except KeyError:
               pass

           if type(i['describe_act']) is str:
               item.set_description(i['describe_act'])
           else:
               for j in i['describe_act']:
                   try:
                       item.set_description(j['text'], j['state'], j['new_state'])
                   except KeyError:
                       # 'new_state' could not be always defined
                       item.set_description(j['text'], j['state'])
           if type(i['catch_act']) is str:
               item.set_catch_act(i['catch_act'])
           else:
               for j in i['catch_act']:
                   item.set_catch_act(j['text'], j['state'], j['hidden_state'], j['new_room_description_status'])
           self.items.append(item)

        # create the Room object instances and add them to the 'rooms' list
        for i in self.game_data['rooms']:
           room = Room(i['id'], i['name'])
           try:
               init_state = i['init_state']
               room.set_init_state(init_state)
           # init_state is not always defined
           except KeyError:
               pass

           if type(i['description']) is str:
               room.set_description(i['description'])
           else:
               for j in i['description']:
                   room.set_description(i['description'])

           for j in i['items']:
               room.add_item_id(j)

           room.set_to_north_room(i['north'])
           room.set_to_south_room(i['south'])
           room.set_to_east_room(i['east'])
           room.set_to_west_room(i['west'])

           self.rooms.append(room)

        self.winning_room = self.game_data['winning_room']
        self.game_name = self.game_data['name']
        self.game_version = self.game_data['version']

        # directions
        self.directions = []
        self.directions_north = self.game_data['directions']['north']
        self.directions_south = self.game_data['directions']['south']
        self.directions_west = self.game_data['directions']['west']
        self.directions_east = self.game_data['directions']['east']
        self.directions.extend(self.directions_north)
        self.directions.extend(self.directions_south)
        self.directions.extend(self.directions_west)
        self.directions.extend(self.directions_east)

        # actions
        self.actions = []
        self.action_catch = self.game_data['actions']['catch']
        self.action_describe = self.game_data['actions']['describe']
        self.action_inventory = self.game_data['actions']['inventory']
        self.action_quit = self.game_data['actions']['quit']
        self.action_help = self.game_data['actions']['help']
        self.actions.extend(self.action_catch)
        self.actions.extend(self.action_describe)
        self.actions.extend(self.action_inventory)
        self.actions.extend(self.action_quit)
        self.actions.extend(self.action_help)

        # standard texts
        self.direction_not_available = self.game_data['text']['direction_not_available']
        self.dont_understand = self.game_data['text']['dont_understand']
        self.help_actions = self.game_data['text']['help_actions']
        self.help_directions = self.game_data['text']['help_directions']
        self.item_not_found = self.game_data['text']['item_not_found']
        self.just_a_moment = self.game_data['text']['just_a_moment']
        self.quiting_game = self.game_data['text']['quitting_game']
        self.what_to_describe = self.game_data['text']['what_to_describe']
        self.you_won = self.game_data['text']['you_won']

        # assign the Room class for the current room
        self.current_room_id = self.game_data['starting_room']
        self.current_room = self.get_room(self.current_room_id)
        self.description_status = list(self.current_room.get_description().keys())[0]


    def assign_waiting_time(self, t):
        self.waiting_time = t


    def countdown(self):
        seconds = self.waiting_time
        while seconds:
            timer = '{:02d}'.format(seconds)
            print(f"{self.just_a_moment}: {timer}", end="\r")
            sleep(1)
            seconds -= 1


    def clear_screen(self):
        if os.name == "posix":
            os.system('clear')
        # else screen will be cleared for windows
        else:
            os.system('cls')


    def print_game_name(self):
        print(f"\n-= {self.game_name} v.{self.game_version} =-\n")


    def print_header(self):
        header_txt = "An Adventure Game that uses Giovanni Venturi's Python Adventure Game Engine"
        size = len(header_txt)
        print((size + 4)*self.special_char)
        print(self.special_char + (size + 2)*' ' + self.special_char)
        print(f'{self.special_char} {header_txt} {self.special_char}')
        print(self.special_char + ' ' + size*' ' + ' ' + self.special_char)
        print((size + 4)*self.special_char)
        self.print_game_name()


    def get_room(self, room_id):
        ret = None
        room_find = False
        i = 0
        while i < len(self.rooms) and not room_find:
            if self.rooms[i].get_id() == room_id:
                room_find = True
                room = self.rooms[i]
            else:
                i += 1
        if room_find:
            ret = room
        return ret


    def describe_room(self):
        print(f"You are into the *{self.current_room.get_name()}*.")
        descr = self.current_room.get_description()
        if type(descr) is str:
            print(f"{self.current_room.get_description()}")
        else:
            descr = self.current_room.get_description()[self.description_status]
            print(f"{descr}")
        if self.winning_room == self.current_room.get_id():
            print(f"{self.you_won}")
            self.won = True
            exit(0)


    def get_item_by_name(self, name):
        ret = None
        find_it = False
        i = 0
        while i < len(self.items) and not find_it:
            if self.items[i].get_name() == name:
                find_it = True
                ret = self.items[i]
            else:
                i += 1
        return ret


    def describe_item(self, item_name):
        item = self.get_item_by_name(item_name)
        if item == None:
            print(f"{self.item_not_found} {item_name}.")
        else:
            descr = item.get_description()
            if descr == '':
                print(f"{self.item_not_found} {item_name}.")
            else:
                print(descr)


    def catch_item(self, item_name):
        item = self.get_item_by_name(item_name)
        if item == None:
            print(f"{self.item_not_found} {item_name}.")
        else:
            catched_output, new_room_description_status = item.get_catch_act()
            if catched_output == '':
                print(f"{self.item_not_found} {item_name}.")
            else:
                print(catched_output)
                self.description_status = new_room_description_status


    def go_to_direction(self, room_id):
        if not room_id == "none":
            room = self.get_room(room_id)
            if room == None:
                exit(1)
            else:
                self.current_room = room
                self.current_room_id = room_id
        else:
            print(f"{self.direction_not_available}")


    def go_to_north(self):
        self.go_to_direction(self.current_room.to_north)


    def go_to_south(self):
        self.go_to_direction(self.current_room.to_south)


    def go_to_west(self):
        self.go_to_direction(self.current_room.to_west)


    def go_to_east(self):
        self.go_to_direction(self.current_room.to_east)


    def print_help(self):
        print(f"\n * {self.help_directions}", end="")
        for item in self.directions:
           print(" " + item, end="")
        print(f"\n * {self.help_actions}", end="")
        for item in self.actions:
            print(" " + item, end="")
        print("")


    def get_action(self):
        if not self.won:
            got_action = False
            while not got_action:
                self.clear_screen()
                self.print_header()
                self.describe_room()
                try:
                    action = input("> ")
                except KeyboardInterrupt:
                    print(f"\n{self.quiting_game}\n")
                    exit(1)

                verb = ''
                item = ''
                if len(action) > 0:
                    token = action.split()
                    verb = token[0]
                    if len(token) == 2:
                        item = token[1]

                    if verb in self.action_help:
                        self.print_help()

                    elif verb in self.action_describe:
                        if item == '':
                            print(f"{self.what_to_describe}")
                        else:
                            self.describe_item(item)
                        got_action = True

                    elif verb in self.action_catch:
                        self.catch_item(item)
                        got_action = True

                    elif verb in self.action_inventory:
                        print(self.inventory_items)
                        got_action = True

                    elif verb in self.directions_north:
                        got_action = True
                        self.go_to_north()

                    elif verb in self.directions_south:
                        got_action = True
                        self.go_to_south()

                    elif verb in self.directions_west:
                        got_action = True
                        self.go_to_west()

                    elif verb in self.directions_east:
                        got_action = True
                        self.go_to_east()

                    elif verb in self.action_quit:
                        print(f"{self.quiting_game}\n")
                        exit(0)

                    else:
                        print(f"{self.dont_understand}")
                        self.print_help()
                else:
                    print(f"{self.dont_understand}")
                    self.print_help()

                print("")
                self.countdown()


    def play(self):
        while not self.won:
            self.get_action()