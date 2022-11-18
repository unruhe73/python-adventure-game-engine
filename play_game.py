#!/usr/bin/env python3

from reading_json_game_file import ReadingJSONGameFile
from room import Room
from item import Item

import os
from time import sleep
import time

class PlayGame:
    def __init__(self):
        self.BEGIN_BOLD = '\033[1m'
        self.END_BOLD = '\033[0m'

        self.items = []
        self.rooms = []
        self.current_room = None
        self.inventory_items = []
        self.special_char = '.'
        self.you_won = False

        # parsing and loading game data
        game = ReadingJSONGameFile()
        self.game_data = game.getGameData()

        # standard texts
        self.text_cannot_find_it_into_inventory = self.game_data['text']['cannot_find_it_into_inventory']
        self.text_direction_not_available = self.game_data['text']['direction_not_available']
        self.text_dont_understand = self.game_data['text']['dont_understand']
        self.text_error_in_action_output_text_bacause_of_square = self.game_data['text']['error_in_action_output_text_bacause_of_square']
        self.text_error_in_the_description_room = self.game_data['text']['error_in_the_description_room']
        self.text_game_author = self.game_data['text']['game_author']
        self.text_game_release_date = self.game_data['text']['game_release_date']
        self.text_game_update_date = self.game_data['text']['game_update_date']
        self.text_game_license = self.game_data['text']['game_license']
        self.text_game_license_url = self.game_data['text']['game_license_url']
        self.text_help_actions = self.game_data['text']['help_actions']
        self.text_help_directions = self.game_data['text']['help_directions']
        self.text_i_cant_move_it = self.game_data['text']['i_cant_move_it']
        self.text_if_can_catch_if_is_defined_state_cannot_be_empty = self.game_data['text']['if_can_catch_if_is_defined_state_cannot_be_empty']
        self.text_inventory_is_empty = self.game_data['text']['inventory_is_empty']
        self.text_inventory_list_is_composed_by = self.game_data['text']['inventory_list_is_composed_by']
        self.text_item_not_found = self.game_data['text']['item_not_found']
        self.text_just_a_moment = self.game_data['text']['just_a_moment']
        self.text_nothing_happened = self.game_data['text']['nothing_happened']
        self.text_press_enter_to_continue = self.game_data['text']['press_enter_to_continue']
        self.text_quiting_game = self.game_data['text']['quitting_game']
        self.text_syntax_error_with_use_action = self.game_data['text']['syntax_error_with_use_action']
        self.text_there_is_a_wall = self.game_data['text']['there_is_a_wall']
        self.text_what_to_describe = self.game_data['text']['what_to_describe']
        self.text_you_are_dead = self.game_data['text']['you_are_dead']
        self.text_you_are_into_the = self.game_data['text']['you_are_into_the']
        self.text_you_cannot_catch_it = self.game_data['text']['you_cannot_catch_it']
        self.text_you_won = self.game_data['text']['you_won']

        # assign the waiting to time you can read tha command output
        self.waiting_time = int(self.game_data['waiting_time'])
        self.setWaitingTime(self.waiting_time)
        try:
            if self.game_data['get_new_action']  == 'Enter Key':
                self.get_new_action = "ENTER"
            elif self.game_data['get_new_action']  == 'countdown':
                self.get_new_action = 'countdown'
        except KeyError:
            # if you want ignore the countdown you need to add:
            # "get_new_action": "Enter Key" or you can specify
            # "get_new_action": "countdown" that is the default
            # action when "get_new_action" is absente in the JSON file
            self.get_new_action = 'countdown'

        # assign the show_countdown: True mean to see 'Just a moment: countdown'
        self.show_contdown_doesn_t_match = self.game_data['text']['show_contdown_doesn_t_match']
        if self.game_data['show_countdown'] == 'True':
            self.show_countdown = True
        elif self.game_data['show_countdown'] == 'False':
            self.show_countdown = False
        else:
            print(self.show_contdown_doesn_t_match)
            exit(1)

        # create the Item object instances and add them to the 'items' list
        for i in self.game_data['items']:
            item = Item(i['id'], i['name'])
            try:
                text = i['detailed_name']
                item.setDetailedName(text)
            except KeyError:
                # set_detailed_name not always defined
                pass
            try:
                text = i['init_state']
                item.setState(text)
            except KeyError:
                # init_state is not always defined
                pass

            try:
                when_included_in_the_room = i['when_included_in_the_room']
                item.setWhenIncludedInTheRoom(when_included_in_the_room)
            except KeyError:
                # when_included_in_the_room is not always defined
                pass

            if type(i['describe_act']) is str:
                item.setDescription(i['describe_act'])
            else:
                for j in i['describe_act']:
                    try:
                        item.setDescription(j['text'], j['state'], j['new_state'])
                    except KeyError:
                        # 'new_state' could not be always defined
                        item.setDescription(j['text'], j['state'])

                    try:
                        for elem in j['if_there_is_item']:
                            item.addItemRelatedDescription(j['state'], elem['if_item_id'],
                                elem['has_destination'], elem['than_append_description'])
                    except KeyError:
                        # not always the 'if_there_is_item' is needed
                        pass

            if type(i['catch_act']) is str:
                item.addCatchAct(i['catch_act'])
            else:
                for j in i['catch_act']:
                    try:
                        state = j['state']
                    except KeyError:
                        state = ''

                    try:
                        new_state = j['new_state']
                    except KeyError:
                        new_state = ''

                    try:
                        destination = j['destination']
                    except KeyError:
                        destination = 'room'
                        
                    try:
                        new_room_description_status = j['new_room_description_status']
                    except KeyError:
                        new_room_description_status = ''

                    try:
                        if j['death'] == 'True':
                            death = True
                        elif j['death'] == 'False':
                            death = False
                    except KeyError:
                        death = False

                    item.addCatchAct(j['text'], destination, state, new_room_description_status, new_state, death)
                    try:
                        can_catch_if = j['can_catch_if']
                        if_item_id = can_catch_if['if_item_id']
                        in_state = can_catch_if['in_state']
                        else_cannot_catch_reason_state = can_catch_if['else_cannot_catch_reason_state']
                        if not state == '':
                            # I need a real state to know if the catch action can executed or not
                            item.setCanCatchIf(state, if_item_id, in_state, else_cannot_catch_reason_state)
                        else:
                            print(self.text_if_can_catch_if_is_defined_state_cannot_be_empty)
                    except KeyError:
                        # not always 'can_catch_if' needs to be defined
                        pass
            try:
                item.setNameForInventory(i['name_for_inventory'])
            except KeyError:
                # not always you need a name_for_inventory
                pass

            try:
                if type(i['pull_act']) is str:
                    item.addPullAct(i['pull_act'])
                else:
                    for j in i['pull_act']:
                        try:
                            state = j['state']
                        except KeyError:
                            state = ''

                        try:
                            new_state = j['new_state']
                        except KeyError:
                            new_state = ''

                        try:
                            destination = j['destination']
                        except KeyError:
                            destination = 'room'

                        try:
                            new_room_description_status = j['new_room_description_status']
                        except KeyError:
                            new_room_description_status = ''

                        try:
                            if j['death'] == 'True':
                                death = True
                            elif j['death'] == 'False':
                                death = False
                        except KeyError:
                            death = False

                        item.addPullAct(j['text'], destination, state, new_room_description_status, new_state, death)
            except KeyError:
                # pull act not always defined
                pass

            try:
                if type(i['push_act']) is str:
                    item.addPushAct(i['push_act'])
                else:
                    for j in i['push_act']:
                        try:
                            state = j['state']
                        except KeyError:
                            state = ''

                        try:
                            new_state = j['new_state']
                        except KeyError:
                            new_state = ''

                        try:
                            destination = j['destination']
                        except KeyError:
                            destination = 'room'

                        try:
                            new_room_description_status = j['new_room_description_status']
                        except KeyError:
                            new_room_description_status = ''

                        try:
                            if j['death'] == 'True':
                                death = True
                            elif j['death'] == 'False':
                                death = False
                        except KeyError:
                            death = False

                        item.addPushAct(j['text'], destination, state, new_room_description_status, new_state, death)
            except KeyError:
                # pull act not always defined
                pass

            try:
                if type(i['open_act']) is str:
                    item.addOpenAct(i['open_act'])
                else:
                    for j in i['open_act']:
                        try:
                            state = j['state']
                        except KeyError:
                            state = ''

                        try:
                            new_state = j['new_state']
                        except KeyError:
                            new_state = ''

                        try:
                            destination = j['destination']
                        except KeyError:
                            destination = 'room'

                        try:
                            new_room_description_status = j['new_room_description_status']
                        except KeyError:
                            new_room_description_status = ''

                        try:
                            if j['death'] == 'True':
                                death = True
                            elif j['death'] == 'False':
                                death = False
                        except KeyError:
                            death = False

                        item.addOpenAct(j['text'], destination, state, new_room_description_status, new_state, death)
            except KeyError:
                # open act not always defined
                pass

            try:
                if type(i['close_act']) is str:
                    item.addOpenAct(i['open_act'])
                else:
                    for j in i['close_act']:
                        try:
                            state = j['state']
                        except KeyError:
                            state = ''

                        try:
                            new_state = j['new_state']
                        except KeyError:
                            new_state = ''

                        try:
                            destination = j['destination']
                        except KeyError:
                            destination = 'room'

                        try:
                            new_room_description_status = j['new_room_description_status']
                        except KeyError:
                            new_room_description_status = ''

                        try:
                            if j['death'] == 'True':
                                death = True
                            elif j['death'] == 'False':
                                death = False
                        except KeyError:
                            death = False

                        item.addCloseAct(j['text'], destination, state, new_room_description_status, new_state, death)
            except KeyError:
                # close act not always defined
                pass

            try:
                use_act = i['use_act']
                try:
                    use_alone = i['use_act']['use_alone']
                    try:
                        state = use_alone['state']
                    except KeyError:
                        # state not always define
                        state = ''
                    try:
                        new_room_description_status = use_alone['new_room_description_status']
                    except KeyError:
                        # this option not always defined
                        new_room_description_status = ''
                    try:
                        new_state = use_alone['new_state']
                    except KeyError:
                        # this option not always defined
                        new_state = ''
                    death = False
                    try:
                        if use_alone['death'] == 'True':
                            death = True
                    except KeyError:
                        # this option not always defined
                        pass
                    item.addUseAloneAct(state=state, text=use_alone['text'], new_room_description_status=new_room_description_status, new_state=new_state, death=death)
                except KeyError:
                    # use_alone not always defined
                    pass

                try:
                    for j in i['use_act']['use_with']:
                        item_id = j['item']
                        used_text = j['text']

                        try:
                            state = j['state']
                        except KeyError:
                            state = ''
                        try:
                            new_state = j['new_state']
                        except KeyError:
                            new_state = ''
                        try:
                            new_room_description_status = j['new_room_description_status']
                        except KeyError:
                            new_room_description_status = ''
                        try:
                            if j['death'] == 'True':
                                death = True
                            elif j['death'] == 'False':
                                death = False
                        except KeyError:
                            death = False

                        item.addUseWithAct(state=state, text=used_text, item=item_id, new_room_description_status=new_room_description_status, new_state=new_state, death=death)
                except KeyError:
                    # use_with not always defined
                    pass
            except KeyError:
                # use act not always defined
                pass
            self.items.append(item)

        # create the Room object instances and add them to the 'rooms' list
        for i in self.game_data['rooms']:
            room = Room(i['id'], i['name'])
            try:
                text = i['init_state']
                room.setState(text)
            except KeyError:
                # init_state is not always defined
                pass

            if type(i['description']) is str:
                room.addDescription(i['description'])
            else:
                for key in i['description'].keys():
                    room.addDescription(i['description'][key], key)

            try:
                for j in i['items']:
                    room.addItemID(j)
            except KeyError:
                # In some case a room can have no itmes inside
                pass

            room.setToNorth(i['north'])
            room.setToSouth(i['south'])
            room.setToEast(i['east'])
            room.setToWest(i['west'])

            self.rooms.append(room)

        self.game_name = self.game_data['name']
        self.game_version = self.game_data['version']
        self.game_license = self.game_data['license']
        self.game_license_url = self.game_data['license_url']
        self.game_author = self.game_data['author']
        self.game_release_date = self.game_data['release_date']
        try:
            self.game_update_date = self.game_data['update_date']
        except KeyError:
            self.game_update_date = ''

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
        self.action_close = self.game_data['actions']['close']
        self.action_describe = self.game_data['actions']['describe']
        self.action_help = self.game_data['actions']['help']
        self.action_inventory = self.game_data['actions']['inventory']
        self.action_open = self.game_data['actions']['open']
        self.action_pull = self.game_data['actions']['pull']
        self.action_push = self.game_data['actions']['push']
        self.action_quit = self.game_data['actions']['quit']
        self.action_use_verb = self.game_data['actions']['use_verb']
        self.action_use_verb_with = self.game_data['actions']['use_with']
        self.actions.extend(self.action_catch)
        self.actions.extend(self.action_close)
        self.actions.extend(self.action_describe)
        self.actions.extend(self.action_inventory)
        self.actions.extend(self.action_open)
        self.actions.extend(self.action_pull)
        self.actions.extend(self.action_push)
        self.actions.extend(self.action_quit)
        self.actions.extend(self.action_use_verb)
        self.actions.extend(self.action_help)

        # assign the Room class for the current room
        self.current_room_id = self.game_data['starting_room']
        self.current_room = self.getRoom(self.current_room_id)

        # some actions lead to death
        self.death = False

        self.winning_conditions = self.game_data['winning_conditions']

    def quitGame(self):
        print('\n' + self.text_quiting_game + '\n')
        exit(0)

    def makeBold(self, text):
        return self.BEGIN_BOLD + text + self.END_BOLD


    def printBold(self, text):
        print(self.BEGIN_BOLD + text + self.END_BOLD)


    def replaceTextWithBoldInPlaceOfStar(self, text):
        replacements = int(text.count('*') / 2)
        i = 0
        while i < replacements:
            ntext = text.replace('*', self.BEGIN_BOLD, 1)
            text = ntext.replace('*', self.END_BOLD, 1)
            i += 1
        return text


    def printTextWithBoldInPlaceOfStar(self, text):
        print(self.replaceTextWithBoldInPlaceOfStar(text))


    def printTextWithWaitingTimeInSquare(self, description):
        text = description
        full_text = ''
        count_open = text.count('[')
        count_close = text.count(']')
        if count_open == count_close:
            if count_open == 0:
                print(text)
            else:
                i = 0
                while i < count_open:
                    begin_index = text.find('[') + 1
                    end_index = text.find(']')
                    full_text += text[:begin_index - 1]
                    full_text = full_text.replace('  ', ' ').replace(' .', '.')
                    print(full_text, end='\r')
                    delay_time = int(text[begin_index:end_index])
                    sleep(delay_time)
                    text = text[end_index + 1:]
                    i += 1
                full_text += text
                full_text = full_text.replace('  ', ' ').replace(' .', '.')
                print(full_text)
        else:
            print(self.text_error_in_action_output_text_bacause_of_square)
            print(text)
            exit(1)


    def setWaitingTime(self, t):
        self.waiting_time = t


    def countdown(self):
        if self.get_new_action == "ENTER":
            try:
                input(self.text_press_enter_to_continue)
            except KeyboardInterrupt:
                self.quitGame()
        elif self.game_data['get_new_action']  == "countdown":
            seconds = self.waiting_time
            while seconds:
                if self.show_countdown:
                    timer = '{:02d}'.format(seconds)
                    print(f"{self.text_just_a_moment}: {timer}", end="\r")
                sleep(1)
                seconds -= 1


    def clearScreen(self):
        if os.name == "posix":
            os.system('clear')
        # else screen will be cleared for windows
        else:
            os.system('cls')


    def printGameDetails(self):
        print(f"\n-= {self.game_name} v{self.game_version} =-\n")
        print(f"{self.text_game_license}: {self.game_license}")
        print(f"{self.text_game_license_url}: {self.game_license_url}")
        print(f"{self.text_game_author}: {self.game_author}")
        print(f"{self.text_game_release_date}: {self.game_release_date}")
        if not self.game_update_date == '':
            print(f"{self.text_game_update_date}: {self.game_update_date}\n")
        else:
            print()


    def printHeader(self):
        header_txt = "An Adventure Game that uses Giovanni Venturi's Python Adventure Game Engine"
        size = len(header_txt)
        print((size + 4)*self.special_char)
        print(self.special_char + (size + 2)*' ' + self.special_char)
        print(f'{self.special_char} {header_txt} {self.special_char}')
        print(self.special_char + ' ' + size*' ' + ' ' + self.special_char)
        print((size + 4)*self.special_char)
        self.printGameDetails()


    def getRoom(self, room_id):
        ret = None
        room_find = False
        i = 0
        while i < len(self.rooms) and not room_find:
            if self.rooms[i].getID() == room_id:
                room_find = True
                room = self.rooms[i]
            else:
                i += 1
        if room_find:
            ret = room
        return ret


    def replaceParametersInTheRoomDescription(self, text):
        if len(self.items) == 0:
            return text

        to_replace_with = []
        for item_id in self.current_room.getItemsID():
            item = self.getItemByID(item_id)
            when_included_in_the_room = item.getWhenIncludedInTheRoom()
            if not when_included_in_the_room == '':
                to_replace_with.append(when_included_in_the_room)

        if len(to_replace_with) == 0:
            return text

        count_open = text.count('{')
        count_close = text.count('}')
        if not count_open == count_close:
            print(self.text_error_in_the_description_room + '\n')
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


    def describeRoom(self):
        head_room_text = f"{self.text_you_are_into_the} *{self.current_room.getName()}*."
        print(self.replaceTextWithBoldInPlaceOfStar(head_room_text))
        text = self.current_room.getDescription()
        if type(text) is str:
            descr = self.replaceParametersInTheRoomDescription(text)
            self.printTextWithBoldInPlaceOfStar(descr)
        else:
            text = self.current_room.getDescription()
            descr = self.replaceParametersInTheRoomDescription(text)
            self.printTextWithBoldInPlaceOfStar(descr)
        if self.checkWinning():
            print()
            print('***' + self.text_you_won)
            exit(0)


    def getItemByID(self, item_id):
        ret = None
        find_it = False
        i = 0
        while i < len(self.items) and not find_it:
            if self.items[i].getID() == item_id:
                find_it = True
                ret = self.items[i]
            else:
                i += 1
        return ret


    def getItemByNameFromRoom(self, name):
        ret = None
        find_it = False
        i = 0
        ids_list = self.current_room.getItemsID()
        while i < len(ids_list) and not find_it:
            # you need to get the object name but it has to be in the current room too
            item = self.getItemByID(ids_list[i])
            if type(name) is str:
                if item.getName() == name:
                    if item.getDestination() == 'room' or item.getDestination() == 'room_and_inventory':
                        ret = item
                    find_it = True
                else:
                    i += 1
            else:
                if not item.getDetailedName() == '':
                    if item.getDetailedNameList() == name:
                        if item.getDestination() == 'room':
                            ret = item
                        find_it = True
                    else:
                        i += 1
                else:
                    i += 1
        return ret


    def getItemByNameFromInventory(self, name):
        ret = None
        find_it = False
        i = 0
        while i < len(self.inventory_items) and not find_it:
            # you need to get the object name but it has to be in the current room too
            item = self.getItemByID(self.inventory_items[i])
            if type(name) is str:
                if item.getName() == name:
                    find_it = True
                    ret = item
                else:
                    i += 1
            else:
                if not item.getDetailedName() == '':
                    inventory_name_items = item.getDetailedName().split()
                else:
                    inventory_name_items = item.getNameForInventory().replace('*', '').split()
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


    def describeRoomItem(self, item_name):
        item = self.getItemByNameFromRoom(item_name)
        if item == None:
            if type(item_name) is str:
                text = self.makeBold(item_name)
                print(f"{self.text_item_not_found} {text}.")
            else:
                text = self.makeBold(' '.join(item_name))
                print(f"{self.text_item_not_found} {text}.")
        else:
            descr = item.getDescription()
            if descr == '':
                if type(item_name) is str:
                    text = self.makeBold(item_name)
                    print(f"{self.text_item_not_found} {text}.")
                else:
                    text = self.makeBold(' '.join(item_name))
                    print(f"{self.text_item_not_found} {text}.")
            else:
                if not item.getDestination() == 'inventory':
                    if len(item.getItemRelatedDescriptionList()) == 0:
                        print(descr)
                    else:
                        print(item.fullDescription(self.items))
                else:
                    if type(item_name) is str:
                        text = self.makeBold(item_name)
                        print(f"{self.text_item_not_found} {text}.")
                    else:
                        text = self.makeBold(' '.join(item_name))
                        print(f"{self.text_item_not_found} {text}.")


    def describeInventoryItem(self, item_name):
        item = self.getItemByNameFromInventory(item_name)
        if item == None:
            text = self.text_cannot_find_it_into_inventory
            rplc = '*' + ' '.join(item_name) + '*'
            txt = text.replace('{item}', rplc)
            text = self.replaceTextWithBoldInPlaceOfStar(txt)
            print(text)
        else:
            print(item.getDescription())


    def useItem(self, item_name, item_name_to_use_with):
        if len(item_name_to_use_with) == 0:
            # you have not to use an item in combination with another item
            if len(item_name) == 0:
                print(self.text_syntax_error_with_use_action)
            else:
                print('use ' + str(item_name) + ' alone')
        else:
            # use item with another item
            print('use ' + str(item_name) + ' with ' + str(item_name_to_use_with))


    def catchItem(self, item_name):
        item = self.getItemByNameFromRoom(item_name)
        if item == None:
            if type(item_name) is str:
                text = self.makeBold(item_name)
                print(f"{self.text_item_not_found} {text}.")
            else:
                text = self.makeBold(' '.join(item_name))
                print(f"{self.text_item_not_found} {text}.")
        else:
            can_catch = False
            if item.getCanCatchIf():
                if_can_catch = item.getCanCatchIf()
                related_item_id = if_can_catch['if_item_id']
                related_item_in_state = if_can_catch['in_state']
                related_item_cannot_reason_state = if_can_catch['else_cannot_catch_reason_state']
                related_item = self.getItemByID(related_item_id)
                if related_item.getState() == related_item_in_state:
                    can_catch = True
                else:
                    descr = related_item.getDescriptionInState(related_item_cannot_reason_state)
                    if descr == '':
                        print(self.text_if_can_catch_bad_configuration)
                        exit(1)
                    else:
                        print(self.text_you_cannot_catch_it + ' ' + related_item.getName().title() + ' ' + descr.lower())
            else:
                can_catch = True

            if can_catch:
                self.death, destination, catched_output, new_room_description_status = item.getCatchAct()
                self.printTextWithWaitingTimeInSquare(catched_output)
                if not new_room_description_status == '':
                    self.current_room.setState(new_room_description_status)
                if destination == 'inventory':
                    self.inventory_items.append(item.getID())
                    self.current_room.removeParamFromCurrentDescription(item.getID())
                elif destination == 'room_and_inventory':
                    if not item.getID() in self.inventory_items:
                        self.inventory_items.append(item.getID())
                elif destination == 'destroyed':
                    self.current_room.removeParamFromCurrentDescription(item.getID())
                item.setDestination(destination)


    def goToRoomID(self, room_id):
        if not room_id == 'none':
            room = self.getRoom(room_id)
            if room == None:
                exit(1)
            else:
                self.current_room = room
                self.current_room_id = room_id
        else:
            print(self.text_direction_not_available + ' ' + self.text_there_is_a_wall)


    def printInventory(self):
        if len(self.inventory_items) == 0:
            print(self.text_inventory_is_empty)
        else:
            print(self.text_inventory_list_is_composed_by)
            for i in self.inventory_items:
                item = self.getItemByID(i)
                name = self.replaceTextWithBoldInPlaceOfStar(item.getNameForInventory())
                print(f" '{name}'", end='')
            print()


    def goToNorth(self):
        self.goToRoomID(self.current_room.to_north)


    def goToSouth(self):
        self.goToRoomID(self.current_room.to_south)


    def goToWest(self):
        self.goToRoomID(self.current_room.to_west)


    def goToEast(self):
        self.goToRoomID(self.current_room.to_east)


    def pullItem(self, item_name):
        item = self.getItemByNameFromRoom(item_name)
        if item == None:
            if type(item_name) is str:
                text = self.makeBold(item_name)
                print(f"{self.text_item_not_found} {text}.")
            else:
                text = self.makeBold(' '.join(item_name))
                print(f"{self.text_item_not_found} {text}.")
        else:
            self.death, destination, pulled_output, new_room_description_status = item.getPullAct()
            if pulled_output == '':
                pulled_output = self.text_nothing_happened + ' ' + self.text_i_cant_move_it
            self.printTextWithWaitingTimeInSquare(pulled_output)
            if not new_room_description_status == '':
                self.current_room.setState(new_room_description_status)
            if destination == 'inventory':
                self.inventory_items.append(item.getID())
                self.current_room.removeParamFromCurrentDescription(item.getID())
            elif destination == 'room_and_inventory':
                if not item.getID() in self.inventory_items:
                    self.inventory_items.append(item.getID())
            elif destination == 'destroyed':
                self.current_room.removeParamFromCurrentDescription(item.getID())
            item.setDestination(destination)


    def pushItem(self, item_name):
        item = self.getItemByNameFromRoom(item_name)
        if item == None:
            if type(item_name) is str:
                text = self.makeBold(item_name)
                print(f"{self.text_item_not_found} {text}.")
            else:
                text = self.makeBold(' '.join(item_name))
                print(f"{self.text_item_not_found} {text}.")
        else:
            self.death, destination, pushed_output, new_room_description_status = item.getPushAct()
            if pushed_output == '':
                pushed_output = self.text_nothing_happened + ' ' + self.text_i_cant_move_it
            self.printTextWithWaitingTimeInSquare(pushed_output)
            if not new_room_description_status == '':
                self.current_room.setState(new_room_description_status)
            if destination == 'inventory':
                self.inventory_items.append(item.getID())
                self.current_room.removeParamFromCurrentDescription(item.getID())
            elif destination == 'room_and_inventory':
                if not item.getID() in self.inventory_items:
                    self.inventory_items.append(item.getID())
            elif destination == 'destroyed':
                self.current_room.removeParamFromCurrentDescription(item.getID())
            item.setDestination(destination)


    def openItem(self, item_name):
        item = self.getItemByNameFromRoom(item_name)
        if item == None:
            if type(item_name) is str:
                text = self.makeBold(item_name)
                print(f"{self.text_item_not_found} {text}.")
            else:
                text = self.makeBold(' '.join(item_name))
                print(f"{self.text_item_not_found} {text}.")
        else:
            self.death, destination, opened_output, new_room_description_status = item.getOpenAct()
            if opened_output == '':
                opened_output = self.text_nothing_happened
            self.printTextWithWaitingTimeInSquare(opened_output)
            if not new_room_description_status == '':
                self.current_room.setState(new_room_description_status)
            if destination == 'inventory':
                self.inventory_items.append(item.getID())
                self.current_room.removeParamFromCurrentDescription(item.getID())
            elif destination == 'room_and_inventory':
                if not item.getID() in self.inventory_items:
                    self.inventory_items.append(item.getID())
            elif destination == 'destroyed':
                self.current_room.removeParamFromCurrentDescription(item.getID())
            item.setDestination(destination)


    def closeItem(self, item_name):
        item = self.getItemByNameFromRoom(item_name)
        if item == None:
            if type(item_name) is str:
                text = self.makeBold(item_name)
                print(f"{self.text_item_not_found} {text}.")
            else:
                text = self.makeBold(' '.join(item_name))
                print(f"{self.text_item_not_found} {text}.")
        else:
            self.death, destination, closed_output, new_room_description_status = item.getCloseAct()
            if closed_output == '':
                closed_output = self.text_nothing_happened
            self.printTextWithWaitingTimeInSquare(closed_output)
            if not new_room_description_status == '':
                self.current_room.setState(new_room_description_status)
            if destination == 'inventory':
                self.inventory_items.append(item.getID())
                self.current_room.removeParamFromCurrentDescription(item.getID())
            elif destination == 'room_and_inventory':
                if not item.getID() in self.inventory_items:
                    self.inventory_items.append(item.getID())
            elif destination == 'destroyed':
                self.current_room.removeParamFromCurrentDescription(item.getID())
            item.setDestination(destination)


    def printHelp(self):
        print(f"\n * {self.text_help_directions}", end='')
        for item in self.directions:
           print(' ' + item, end='')
        print(f"\n * {self.text_help_actions}", end='')
        for item in self.actions:
            print(' ' + item, end='')
        print()


    def checkWinning(self):
        count = 0
        total = len(self.winning_conditions['collected_items'])
        for i in self.inventory_items:
            if i in self.winning_conditions['collected_items']:
                count += 1
        if self.winning_conditions['current_room'] == self.current_room.getID() and count == total:
            self.you_won = True
        return self.you_won


    def getAction(self):
        if not self.you_won:
            got_action = False
            while not got_action:
                self.clearScreen()
                self.printHeader()
                self.describeRoom()
                try:
                    action = input('> ')
                    print()
                except KeyboardInterrupt:
                    self.quitGame()

                verb = ''
                item = ''
                if len(action) > 0:
                    token = action.split()
                    verb = token[0]
                    item_to_use_with = []
                    if len(token) == 2:
                        item = token[1]
                    elif len(token) > 2:
                        if verb in self.action_describe:
                            if token[1] in self.action_inventory:
                                item = token[2:]
                            else:
                                item = token[1:]
                        elif verb in self.action_catch:
                            item = token[1:]
                        elif verb in self.action_use_verb:
                            if len(token) >= 4:
                                got_use_verb_with = False
                                for i in token[1:]:
                                    if i in self.action_use_verb_with:
                                        got_use_verb_with = True
                                        pos = token.index(i)
                                        item = token[1:pos]
                                        item_to_use_with = token[pos + 1:]
                                        break
                                if not got_use_verb_with:
                                    # item can be used alone too
                                    item = token[1:]
                                    item_to_use_with = []
                            else:
                                # item can be used alone too
                                got_use_verb_with = False
                                item = token[1:]
                                item_to_use_with = []

                    if verb in self.action_help:
                        self.printHelp()

                    elif verb in self.action_describe:
                        if item == '':
                            print(self.text_what_to_describe)
                        else:
                            if token[1] in self.action_inventory:
                                self.describeInventoryItem(item)
                            else:
                                self.describeRoomItem(item)
                        got_action = True

                    elif verb in self.action_use_verb:
                        self.useItem(item, item_to_use_with)

                    elif verb in self.action_catch:
                        self.catchItem(item)
                        got_action = True

                    elif verb in self.action_open:
                        self.openItem(item)
                        got_action = True

                    elif verb in self.action_close:
                        self.closeItem(item)
                        got_action = True

                    elif verb in self.action_inventory:
                        self.printInventory()
                        got_action = True

                    elif verb in self.directions_north:
                        got_action = True
                        self.goToNorth()

                    elif verb in self.directions_south:
                        got_action = True
                        self.goToSouth()

                    elif verb in self.directions_west:
                        got_action = True
                        self.goToWest()

                    elif verb in self.directions_east:
                        got_action = True
                        self.goToEast()

                    elif verb in self.action_pull:
                        self.pullItem(item)
                        got_action = True

                    elif verb in self.action_push:
                        self.pushItem(item)
                        got_action = True

                    elif verb in self.action_quit:
                        print(self.text_quiting_game + '\n')
                        exit(0)

                    else:
                        print(self.text_dont_understand)
                        self.printHelp()
                else:
                    print(self.text_dont_understand)
                    self.printHelp()

                self.countdown()


    def play(self):
        while not self.you_won and not self.death:
            self.getAction()
            if self.death:
                print(self.text_you_are_dead)
