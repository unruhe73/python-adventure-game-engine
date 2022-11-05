#!/usr/bin/env python3

class Item:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.detailed_name = ''
        self.name_for_inventory = ''
        self.state = ''
        self.destination = ''
        self.description_act = []
        self.catch_act = []
        self.when_included_in_the_room = ''


    def get_id(self):
        return self.id


    def set_id(self, text):
        self.id = text


    def get_name(self):
        return self.name


    def set_name(self, text):
        self.name = text


    def set_detailed_name(self, text):
        self.detailed_name = text


    def get_detailed_name(self):
        return self.detailed_name


    def get_name_for_inventory(self):
        text = self.name_for_inventory
        if self.name_for_inventory == '':
            text = self.name
        return text


    def set_name_for_inventory(self, text):
        self.name_for_inventory = text


    def set_state(self, text):
        self.state = text


    def get_state(self):
        return self.state


    def get_destination(self):
        return self.destination


    def set_destination(self, text):
        self.destination = text


    def get_description(self):
        descr = ''
        if self.destination == 'destroyed':
            return descr
        else:
            find_it = False
            i = 0
            while i < len(self.description_act) and not find_it:
                if self.state in self.description_act[i]['state']:
                    find_it = True
                    if not self.description_act[i]['new_state'] == '':
                        self.state = self.description_act[i]['new_state']
                else:
                    i += 1
            if find_it:
                descr = self.description_act[i]['description']
            return descr


    def set_description(self, text, state='', new_state=''):
        if new_state == '':
            if state == '':
                self.description_act.append({'state': self.state, 'description': text, 'new_state': ''})
            else:
                self.description_act.append({'state': state, 'description': text, 'new_state': ''})
        else:
            if state == '':
                self.description_act.append({'state': self.state, 'description': text, 'new_state': new_state})
            else:
                self.description_act.append({'state': state, 'description': text, 'new_state': new_state})


    def get_catch_act(self):
        find_it = False
        catched = ''
        destination = ''
        new_room_description_status = ''
        i = 0
        while i < len(self.catch_act) and not find_it:
            item = self.catch_act[i]
            if item['state'] == '*' or item['state'] == '' or self.state in item['state']:
                destination = item['destination']
                catched = item['text']
                new_room_description_status = item['new_room_description_status']
                find_it = True
            else:
                i += 1

        return destination, catched, new_room_description_status


    def set_catch_act(self, text, destination='', state='', new_room_description_status=''):
        # destination can be:
        #  - room: the item stay in the room
        #  - destroyed: the item destroy itself: no more accessible to any action
        #  - inventory: the item go into the inventory, it's not in the room anymore
        self.catch_act.append({'state': state, 'text': text, 'destination': destination, 'new_room_description_status': new_room_description_status})


    def get_when_included_in_the_room(self):
        return self.when_included_in_the_room


    def set_when_included_in_the_room(self, text):
        self.when_included_in_the_room = text
