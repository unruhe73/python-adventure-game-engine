#!/usr/bin/env python3

class Room:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.items = []
        self.to_north = ''
        self.to_south = ''
        self.to_east = ''
        self.to_west = ''


    def get_item_by_id(self, item_id):
        find_it = False
        i = 0
        while i < 0 and not find_it:
            if self.items[i]['item'] == item_id:
                find_it = True
            else:
                i += 1

        if not find_it:
            ret = None
        else:
            ret = self.items[i]
        return ret


    def get_id(self):
        return self.id


    def get_name(self):
        return self.name


    def get_description(self):
        return self.description


    def set_description(self, description):
        self.description = description


    def set_init_state(self, init_state):
        self.init_state = init_state


    def add_item_id(self, item_id):
        self.items.append(item_id)


    def set_to_north_room(self, new_room_id):
        self.to_north = new_room_id


    def set_to_south_room(self, new_room_id):
        self.to_south = new_room_id


    def set_to_east_room(self, new_room_id):
        self.to_east = new_room_id


    def set_to_west_room(self, new_room_id):
        self.to_west = new_room_id
