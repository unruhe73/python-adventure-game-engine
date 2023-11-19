#!/usr/bin/env python3

from reading_json_game_file import ReadingJSONGameFile
from room import Room
from item import Item

from game_sound_system import GameSoundSystem

import os
from time import sleep
import time
import random


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
        self.game_started = False

        # parsing and loading game data
        game = ReadingJSONGameFile()
        self.game_data = game.getGameData()

        # standard texts
        self.text_assignment_value_error_for_key = self.game_data['text']['assignment_value_error_for_key']
        self.text_cant_create_replay_file = self.game_data['text']['cant_create_replay_file']
        self.text_cant_find_it_into_inventory = self.game_data['text']['cant_find_it_into_inventory']
        self.text_cant_read_replay_file = self.game_data['text']['cant_read_replay_file']
        self.text_cant_replay_during_game = self.game_data['text']['cant_replay_during_game']
        self.text_direction_not_available = self.game_data['text']['direction_not_available']
        self.text_dont_understand = self.game_data['text']['dont_understand']
        self.text_error_in_action_output_text_bacause_of_square = self.game_data['text']['error_in_action_output_text_bacause_of_square']
        self.text_error_in_the_description_room = self.game_data['text']['error_in_the_description_room']
        self.text_game_author_name = self.game_data['text']['game_author_name']
        self.text_game_author_contact = self.game_data['text']['game_author_contact']
        self.text_game_author_github = self.game_data['text']['game_author_github']
        self.text_game_release_date = self.game_data['text']['game_release_date']
        self.text_game_update_date = self.game_data['text']['game_update_date']
        self.text_game_license = self.game_data['text']['game_license']
        self.text_game_license_url = self.game_data['text']['game_license_url']
        self.text_game_sound_off = self.game_data['text']['game_sound_off']
        self.text_game_sound_on = self.game_data['text']['game_sound_on']
        self.text_help_actions = self.game_data['text']['help_actions']
        self.text_help_directions = self.game_data['text']['help_directions']
        self.text_i_cant_move_it = self.game_data['text']['i_cant_move_it']
        self.text_i_dont_know_what_to_do = self.game_data['text']['i_dont_know_what_to_do']
        self.text_i_cant_catch_it = self.game_data['text']['i_cant_catch_it']
        self.text_i_got_confused_about_direction = self.game_data['text']['i_got_confused_about_direction']
        self.text_i_havent_got = self.game_data['text']['i_havent_got']
        self.text_if_can_catch_if_is_defined_state_cant_be_empty = self.game_data['text']['if_can_catch_if_is_defined_state_cant_be_empty']
        self.text_inventory_is_empty = self.game_data['text']['inventory_is_empty']
        self.text_inventory_list_is_composed_by = self.game_data['text']['inventory_list_is_composed_by']
        self.text_item_not_found = self.game_data['text']['item_not_found']
        self.text_just_a_moment = self.game_data['text']['just_a_moment']
        self.text_nothing_happened = self.game_data['text']['nothing_happened']
        self.text_press_enter_to_continue = self.game_data['text']['press_enter_to_continue']
        self.text_quiting_game = self.game_data['text']['quitting_game']
        self.text_replaying_game = self.game_data['text']['replaying_game']
        self.text_syntax_error_with_use_action = self.game_data['text']['syntax_error_with_use_action']
        self.text_there_is_a_wall = self.game_data['text']['there_is_a_wall']
        self.text_there_is_also = self.game_data['text']['there_is_also']
        self.text_type_a_combination_to_open = self.game_data['text']['type_a_combination_to_open']
        self.text_what_to_describe = self.game_data['text']['what_to_describe']
        self.text_wrong_combination = self.game_data['text']['wrong_combination']
        self.text_you_are_dead = self.game_data['text']['you_are_dead']
        self.text_you_are_into_the = self.game_data['text']['you_are_into_the']
        self.text_you_cant_catch_it = self.game_data['text']['you_cant_catch_it']
        self.text_you_need_item_xyz = self.game_data['text']['you_need_item_xyz']
        self.text_you_cant_open_it = self.game_data['text']['you_cant_open_it']
        self.text_you_won = self.game_data['text']['you_won']
        self.text_your_combination = self.game_data['text']['your_combination']

        # Enable Game Sound System if it's specified in the game JSON file
        try:
            sound_system_status = self.game_data['sound_system']
        except KeyError:
            sound_system_status = 'Off'
        self.game_sound_system = GameSoundSystem(sound_system_status)
        try:
            self.game_sound_system.assignSoundDirectory(self.game_data['sounds_files_directory_name'])
        except KeyError:
            self.game_sound_system.setStatus('Off')

        for sound_file_id, sound_file_name in self.game_data['sounds'].items():
            self.game_sound_system.assignSoundFilename(sound_file_id, sound_file_name)

        try:
            self.starting_sound_id = self.game_data['starting_sound_id']
        except KeyError:
            self.starting_sound_id = ''

        # assigned text values
        self.assigned_values = self.game_data['values']
        for k in self.assigned_values.keys():
            self.assigned_values[k] = self.getValue(self.assigned_values[k])

        # assign the 'waiting time' seconds: seconds to wait
        # before you can type a new command
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
            # because "countdown" is the default value of "get_new_action"
            # and it's used when it's not in the JSON file
            self.get_new_action = 'countdown'

        # assign the show_countdown: true means you're going to see: 'Just a moment: *countdown act* before a new action can be executed'
        self.show_countdown = self.game_data['show_countdown']

        # create the Item object instances and add them to the 'items' list
        for i in self.game_data['items']:
            item = Item(i['id'], i['name'])
            try:
                text = i['detailed_name']
                item.setDetailedName(text)
            except KeyError:
                # set_detailed_name not always defined
                item.setDetailedName(i['name'])
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

            try:
                assigned_text = i['assigned_text']
                for k in assigned_text.keys():
                    evaluated_value = self.getValue(assigned_text[k])
                    item.assignOriginalTextToKey(assigned_text[k], k)
                    item.assignTextToKey(evaluated_value, k)
            except KeyError:
                # 'assigned_text' is not always defined
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
                            try:
                                item.addItemRelatedDescription(j['state'], elem['if_item_id'],
                                    elem['has_destination'], elem['than_append_description'],
                                    elem['add_item_to_room_id'])
                            except KeyError:
                                # add_item_to_room_id it's not always defined
                                item.addItemRelatedDescription(j['state'], elem['if_item_id'],
                                    elem['has_destination'], elem['than_append_description'])
                    except KeyError:
                        # not always the 'if_there_is_item' is needed
                        pass

            try:
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
                            death = j['death']
                        except KeyError:
                            death = False

                        try:
                            sound_id = j['sound_id']
                        except:
                            sound_id = ''

                        item.addCatchAct(j['text'], destination, state, new_room_description_status, new_state, death, sound_id)
                        try:
                            can_catch_if = j['can_catch_if']
                            if_item_id = can_catch_if['if_item_id']
                            in_state = can_catch_if['in_state']
                            else_cant_catch_reason_state = can_catch_if['else_cant_catch_reason_state']
                            if state:
                                # I need a real state to know if the catch action can executed or not
                                item.setCanCatchIf(state, if_item_id, in_state, else_cant_catch_reason_state)
                            else:
                                print(self.text_if_can_catch_if_is_defined_state_cant_be_empty)
                        except KeyError:
                            # not always 'can_catch_if' needs to be defined
                            pass
            except KeyError:
                # catch act is not always defined
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
                            death = j['death']
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
                            death = j['death']
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
                            sound_id = j['sound_id']
                        except KeyError:
                            sound_id = ''

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
                            death = j['death']
                        except KeyError:
                            death = False

                        # if you need a condition to open:
                        #  you could need a combination:
                        # "to_open": {
                        #   "method": "combination",
                        #   "value": "%my_combination_value",
                        #   "attempts": "3"
                        # }
                        # or an item into the inventory:
                        # "to_open": {
                        #   "method": "item_in_inventory",
                        #   "used_with_item": "key_room_08"
                        # }
                        try:
                            original_value = ''
                            value = ''
                            attempts = 0
                            used_with_item = ''
                            to_open = j['to_open']
                            method = to_open['method']
                            if method == 'combination':
                                original_value = to_open['value']
                                value = self.getValue(to_open['value'])
                                attempts = to_open['attempts']
                            elif method == 'item_in_inventory':
                                used_with_item = to_open['used_with_item']
                            item.assignToOpenCondition(state, method, original_value, value, attempts, used_with_item)
                        except KeyError:
                            # just in case of a 'safe' or 'doors' item or similar you can have an access condition
                            pass
                        item.addOpenAct(j['text'], destination, state, new_room_description_status, new_state, death, sound_id)
            except KeyError:
                # open act not always defined
                pass

            try:
                if type(i['close_act']) is str:
                    item.addCloseAct(i['close_act'])
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
                            death = j['death']
                        except KeyError:
                            death = False

                        try:
                            for elem in j['if_there_is_item']:
                                try:
                                    item.addItemRelatedCloseAct(j['state'], elem['if_item_id'],
                                        elem['has_destination'], '', elem['remove_item_from_room_id'])
                                except KeyError:
                                    # remove_item_from_room_id it's not always defined
                                    item.addItemRelatedCloseAct(j['state'], elem['if_item_id'],
                                        elem['has_destination'], '', '')
                        except KeyError:
                            # not always the 'if_there_is_item' is needed
                            pass

                        item.addCloseAct(j['text'], destination, state, new_room_description_status, new_state, death)
            except KeyError:
                # close act not always defined
                pass

            try:
                use_act = i['use_act']
                try:
                    for j in use_act['use_alone']:
                        try:
                            state = j['state']
                        except KeyError:
                            # state not always define
                            state = ''
                        try:
                            new_room_description_status = j['new_room_description_status']
                        except KeyError:
                            # this option not always defined
                            new_room_description_status = ''
                        try:
                            new_state = j['new_state']
                        except KeyError:
                            # this option not always defined
                            new_state = ''
                        death = False
                        try:
                            death = j['death']
                        except KeyError:
                            # this option not always defined
                            pass
                        item.addUseAloneAct(text=j['text'], state=state, new_room_description_status=new_room_description_status, new_state=new_state, death=death)
                except KeyError:
                    # use_alone not always defined
                    pass

                try:
                    for j in use_act['use_with']:
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
                            death = j['death']
                        except KeyError:
                            death = False
                        try:
                            after_use = j['after_use']
                        except KeyError:
                            after_use = ''
                        try:
                            status = j['status']
                        except KeyError:
                            status = ''
                        item.addUseWithAct(text=used_text, item=item_id, state=state, new_room_description_status=new_room_description_status, new_state=new_state, death=death, status=status, after_use=after_use)
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

            try:
                text_sound_id = i['enter_sound_id']
                room.setEnterSoundID(text_sound_id)
            except KeyError:
                # you not always there is an enter sound ID
                pass

            self.rooms.append(room)

        self.game_name = self.game_data['name']
        self.game_version = self.game_data['version']
        self.game_license = self.game_data['license']
        self.game_license_url = self.game_data['license_url']
        self.game_author_name = self.game_data['author_name']
        try:
            self.game_author_contact = self.game_data['author_contact']
        except KeyError:
            # it's an option information
            self.game_author_contact = ""
            pass
        try:
            self.game_author_github = self.game_data['author_github']
        except KeyError:
            # it's an optional information
            self.game_author_github = ""
            pass
        self.game_release_date = self.game_data['release_date']
        try:
            self.game_update_date = self.game_data['update_date']
        except KeyError:
            self.game_update_date = ''

        self.replaying = False
        self.game_running = False
        self.just_replayed = False
        try:
            infoname = self.game_data['replay_filename']
            replay_filename = infoname.split(os.sep)[-1]
        except KeyError:
            replay_filename = game.getFileName().split(os.sep)[-1] + '.replay'

        if not os.path.exists('replays'):
            os.makedirs('replays')
        self.replay_filename = os.path.join('replays', replay_filename)

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

        # load the winning conditions
        self.winning_conditions = self.game_data['winning_conditions']


    def getValue(self, text):
        text = text.strip()
        digits = '0123456789'
        letters = 'QWERTYUIOPASDFGHJKLZXCVBNM'
        sequence = letters + digits
        if text.count('%RANDOM(') == 1:
            length = int(text[8:len(text) - 1])
            value = ''
            for x in range(0, length):
                value += random.choice(sequence)
            text = value
        elif text.count('%') > 0:
            index = 0
            sequence += '_'
            while index < len(text):
                # it's in the text assigned format: %text_assigned_name
                index = text.find('%') + 1
                name = ''
                quit = False
                replaceDoublePerCent = False
                while not quit and index < len(text):
                    if text[index].upper() in sequence:
                        name += text[index]
                    elif text[index] == '%':
                        replaceDoublePerCent = True
                        quit = True
                    else:
                        quit = True
                    index += 1
                if replaceDoublePerCent:
                    text = text.replace('%%', '%')
                    index += 1
                else:
                    try:
                        text = text.replace('%' + name, self.assigned_values[name])
                    except KeyError:
                        print(self.makeBold(name) + ' '
                            + self.replaceTextWithBoldInPlaceOfStar(self.text_assignment_value_error_for_key))
                        self.quitGame(1)
        return text


    def quitGame(self, exit_code=0):
        if exit_code == 0:
            print('\n' + self.text_quiting_game + '\n')
        try:
            self.replay_file.close()
        except:
            pass
        exit(exit_code)


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


    def cleanText(self, text):
        return text.replace('  ', ' ').replace(' .', '.').replace('..', '.').replace(', .','.')


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
                    full_text = self.cleanText(full_text)
                    print(full_text, end='\r')
                    delay_time = int(text[begin_index:end_index])
                    sleep(delay_time)
                    text = text[end_index + 1:]
                    i += 1
                full_text += text
                full_text = self.cleanText(full_text)
                print(full_text)
        else:
            print(self.text_error_in_action_output_text_bacause_of_square)
            print(text)
            self.quitGame(1)


    def setWaitingTime(self, t):
        self.waiting_time = t


    def countdown(self):
        if self.replaying:
            seconds = self.waiting_time - 2
            try:
                while seconds:
                    timer = '{:02d}'.format(seconds)
                    print(f"{self.text_just_a_moment}: {timer}", end="\r")
                    sleep(1)
                    seconds -= 1
            except KeyboardInterrupt:
                self.quitGame()
        else:
            if self.get_new_action == "ENTER":
                try:
                    input(self.text_press_enter_to_continue)
                except KeyboardInterrupt:
                    self.quitGame()
            elif self.game_data['get_new_action']  == "countdown":
                seconds = self.waiting_time
                try:
                    while seconds:
                        if self.show_countdown:
                            timer = '{:02d}'.format(seconds)
                            print(f"{self.text_just_a_moment}: {timer}", end="\r")
                        sleep(1)
                        seconds -= 1
                except KeyboardInterrupt:
                    self.quitGame()


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
        print(f"{self.text_game_author_name}: {self.game_author_name}")
        if self.game_author_contact:
            print(f"{self.text_game_author_contact}: {self.game_author_contact}")
        if self.game_author_github:
            print(f"{self.text_game_author_github}: {self.game_author_github}")
        print(f"{self.text_game_release_date}: {self.game_release_date}")
        if self.game_update_date:
            print(f"{self.text_game_update_date}: {self.game_update_date}")
        if self.game_sound_system.isEnabled():
            print(f"{self.text_game_sound_on}")
        else:
            print(f"{self.text_game_sound_off}")
        print()
        if not self.game_started:
            if self.current_room.hasEnterSoundID():
                self.game_sound_system.play(self.current_room.enterSoundID())
            else:
                self.game_sound_system.play(self.starting_sound_id, 3)
            self.game_started = True


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
            if when_included_in_the_room:
                to_replace_with.append(when_included_in_the_room)

        if len(to_replace_with) == 0:
            count_open = text.count('{')
            count_close = text.count('}')
            if not count_open == count_close:
                print(self.text_error_in_the_description_room + '\n')
                self.quitGame(1)
            sIndex = text.find('{')
            eIndex = text.find('}')
            if sIndex > -1 and eIndex > -1:
                to_replace = text[sIndex : eIndex + 1]
                text = text.replace(to_replace, '')
                text = self.cleanText(text)
            return text

        count_open = text.count('{')
        count_close = text.count('}')
        if not count_open == count_close:
            print(self.text_error_in_the_description_room + '\n')
            self.quitGame(1)
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
        text = self.cleanText(text)
        return text


    def describeRoom(self):
        head_room_text = f"{self.text_you_are_into_the} *{self.current_room.getName()}*."
        print(self.replaceTextWithBoldInPlaceOfStar(head_room_text))
        text = self.current_room.getDescription()
        descr = self.replaceParametersInTheRoomDescription(text)
        self.printTextWithBoldInPlaceOfStar(descr)
        if self.checkWinning():
            print()
            print('***' + self.text_you_won)
            self.quitGame()


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
                if item.getDetailedName():
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
                if item.getDetailedName():
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
        if not item:
            if type(item_name) is str:
                text = self.makeBold(item_name)
                print(f"{self.text_item_not_found} {text}.")
            else:
                text = self.makeBold(' '.join(item_name))
                print(f"{self.text_item_not_found} {text}.")
        else:
            descr = item.getDescription()
            if not descr:
                if type(item_name) is str:
                    text = self.makeBold(item_name)
                    print(f"{self.text_item_not_found} {text}.")
                else:
                    text = self.makeBold(' '.join(item_name))
                    print(f"{self.text_item_not_found} {text}.")
            else:
                if not item.getDestination() == 'inventory':
                    if len(item.getItemRelatedDescriptionList()) == 0:
                        if item.isAggregatedItemsAvailable():
                            print(self.replaceTextWithBoldInPlaceOfStar(item.fullDescription(self.items)))
                        else:
                            print(descr)
                    else:
                        if item.isAddItemToRoomDefined():
                            if self.current_room.getID() == item.getRoomIDInWhichToAddRelatedItem(self.items):
                                self.current_room.addItemID(item.getIfIitemIDforDescription(self.items))
                        print(self.replaceTextWithBoldInPlaceOfStar(item.fullDescription(self.items)))
                else:
                    if type(item_name) is str:
                        text = self.makeBold(item_name)
                        print(f"{self.text_item_not_found} {text}.")
                    else:
                        text = self.makeBold(' '.join(item_name))
                        print(f"{self.text_item_not_found} {text}.")


    def describeInventoryItem(self, item_name):
        item = self.getItemByNameFromInventory(item_name)
        if not item:
            text = self.text_cant_find_it_into_inventory
            rplc = '*' + ' '.join(item_name) + '*'
            txt = text.replace('{item}', rplc)
            text = self.replaceTextWithBoldInPlaceOfStar(txt)
            print(text)
        else:
            print(item.getDescription())


    def useItem(self, item_name, item_name_used_with):
        if len(item_name_used_with) == 0:
            # you have not to use an item in combination with another item
            if len(item_name) == 0:
                print(self.text_syntax_error_with_use_action)
            else:
                # the first item has to be in your inventory
                item = self.getItemByNameFromInventory(item_name)
                if not item:
                    if type(item_name) is str:
                        print(self.text_i_havent_got + ' ' + self.makeBold(item_name) + '.')
                    else:
                        print(self.text_i_havent_got + ' ' + self.makeBold(' '.join(item_name)) + '.')
                else:
                    self.death, used_alone_text, new_room_description_status = item.getUseAloneAct()
                    if used_alone_text:
                        self.printTextWithWaitingTimeInSquare(used_alone_text)
                    else:
                        print(self.text_i_dont_know_what_to_do)
        else:
            # use item with another item
            if len(item_name) == 0:
                print(self.text_syntax_error_with_use_action)
            else:
                # the first item has to be in your inventory
                item = self.getItemByNameFromInventory(item_name)
                if not item:
                    if type(item_name) is str:
                        print(self.text_i_havent_got + ' ' + self.makeBold(item_name) + '.')
                    else:
                        print(self.text_i_havent_got + ' ' + self.makeBold(' '.join(item_name)) + '.')
                else:
                    item_with = self.getItemByNameFromInventory(item_name_used_with)
                    if not item_with:
                        # look for it into the room
                        item_with = self.getItemByNameFromRoom(item_name_used_with)
                        if not item_with:
                            text = self.text_item_not_found
                            if type(item_name_used_with) is str:
                                text += ' ' + makeBold(item_name_used_with) + '.'
                            else:
                                text += ' ' + self.makeBold(' '.join(item_name_used_with)) + '.'
                            print(text)
                    if item_with:
                        self.death, used_with_text, new_room_description_status, to_aggregate = item.getUseWithAct(item_with.getID())
                        if used_with_text:
                            self.printTextWithWaitingTimeInSquare(used_with_text)
                            if to_aggregate:
                                if item.getID() in self.inventory_items:
                                    self.inventory_items.remove(item.getID())
                                    item_with.addToAggregateList(item.getID())
                        else:
                            print(self.text_i_dont_know_what_to_do)


    def catchItem(self, item_name):
        item = self.getItemByNameFromRoom(item_name)
        if not item:
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
                related_item_cant_reason_state = if_can_catch['else_cant_catch_reason_state']
                related_item = self.getItemByID(related_item_id)
                if related_item.getState() == related_item_in_state:
                    can_catch = True
                else:
                    descr = related_item.getDescriptionInState(related_item_cant_reason_state)
                    if not descr:
                        print(self.text_if_can_catch_bad_configuration)
                        self.quitGame(1)
                    else:
                        print(self.text_you_cant_catch_it + ' ' + related_item.getName().title() + ' ' + descr.lower())
            else:
                can_catch = item.canCatch()

            if can_catch:
                self.death, destination, catched_output, new_room_description_status, sound_id = item.getCatchAct()
                self.printTextWithWaitingTimeInSquare(catched_output)
                if new_room_description_status:
                    self.current_room.setState(new_room_description_status)
                if destination == 'inventory':
                    self.inventory_items.append(item.getID())
                    self.current_room.removeParamFromCurrentDescription(item.getID())
                elif destination == 'room_and_inventory':
                    if not item.getID() in self.inventory_items:
                        self.inventory_items.append(item.getID())
                elif destination == 'destroyed':
                    self.current_room.removeParamFromCurrentDescription(item.getID())
                if sound_id:
                    self.game_sound_system.play(sound_id)
                item.setDestination(destination)
            else:
                print(self.text_i_cant_catch_it)


    def goToRoomID(self, room_id):
        if not room_id == 'none':
            room = self.getRoom(room_id)
            if not room:
                print(self.text_i_got_confused_about_direction)
                self.quitGame(1)
            else:
                self.current_room = room
                self.current_room_id = room_id
                if self.current_room.hasEnterSoundID():
                    self.game_sound_system.play(self.current_room.enterSoundID(), 30)
                else:
                    self.game_sound_system.stop()
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
        elem = self.current_room.to_north
        if type(elem) is str:
            self.goToRoomID(self.current_room.getToNorth())
        else:
            item_id = elem['if_item_id']
            state = elem['if_state']
            failed_because = elem['failed_because']
            item = self.getItemByID(item_id)
            if not item:
                print(self.text_i_got_confused_about_direction)
            else:
                if item.getState() == state:
                    self.goToRoomID(self.current_room.getToNorth())
                else:
                    print(self.text_direction_not_available + ' ' + failed_because)


    def goToSouth(self):
        elem = self.current_room.to_south
        if type(elem) is str:
            self.goToRoomID(self.current_room.getToSouth())
        else:
            item_id = elem['if_item_id']
            state = elem['if_state']
            failed_because = elem['failed_because']
            item = self.getItemByID(item_id)
            if not item:
                print(self.text_i_got_confused_about_direction)
            else:
                if item.getState() == state:
                    self.goToRoomID(self.current_room.getToSouth())
                else:
                    print(self.text_direction_not_available + ' ' + failed_because)


    def goToWest(self):
        elem = self.current_room.to_west
        if type(elem) is str:
            self.goToRoomID(self.current_room.getToWest())
        else:
            item_id = elem['if_item_id']
            state = elem['if_state']
            failed_because = elem['failed_because']
            item = self.getItemByID(item_id)
            if not item:
                print(self.text_i_got_confused_about_direction)
            else:
                if item.getState() == state:
                    self.goToRoomID(self.current_room.getToWest())
                else:
                    print(self.text_direction_not_available + ' ' + failed_because)


    def goToEast(self):
        elem = self.current_room.to_east
        if type(elem) is str:
            self.goToRoomID(self.current_room.getToEast())
        else:
            item_id = elem['if_item_id']
            state = elem['if_state']
            failed_because = elem['failed_because']
            item = self.getItemByID(item_id)
            if not item:
                print(self.text_i_got_confused_about_direction)
            else:
                if item.getState() == state:
                    self.goToRoomID(self.current_room.getToEast())
                else:
                    print(self.text_direction_not_available + ' ' + failed_because)


    def pullItem(self, item_name):
        item = self.getItemByNameFromRoom(item_name)
        if not item:
            if type(item_name) is str:
                text = self.makeBold(item_name)
                print(f"{self.text_item_not_found} {text}.")
            else:
                text = self.makeBold(' '.join(item_name))
                print(f"{self.text_item_not_found} {text}.")
        else:
            self.death, destination, pulled_output, new_room_description_status = item.getPullAct()
            if not pulled_output:
                pulled_output = self.text_nothing_happened + ' ' + self.text_i_cant_move_it
                print(pulled_output)
            else:
                self.printTextWithWaitingTimeInSquare(pulled_output)
            if new_room_description_status:
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
        if not item:
            if type(item_name) is str:
                text = self.makeBold(item_name)
                print(f"{self.text_item_not_found} {text}.")
            else:
                text = self.makeBold(' '.join(item_name))
                print(f"{self.text_item_not_found} {text}.")
        else:
            self.death, destination, pushed_output, new_room_description_status = item.getPushAct()
            if not pushed_output:
                pushed_output = self.text_nothing_happened + ' ' + self.text_i_cant_move_it
                print(pushed_output)
            else:
                self.printTextWithWaitingTimeInSquare(pushed_output)
            if new_room_description_status:
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
        if not item:
            if type(item_name) is str:
                text = self.makeBold(item_name)
                print(f"{self.text_item_not_found} {text}.")
            else:
                text = self.makeBold(' '.join(item_name))
                print(f"{self.text_item_not_found} {text}.")
        else:
            canOpenItem = False
            if item.neededConditionToOpen():
                if item.needCombination():
                    attempts = int(item.getAttempts())
                    i = 0
                    find_it = False
                    print(self.text_type_a_combination_to_open)
                    while i < attempts and not find_it:
                        if self.replaying:
                            combination = self.replay_file.readline().replace('\n', '').strip()
                            print(self.text_your_combination
                                + ' n.' + str(i + 1) + '/' + str(attempts) + ': '
                                + combination + '\n')
                            sleep(1)
                        else:
                            combination = ''
                            try:
                                while not combination:
                                    combination = input(self.text_your_combination
                                        + ' n.' + str(i + 1) + '/' + str(attempts) + ': ')
                                self.replay_file.write(combination + '\n')
                                self.replay_file.flush()
                            except KeyboardInterrupt:
                                self.quitGame()

                        if self.replay_file:
                            find_it = self.getValue(item.getOriginalValueForCombination()) == combination
                        else:
                            find_it = item.checkCombination(combination)
                        if not find_it:
                            print(self.text_wrong_combination)
                        i += 1
                    canOpenItem = find_it
                    if not canOpenItem:
                        print(self.text_you_cant_open_it)
                elif item.neededItem():
                    item2 = self.getItemByID(item.getNeededItemID())
                    if item2.getDestination() == 'inventory' and item2.usedItemWith(item.getID()):
                        canOpenItem = True
                    else:
                        print(self.text_you_need_item_xyz + ' ' + item2.getName() + '.')
            else:
                canOpenItem = True

            if canOpenItem:
                self.death, destination, opened_output, new_room_description_status, sound_id = item.getOpenAct()
                if not opened_output:
                    opened_output = self.text_nothing_happened
                    print(opened_output)
                else:
                    self.game_sound_system.play(sound_id)
                    self.printTextWithWaitingTimeInSquare(opened_output)
                if new_room_description_status:
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
        if not item:
            if type(item_name) is str:
                text = self.makeBold(item_name)
                print(f"{self.text_item_not_found} {text}.")
            else:
                text = self.makeBold(' '.join(item_name))
                print(f"{self.text_item_not_found} {text}.")
        else:
            if item.getDestination() == 'room':
                if len(item.getItemRelatedCloseActList()) > 0:
                    if item.isRemoveItemFromRoomDefined():
                        if self.current_room.getID() == item.getRoomIDFromWhichToRemoveRelatedItem(self.items):
                            self.current_room.removeItemID(item.getIfIitemIDforCloseAct(self.items))

            self.death, destination, closed_output, new_room_description_status = item.getCloseAct()
            if not closed_output:
                closed_output = self.text_nothing_happened
                print(closed_output)
            else:
                self.printTextWithWaitingTimeInSquare(closed_output)
            if new_room_description_status:
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


    def showingRoom(self):
        self.clearScreen()
        self.printHeader()
        self.describeRoom()


    def getAction(self, action=''):
        if not action:
            try:
                while not action:
                    action = input('> ')
                print()
            except KeyboardInterrupt:
                self.quitGame()

        if self.replaying:
            print('> ' + action + '\n')

        verb = ''
        item = ''
        self.action = action
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
                    confused = False
                    for i in token[1:]:
                        if i in self.action_use_verb_with:
                            confused = True
                            break
                    if confused:
                        item = []
                    else:
                        item = token[1:]
                    item_to_use_with = []
        return verb, item, token, item_to_use_with


    def replay(self):
        if not self.game_running:
            self.replaying = True
            print(self.text_replaying_game)

            try:
                self.replay_file = open(self.replay_filename, 'r')
                line = ''
                while line.find('***assigned_values') == -1 and line.find('***list_of_actions') == -1:
                    # Get next line from file
                    line = self.replay_file.readline().strip()

                if not line.find('***list_of_actions') == -1:
                    line = self.replay_file.readline()
                    assigned_data = line.replace('\n', '').split(':')
                    if len(assigned_data) == 2:
                        self.assigned_values[assigned_data[0]] = assigned_data[1]

                while line.find('***list_of_actions') == -1:
                    line = self.replay_file.readline().strip()
                    assigned_data = line.replace('\n', '').split(':')
                    if len(assigned_data) == 2:
                        self.assigned_values[assigned_data[0]] = assigned_data[1]

                # assign the old assigned text into the items
                items_with_assigned_text = [i for i in self.items if i.hasAnAssignedText()]
                for iwat in items_with_assigned_text:
                    try:
                        for k in iwat.getAssignedKeys():
                            evaluated_value = self.getValue(iwat.getAssignedOriginalText(k))
                            iwat.assignTextToKey(evaluated_value, k)
                    except KeyError:
                        # 'assigned_text' is not always defined
                        pass

            except FileNotFoundError:
                print(self.text_cant_read_replay_file)
                self.quitGame(1)

            for line in self.replay_file:
                line = line.strip()
                self.showingRoom()
                verb, item, token, item_to_use_with = self.getAction(line)
                self.executeAction(verb, item, token, item_to_use_with)
                self.countdown()
            self.replay_file.close()
            self.replaying = False
            self.just_replayed = True
        else:
            print(self.text_cant_replay_during_game)


    def executeAction(self, verb, item, token, item_to_use_with):
        if verb == 'replay':
            self.replay()
        else:
            if not verb in self.action_help:
                if not self.replaying:
                    try:
                        if self.just_replayed:
                            self.replay_file = open(self.replay_filename, 'a')
                            self.just_replayed = False
                        else:
                            if not self.game_running:
                                self.replay_file = open(self.replay_filename, 'w+')
                                self.replay_file.write('***assigned_values\n')
                                for k in self.assigned_values.keys():
                                    self.replay_file.write(f"{k}:{self.assigned_values[k]}\n")
                                self.replay_file.write('\n***list_of_actions\n')
                    except FileNotFoundError:
                        print(self.text_cant_create_replay_file)
                        self.quitGame(1)

            if not self.action in self.action_quit and not self.replaying:
                self.replay_file.write(self.action + '\n')
                self.replay_file.flush()

            if verb in self.action_help:
                self.printHelp()

            elif verb in self.action_describe:
                self.game_running = True
                if not item:
                    print(self.text_what_to_describe)
                else:
                    if token[1] in self.action_inventory:
                        self.describeInventoryItem(item)
                    else:
                        self.describeRoomItem(item)

            elif verb in self.action_use_verb:
                self.game_running = True
                self.useItem(item, item_to_use_with)

            elif verb in self.action_catch:
                self.game_running = True
                self.catchItem(item)

            elif verb in self.action_open:
                self.game_running = True
                self.openItem(item)

            elif verb in self.action_close:
                self.game_running = True
                self.closeItem(item)

            elif verb in self.action_inventory:
                self.game_running = True
                self.printInventory()

            elif verb in self.directions_north:
                self.game_running = True
                self.goToNorth()

            elif verb in self.directions_south:
                self.game_running = True
                self.goToSouth()

            elif verb in self.directions_west:
                self.game_running = True
                self.goToWest()

            elif verb in self.directions_east:
                self.game_running = True
                self.goToEast()

            elif verb in self.action_pull:
                self.game_running = True
                self.pullItem(item)

            elif verb in self.action_push:
                self.game_running = True
                self.pushItem(item)

            elif verb in self.action_quit:
                self.quitGame(1)

            else:
                print(self.text_dont_understand)
                self.printHelp()


    def getActionAndRunIt(self):
        if not self.you_won:
            self.showingRoom()
            verb, item, token, item_to_use_with = self.getAction()
            self.executeAction(verb, item, token, item_to_use_with)
            self.countdown()


    def play(self):
        while not self.you_won and not self.death:
            self.getActionAndRunIt()
            if self.death:
                print(self.text_you_are_dead)
        self.replay_file.close()
