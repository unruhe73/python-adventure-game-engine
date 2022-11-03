#!/usr/bin/env python3

class Room:
    def __init__(self, id, name):
        self.id = id
        self.items = []
        self.name = name
        self.to_north = ''
        self.to_south = ''
        self.to_east = ''
        self.to_west = ''


    def get_id(self):
        return self.id


    def set_id(self, text):
        self.id = text


    def get_name(self):
        return self.name


    def set_name(self, text):
        self.name = text


    def get_description(self):
        return self.description


    def set_description(self, text):
        self.description = text


    def get_init_state(self):
        return self.init_state


    def set_init_state(self, init_state):
        self.init_state = init_state


    def add_item_id(self, item_id):
        elem = {'item': item_id, 'visible': True}
        self.items.append(elem)


    def remove_item(self, item_id):
        find_it = False
        i = 0
        while i < len(self.items) and not find_it:
            if item_id == self.items[i]['item']:
               elem = {'item': item_id, 'visible': False}
               self.items[i] = elem
               find_it = True
            else:
                i += 1


    def get_to_north_room(self):
        return self.to_north


    def set_to_north_room(self, new_room_id):
        self.to_north = new_room_id


    def get_to_south_room(self):
        return self.to_south


    def set_to_south_room(self, new_room_id):
        self.to_south = new_room_id


    def get_to_east_room(self):
        return self.to_east


    def set_to_east_room(self, new_room_id):
        self.to_east = new_room_id


    def get_to_west_room(self):
        return self.to_west


    def set_to_west_room(self, new_room_id):
        self.to_west = new_room_id
