#!/usr/bin/env python3

class Item:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.detailed_name = ''
        self.name_for_inventory = ''
        self.state = ''
        self.destination = 'room'
        self.description_act = []
        self.catch_act = []
        self.when_included_in_the_room = ''


    def getID(self):
        return self.id


    def setID(self, text):
        self.id = text


    def getName(self):
        return self.name


    def setName(self, name):
        self.name = name


    def getDetailedName(self):
        return self.detailed_name


    def getDetailedNameList(self):
        return self.detailed_name.split()


    def setDetailedName(self, detailed_name):
        self.detailed_name = detailed_name


    def getNameForInventory(self):
        text = self.name_for_inventory
        if self.name_for_inventory == '':
            text = self.name
        return text


    def setNameForInventory(self, name):
        self.name_for_inventory = name


    def setState(self, state):
        self.state = state


    def getState(self):
        return self.state


    def getDestination(self):
        return self.destination


    def setDestination(self, destination):
        self.destination = destination


    def getDescription(self):
        descr = ''
        if self.destination == 'destroyed':
            return descr
        else:
            find_it = False
            i = 0
            while i < len(self.description_act) and not find_it:
                if self.state in self.description_act[i]['state']:
                    find_it = True
                    # the describe act can change the item status if a 'new_state' available
                    if not self.description_act[i]['new_state'] == '':
                        self.state = self.description_act[i]['new_state']
                else:
                    i += 1
            if find_it:
                descr = self.description_act[i]['description']
            return descr


    def setDescription(self, text, state='', new_state=''):
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


    def getCatchAct(self):
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


    def setCatchAct(self, text, destination='', state='', new_room_description_status=''):
        # destination can be:
        #  - room: the item stay in the room
        #  - destroyed: the item destroy itself: no more accessible to any action
        #  - inventory: the item go into the inventory, it's not in the room anymore
        self.catch_act.append({'state': state, 'text': text, 'destination': destination, 'new_room_description_status': new_room_description_status})


    def getWhenIncludedInTheRoom(self):
        return self.when_included_in_the_room


    def setWhenIncludedInTheRoom(self, when_included_in_the_room):
        self.when_included_in_the_room = when_included_in_the_room
