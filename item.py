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
        self.description_related_items = []
        self.catch_act = []
        self.can_catch_if = {}
        self.when_included_in_the_room = ''
        self.pull_act = []
        self.push_act = []
        self.close_act = []
        self.open_act = []
        self.use_alone_act = []
        self.use_with_act = []


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
                item = self.description_act[i]
                if item['state'] == '*' or item['state'] == '' or self.state in item['state']:
                    find_it = True
                    # the describe act can change the item status if a 'new_state' available
                    if not item['new_state'] == '':
                        self.state = item['new_state']
                else:
                    i += 1
            if find_it:
                descr = item['description']
            return descr


    def getDescriptionInState(self, state):
        descr = ''
        if self.destination == 'destroyed':
            return descr
        else:
            find_it = False
            i = 0
            while i < len(self.description_act) and not find_it:
                item = self.description_act[i]
                if state == item['state']:
                    find_it = True
                else:
                    i += 1
            if find_it:
                descr = item['description']
            return descr


    def setDescription(self, text, state='', new_state=''):
        if new_state == '':
            self.description_act.append({'state': state, 'description': text, 'new_state': ''})
        else:
            if state == '':
                self.description_act.append({'state': self.state, 'description': text, 'new_state': new_state})
            else:
                self.description_act.append({'state': state, 'description': text, 'new_state': new_state})


    def addItemRelatedDescription(self, state, if_item_id, has_destination, than_append_description):
        if if_item_id == '' or has_destination == '' or than_append_description == '':
            return
        if if_item_id == self.id:
            # you cannot add a related description using your own item ID
            return
        related_item = {
          "state": state,
          "if_item_id": if_item_id,
          "has_destination": has_destination,
          "than_append_description": than_append_description
        }
        self.description_related_items.append(related_item)


    def fullDescription(self, items):
        descr = self.getDescription()
        if len(self.description_related_items) > 0:
            used_items_id = [ i['if_item_id'] for i in self.description_related_items if i['state'] == self.state ]
            for i in items:
                if i.id in used_items_id:
                    for j in self.description_related_items:
                        if j['if_item_id'] == i.id and j['state'] == self.state and i.destination == 'room':
                            than_append_description = j['than_append_description']
                            descr += ' ' + than_append_description.replace('{name}', i.name)
        return descr


    def getItemRelatedDescriptionList(self):
        return self.description_related_items


    def getCatchAct(self):
        find_it = False
        catched_text = ''
        destination = 'room'
        new_room_description_status = ''
        i = 0
        while i < len(self.catch_act) and not find_it:
            item = self.catch_act[i]
            if item['state'] == '*' or item['state'] == '' or self.state in item['state']:
                destination = item['destination']
                catched_text = item['text']
                new_room_description_status = item['new_room_description_status']
                death = item['death']
                # the catch act can change the item status if a 'new_state' available
                if not self.catch_act[i]['new_state'] == '':
                    self.state = self.catch_act[i]['new_state']
                find_it = True
            else:
                i += 1
        return death, destination, catched_text, new_room_description_status


    def addCatchAct(self, text, destination='room', state='', new_room_description_status='', new_state='', death=False):
        # destination can be:
        #  - room: the item stay in the room
        #  - destroyed: the item destroy itself: no more accessible to any action
        #  - inventory: the item go into the inventory, it's not in the room anymore
        #  - room_and_inventory: it's a special item: you can put only a part of it into the inventory
        self.catch_act.append({'state': state, 'text': text, 'destination': destination, 'new_room_description_status': new_room_description_status, 'new_state': new_state, 'death': death})


    def getCanCatchIf(self):
        return self.can_catch_if


    def setCanCatchIf(self, assigned_state, if_item_id, in_state, else_cannot_catch_reason_state):
        self.can_catch_if = { 'if_item_id': if_item_id, 'assigned_state': assigned_state, 'in_state': in_state, 'else_cannot_catch_reason_state': else_cannot_catch_reason_state}


    def getOpenAct(self):
        find_it = False
        opened_text = ''
        destination = 'room'
        new_room_description_status = ''
        i = 0
        while i < len(self.open_act) and not find_it:
            item = self.open_act[i]
            if item['state'] == '*' or item['state'] == '' or self.state in item['state']:
                destination = item['destination']
                opened_text = item['text']
                new_room_description_status = item['new_room_description_status']
                death = item['death']
                # the catch act can change the item status if a 'new_state' available
                if not self.open_act[i]['new_state'] == '':
                    self.state = self.open_act[i]['new_state']
                find_it = True
            else:
                i += 1
        return death, destination, opened_text, new_room_description_status


    def addOpenAct(self, text, destination='room', state='', new_room_description_status='', new_state='', death=False):
        # destination can be:
        #  - room: the item stay in the room
        #  - destroyed: the item destroy itself: no more accessible to any action
        #  - inventory: the item go into the inventory, it's not in the room anymore
        self.open_act.append({'state': state, 'text': text, 'destination': destination, 'new_room_description_status': new_room_description_status, 'new_state': new_state, 'death': death})


    def getCloseAct(self):
        find_it = False
        closed_text = ''
        destination = 'room'
        new_room_description_status = ''
        i = 0
        while i < len(self.close_act) and not find_it:
            item = self.close_act[i]
            if item['state'] == '*' or item['state'] == '' or self.state in item['state']:
                destination = item['destination']
                closed_text = item['text']
                new_room_description_status = item['new_room_description_status']
                death = item['death']
                # the catch act can change the item status if a 'new_state' available
                if not self.close_act[i]['new_state'] == '':
                    self.state = self.close_act[i]['new_state']
                find_it = True
            else:
                i += 1
        return death, destination, closed_text, new_room_description_status


    def addCloseAct(self, text, destination='room', state='', new_room_description_status='', new_state='', death=False):
        # destination can be:
        #  - room: the item stay in the room
        #  - destroyed: the item destroy itself: no more accessible to any action
        #  - inventory: the item go into the inventory, it's not in the room anymore
        self.close_act.append({'state': state, 'text': text, 'destination': destination, 'new_room_description_status': new_room_description_status, 'new_state': new_state, 'death': death})


    def getWhenIncludedInTheRoom(self):
        return self.when_included_in_the_room


    def setWhenIncludedInTheRoom(self, when_included_in_the_room):
        self.when_included_in_the_room = when_included_in_the_room


    def getPullAct(self):
        find_it = False
        death = False
        destination = 'room'
        pulled_text = ''
        new_room_description_status = ''
        i = 0
        while i < len(self.pull_act) and not find_it:
            item = self.pull_act[i]
            if item['state'] == '*' or item['state'] == '' or self.state in item['state']:
                destination = item['destination']
                pulled_text = item['text']
                new_room_description_status = item['new_room_description_status']
                death = item['death']
                # the catch act can change the item status if a 'new_state' available
                if not self.pull_act[i]['new_state'] == '':
                    self.state = self.pull_act[i]['new_state']
                find_it = True
            else:
                i += 1
        return death, destination, pulled_text, new_room_description_status


    def addPullAct(self, text, destination='room', state='', new_room_description_status='', new_state='', death=False):
        self.pull_act.append({'state': state, 'text': text, 'destination': destination, 'new_room_description_status': new_room_description_status, 'new_state': new_state, 'death': death})


    def getPushAct(self):
        find_it = False
        death = False
        destination = 'room'
        pushed_text = ''
        new_room_description_status = ''
        i = 0
        while i < len(self.push_act) and not find_it:
            item = self.push_act[i]
            if item['state'] == '*' or item['state'] == '' or self.state in item['state']:
                destination = item['destination']
                pushed_text = item['text']
                new_room_description_status = item['new_room_description_status']
                death = item['death']
                # the catch act can change the item status if a 'new_state' available
                if not self.push_act[i]['new_state'] == '':
                    self.state = self.push_act[i]['new_state']
                find_it = True
            else:
                i += 1
        return death, destination, pushed_text, new_room_description_status


    def addPushAct(self, text, destination='room', state='', new_room_description_status='', new_state='', death=False):
        self.push_act.append({'state': state, 'text': text, 'destination': destination, 'new_room_description_status': new_room_description_status, 'new_state': new_state, 'death': death})


    def getUseAloneAct(self):
        find_it = False
        used_alone_text = ''
        new_room_description_status = ''
        new_state = ''
        death = False
        i = 0
        while i < len(self.use_alone_act) and not find_it:
            item = self.use_alone_act[i]
            if item['state'] == '*' or item['state'] == '' or self.state in item['state']:
                used_alone_text = item['text']
                new_room_description_status = item['new_room_description_status']
                death = item['death']
                # the use act can change the item status if a 'new_state' available
                if not self.use_alone_act[i]['new_state'] == '':
                    self.state = self.use_alone_act[i]['new_state']
                find_it = True
            else:
                i += 1
        return death, used_alone_text, new_room_description_status


    def addUseAloneAct(self, state='', text, new_room_description_status='', new_state='', death=False):
        self.use_alone_act.append({'state': state, 'text': text, 'new_room_description_status': new_room_description_status, 'new_state': new_state, 'death': death})


    def getUseWithAct(self, item_id):
        find_it = False
        used_with_text = ''
        item_id = ''
        new_room_description_status = ''
        death = False
        i = 0
        while i < len(self.use_with_act) and not find_it:
            item = self.use_with_act[i]
            if item_id == item['item']:
                if item['state'] == '*' or item['state'] == '' or self.state in item['state']:
                    used_with_text = item['text']
                    new_room_description_status = item['new_room_description_status']
                    death = item['death']
                    # the use act can change the item status if a 'new_state' available
                    if not self.use_with_act[i]['new_state'] == '':
                        self.state = self.use_with_act[i]['new_state']
                    find_it = True
                else:
                    i += 1
            else:
                i += 1
        return death, used_with_text, new_room_description_status, new_state


    def addUseWithAct(self, state='', text, item, new_room_description_status='', new_state='', death=False):
        self.use_with_act.append({'state': state, 'text': text, 'item': item, 'new_room_description_status': new_room_description_status, 'new_state': new_state, 'death': death})
