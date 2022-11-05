#!/usr/bin/env python3

from reading_json_game_file import ReadingJSONGameFile
from room import Room
from item import Item

import os
from time import sleep
import time

class PlayGame:
    def __init__(self):
        self.START_BOLD = '\033[1m'
        self.END_BOLD = '\033[0m'

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

        # assign the show_countdown: True mean to see "Just a moment: countdown"
        if self.game_data['show_countdown'] == 'True':
            self.show_countdown = True
        elif self.game_data['show_countdown'] == 'False':
            self.show_countdown = False

        # create the Item object instances and add them to the 'items' list
        for i in self.game_data['items']:
            item = Item(i['id'], i['name'])
            try:
                text = i['detailed_name']
                item.set_detailed_name(text)
            except KeyError:
                # set_detailed_name not always defined
                pass
            try:
                text = i['init_state']
                item.set_state(text)
            except KeyError:
                # init_state is not always defined
                pass

            try:
                when_included_in_the_room = i['when_included_in_the_room']
                item.set_when_included_in_the_room(when_included_in_the_room)
            except KeyError:
                # when_included_in_the_room is not always defined
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
                    try:
                        state = j['state']
                    except KeyError:
                        state = ''
                    destination = j['destination']

                    try:
                        new_room_description_status = j['new_room_description_status']
                    except KeyError:
                        new_room_description_status = ''
                    item.set_catch_act(j['text'], destination, state, new_room_description_status)
            try:
                item.set_name_for_inventory(i['name_for_inventory'])
            except KeyError:
                # not always you need a name_for_inventory
                pass
            self.items.append(item)

        # create the Room object instances and add them to the 'rooms' list
        for i in self.game_data['rooms']:
            room = Room(i['id'], i['name'])
            try:
                text = i['init_state']
                room.set_state(text)
            except KeyError:
                # init_state is not always defined
                pass

            if type(i['description']) is str:
                room.add_description(i['description'])
            else:
                for key in i['description'].keys():
                    room.add_description(i['description'][key], key)

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
        self.game_license = self.game_data['license']
        self.game_license_url = self.game_data['license_url']
        self.game_author = self.game_data['author']
        self.game_date = self.game_data['date']

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
        self.cannot_find_it_into_inventory = self.game_data['text']['cannot_find_it_into_inventory']
        self.direction_not_available = self.game_data['text']['direction_not_available']
        self.dont_understand = self.game_data['text']['dont_understand']
        self.error_in_the_description_room = self.game_data['text']['error_in_the_description_room']
        self.game_author_string = self.game_data['text']['game_author']
        self.game_date_string = self.game_data['text']['game_date']
        self.game_license_string = self.game_data['text']['game_license']
        self.game_license_url_string = self.game_data['text']['game_license_url']
        self.help_actions = self.game_data['text']['help_actions']
        self.help_directions = self.game_data['text']['help_directions']
        self.inventory_is_empty = self.game_data['text']['inventory_is_empty']
        self.inventory_list_is_composed_by = self.game_data['text']['inventory_list_is_composed_by']
        self.item_not_found = self.game_data['text']['item_not_found']
        self.just_a_moment = self.game_data['text']['just_a_moment']
        self.quiting_game = self.game_data['text']['quitting_game']
        self.what_to_describe = self.game_data['text']['what_to_describe']
        self.you_are_into_the = self.game_data['text']['you_are_into_the']
        self.you_won = self.game_data['text']['you_won']

        # assign the Room class for the current room
        self.current_room_id = self.game_data['starting_room']
        self.current_room = self.get_room(self.current_room_id)


    def print_bold(self, text):
        print(TEXT_BOLD + text + END_BOLD)


    def replace_text_with_bold_in_place_of_star(self, text):
        replacements = int(text.count('*') / 2)
        i = 0
        while i < replacements:
            ntext = text.replace('*', self.START_BOLD, 1)
            text = ntext.replace('*', self.END_BOLD, 1)
            i += 1
        return text


    def print_text_with_bold_in_place_of_star(self, text):
        print(self.replace_text_with_bold_in_place_of_star(text))


    def assign_waiting_time(self, t):
        self.waiting_time = t


    def countdown(self):
        seconds = self.waiting_time
        while seconds:
            if self.show_countdown:
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


    def print_game_details(self):
        print(f"\n-= {self.game_name} v.{self.game_version} =-\n")
        print(f"{self.game_license_string}: {self.game_license}")
        print(f"{self.game_license_url_string}: {self.game_license_url}")
        print(f"{self.game_author_string}: {self.game_author}")
        print(f"{self.game_date_string}: {self.game_date}\n")


    def print_header(self):
        header_txt = "An Adventure Game that uses Giovanni Venturi's Python Adventure Game Engine"
        size = len(header_txt)
        print((size + 4)*self.special_char)
        print(self.special_char + (size + 2)*' ' + self.special_char)
        print(f'{self.special_char} {header_txt} {self.special_char}')
        print(self.special_char + ' ' + size*' ' + ' ' + self.special_char)
        print((size + 4)*self.special_char)
        self.print_game_details()


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


    def replace_parameters_in_the_room_description(self, text):
        if len(self.items) == 0:
            return text

        to_replace_with = []
        for item in self.items:
            item_ids = [ self.current_room.items[i]['item_id'] for i in range(len(self.current_room.items)) ]
            if item.get_id() in item_ids:
                when_included_in_the_room = item.get_when_included_in_the_room()
                if not when_included_in_the_room == '':
                    pos = item_ids.index(item.get_id())
                    if self.current_room.items[pos]['visible']:
                        to_replace_with.append(when_included_in_the_room)
                    else:
                        to_replace_with.append('')


        if len(to_replace_with) == 0:
            return text

        count_open = text.count('{')
        count_close = text.count('}')
        if not count_open == count_close:
            print(self.error_in_the_description_room + '\n')
            exit(1)
        param_begin_index = 0
        ids = []
        i = 0
        while i < count_open:
            param_begin_index = text.find('{', param_begin_index) + 1
            param_end_index = text.find('}', param_begin_index)
            param = text[param_begin_index:param_end_index]
            ids.append(param)
            param_begin_index = param_end_index + 1
            i += 1
        i = 0
        while i < len(ids):
            txt = text.replace('{' + ids[i] + '}', to_replace_with[i], 1)
            text = txt
            i += 1
        text = text.replace('  ', ' ').replace(' .', '.').replace('..', '.')
        return text


    def describe_room(self):
        head_room_text = f"{self.you_are_into_the} *{self.current_room.get_name()}*."
        print(self.replace_text_with_bold_in_place_of_star(head_room_text))
        text = self.current_room.get_description()
        if type(text) is str:
            descr = self.replace_parameters_in_the_room_description(text)
            self.print_text_with_bold_in_place_of_star(descr)
        else:
            text = self.current_room.get_description()
            descr = self.replace_parameters_in_the_room_description(text)
            self.print_text_with_bold_in_place_of_star(descr)
        if self.winning_room == self.current_room.get_id():
            print(f"{self.you_won}")
            self.won = True
            exit(0)


    def get_item_by_id(self, item_id):
        ret = None
        find_it = False
        i = 0
        while i < len(self.items) and not find_it:
            if self.items[i].get_id() == item_id:
                find_it = True
                ret = self.items[i]
            else:
                i += 1
        return ret


    def get_item_by_name(self, name):
        ret = None
        find_it = False
        i = 0
        while i < len(self.items) and not find_it:
            # you need to get the object name but it has to be in the current room too
            item_ids = [ self.current_room.items[i]['item_id'] for i in range(len(self.current_room.items)) ]
            if self.items[i].get_name() == name and self.items[i].get_id() in item_ids and not self.items[i].destination == 'destroyed':
                find_it = True
                ret = self.items[i]
            else:
                i += 1
        return ret


    def get_item_by_name_from_inventory(self, name):
        ret = None
        find_it = False
        i = 0
        while i < len(self.inventory_items) and not find_it:
            # you need to get the object name but it has to be in the current room too
            item = self.get_item_by_id(self.inventory_items[i])
            if type(name) is str:
                if item.get_name() == name:
                    find_it = True
                    ret = item
                else:
                    i += 1
            else:
                if not item.get_detailed_name() == '':
                    inventory_name_items = item.get_detailed_name().split()
                else:
                    inventory_name_items = item.get_name_for_inventory().replace('*', '').split()
                condition = True
                n = len(name)
                j = 0
                quit_from_for = False
                while j < n and not quit_from_for:
                    if not name[j] in inventory_name_items:
                        condition = False
                        quit_from_for = True
                    j += 1
                if condition:
                    find_it = True
                    ret = item
                else:
                    i += 1
        return ret


    def describe_room_item(self, item_name):
        item = self.get_item_by_name(item_name)
        if item == None:
            if type(item_name) is str:
                print(f"{self.item_not_found} {item_name}.")
            else:
                print(f"{self.item_not_found} {' '.join(item_name)}.")
        else:
            descr = item.get_description()
            if descr == '':
                if type(item_name) is str:
                    print(f"{self.item_not_found} {item_name}.")
                else:
                    print(f"{self.item_not_found} {' '.join(item_name)}.")
            else:
                if not item.get_destination() == 'inventory':
                    print(descr)
                else:
                    if type(item_name) is str:
                        print(f"{self.item_not_found} {item_name}.")
                    else:
                        print(f"{self.item_not_found} {' '.join(item_name)}.")


    def describe_inventory_item(self, item_name):
        item = self.get_item_by_name_from_inventory(item_name)
        if item == None:
            text = self.cannot_find_it_into_inventory
            rplc = '*' + ' '.join(item_name) + '*'
            txt = text.replace('{item}', rplc)
            text = self.replace_text_with_bold_in_place_of_star(txt)
            print(text)
        else:
            print(item.get_description())


    def catch_item(self, item_name):
        item = self.get_item_by_name(item_name)
        if item == None:
            print(f"{self.item_not_found} {item_name}.")
        else:
            if item.get_destination() == 'inventory':
                print(f"{self.item_not_found} {item_name}.")
            else:
                destination, catched_output, new_room_description_status = item.get_catch_act()
                if catched_output == '':
                    print(f"{self.item_not_found} {item_name}.")
                else:
                    print(catched_output)
                    if not new_room_description_status == '':
                        self.current_room.set_state(new_room_description_status)
                    if destination == 'inventory':
                        self.inventory_items.append(item.get_id())
                        self.current_room.remove_item(item.get_id())
                        item.set_destination(destination)
                    elif destination == 'destroyed':
                        item.set_destination(destination)
                        self.current_room.remove_item(item.get_id())
                        item.set_destination(destination)


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


    def print_inventory(self):
        if len(self.inventory_items) == 0:
            print(self.inventory_is_empty)
        else:
            print(self.inventory_list_is_composed_by)
            for i in self.inventory_items:
                item = self.get_item_by_id(i)
                name = self.replace_text_with_bold_in_place_of_star(item.get_name_for_inventory())
                print(f" '{name}'", end='')
            print()


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
                    print()
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
                    elif len(token) > 2:
                        if verb in self.action_describe:
                            if token[1] in self.action_inventory:
                                item = token[2:]
                            else:
                                item = token[1:]

                    if verb in self.action_help:
                        self.print_help()

                    elif verb in self.action_describe:
                        if item == '':
                            print(f"{self.what_to_describe}")
                        else:
                            if token[1] in self.action_inventory:
                                self.describe_inventory_item(item)
                            else:
                                self.describe_room_item(item)
                        got_action = True

                    elif verb in self.action_catch:
                        self.catch_item(item)
                        got_action = True

                    elif verb in self.action_inventory:
                        self.print_inventory()
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

                self.countdown()


    def play(self):
        while not self.won:
            self.get_action()
