#!/usr/bin/env python3

class Room:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.state = '0'
        self.description = {}
        self.items = []
        self.to_north = ''
        self.to_south = ''
        self.to_east = ''
        self.to_west = ''


    def getID(self):
        return self.id


    def setID(self, text):
        self.id = text


    def getName(self):
        return self.name


    def setName(self, text):
        self.name = text


    def getState(self):
        return self.state


    def setState(self, text):
        self.state = text


    def getDescription(self):
        return self.description[self.state]


    def addDescription(self, text, state='0'):
        self.description[state] = text


    def addItemID(self, item_id):
        self.items.append(item_id)


    def removeItemID(self, item_id):
        self.items.remove(item_id)


    def getItemsID(self):
        return self.items

    def getToNorth(self):
        return self.to_north


    def setToNorth(self, new_room_id):
        self.to_north = new_room_id


    def getToSouth(self):
        return self.to_south


    def setToSouth(self, new_room_id):
        self.to_south = new_room_id


    def getToEast(self):
        return self.to_east


    def setToEast(self, new_room_id):
        self.to_east = new_room_id


    def getToWest(self):
        return self.to_west


    def setToWest(self, new_room_id):
        self.to_west = new_room_id


    def removeParamFromCurrentDescription(self, item_id):
        remove_done = False
        text = self.description[self.state]
        if item_id in text:
            count_open = text.count('{')
            count_close = text.count('}')
            param_begin_index = 0
            i = 0
            still_to_be_replaced = True
            while i < count_open and still_to_be_replaced:
                param_begin_index = text.find('{', param_begin_index) + 1
                param_end_index = text.find('}', param_begin_index)
                param_to_remove = text[param_begin_index:param_end_index]
                if param_to_remove == item_id:
                    to_replace = '{' + param_to_remove + '}'
                    text = text.replace(to_replace, '')
                    still_to_be_replaced = False
                param_begin_index = param_end_index + 1
                i += 1
            self.description[self.state] = text.replace('  ', ' ').replace(' .', '.').replace(', .','.')
            self.items.remove(item_id)
            remove_done = True
        return remove_done
