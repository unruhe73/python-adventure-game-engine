#!/usr/bin/env python3

class Item:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.detailed_name = ''
        self.name_for_inventory = ''
        self.state = ''
        self.destination = 'room'
        self.assigned_text = {}
        self.description_act = []

        # they're items you can add to the room after a description
        # needed to discover items inside other items
        self.description_related_items = []

        # they're items you can aggregate to another item after "use X with Y"
        # needed to move a key into a door, for example, when that key is not needed anymore
        self.aggregated_items = []

        self.closeact_related_items = []
        self.catch_act = []
        self.can_catch_if = {}
        self.when_included_in_the_room = ''
        self.pull_act = []
        self.push_act = []
        self.close_act = []
        self.open_act = []
        self.use_alone_act = []
        self.use_with_act = []

        self.added_item_to_room = False
        self.removed_item_from_room = False

        self.to_open_condition = []
        self.used_with_item = []


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
        if not self.name_for_inventory:
            text = self.name
        return text


    def setNameForInventory(self, name):
        self.name_for_inventory = name


    def getState(self):
        return self.state


    def setState(self, state):
        self.state = state


    def getDestination(self):
        return self.destination


    def setDestination(self, destination):
        self.destination = destination


    def getAssignedText(self, assigned_key):
        ret = ''
        if assigned_key in self.assigned_text.keys():
            ret = self.assigned_text[assigned_key]
        return ret


    def assignTextToKey(self, text, key):
        self.assigned_text[key] = text


    def replaceAssignedText(self, text):
        ret = text
        if len(self.assigned_text) > 0 and text:
            for k in self.assigned_text.keys():
                key = '%' + k
                if not text.find(key) == -1:
                    text = text.replace(key, self.assigned_text[k])
            ret = text
        return ret


    def getDescription(self):
        descr = ''
        if self.destination == 'destroyed':
            return descr
        else:
            find_it = False
            i = 0
            while i < len(self.description_act) and not find_it:
                item = self.description_act[i]
                if item['state'] == '*' or not item['state'] or self.state in item['state']:
                    find_it = True
                    # the describe act can change the item status if a 'new_state' available
                    if item['new_state']:
                        self.state = item['new_state']
                else:
                    i += 1
            if find_it:
                descr = item['description']
            descr = self.replaceAssignedText(descr)
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
        if not new_state:
            self.description_act.append({'state': state, 'description': text, 'new_state': ''})
        else:
            if not state:
                self.description_act.append({'state': self.state, 'description': text, 'new_state': new_state})
            else:
                self.description_act.append({'state': state, 'description': text, 'new_state': new_state})


    def addItemRelatedDescription(self, state, if_item_id, has_destination, than_append_description, add_item_to_room_id=''):
        if not if_item_id or not has_destination or not than_append_description:
            return
        if if_item_id == self.id:
            # you cannot add a related description using your own item ID
            return
        related_item = {
          "state": state,
          "if_item_id": if_item_id,
          "has_destination": has_destination,
          "than_append_description": than_append_description,
          "add_item_to_room_id": add_item_to_room_id,
          "remove_item_from_room_id": ''
        }
        self.description_related_items.append(related_item)
        if add_item_to_room_id:
            self.added_item_to_room = True


    def addItemRelatedCloseAct(self, state, if_item_id, has_destination, add_item_to_room_id='', remove_item_from_room_id=''):
        if not if_item_id or not has_destination:
            return
        if if_item_id == self.id:
            # you cannot add a related description using your own item ID
            return
        related_item = {
          "state": state,
          "if_item_id": if_item_id,
          "has_destination": has_destination,
          "than_append_description": '',
          "add_item_to_room_id": add_item_to_room_id,
          "remove_item_from_room_id": remove_item_from_room_id
        }
        self.closeact_related_items.append(related_item)
        if remove_item_from_room_id:
            self.removed_item_from_room = True


    def getIfIitemIDforDescription(self, items):
        if_item_id = ''
        if self.added_item_to_room:
            items_id = [ i['if_item_id'] for i in self.description_related_items if i['state'] == self.state ]
            for i in items:
                if i.id in items_id:
                    for j in self.description_related_items:
                        if j['if_item_id'] == i.id and j['state'] == self.state and i.destination == 'room':
                            if_item_id = j['if_item_id']
        return if_item_id


    def getIfIitemIDforCloseAct(self, items):
        if_item_id = ''
        if self.removed_item_from_room:
            items_id = [ i['if_item_id'] for i in self.closeact_related_items if i['state'] == self.state ]
            for i in items:
                if i.id in items_id:
                    for j in self.closeact_related_items:
                        if j['if_item_id'] == i.id and j['state'] == self.state and i.destination == 'room':
                            if_item_id = j['if_item_id']
        return if_item_id


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
        if len(self.aggregated_items) > 0:
            other_items_description = ' There is also'
            aggregated_items = [i for i in items if i.id in self.aggregated_items]
            for i in aggregated_items:
                other_items_description += ' ' + i.detailed_name + ' in it'
                other_items_description += '. ' + i.getDescription()
            descr += other_items_description
        return descr


    def getItemRelatedDescriptionList(self):
        return self.description_related_items


    def getItemRelatedCloseActList(self):
        return self.closeact_related_items


    def getRoomIDInWhichToAddRelatedItem(self, items):
        room_id_in_which_to_add_related_item = ''
        if self.added_item_to_room:
            if len(self.description_related_items) > 0:
                items_id = [ i['if_item_id'] for i in self.description_related_items if i['state'] == self.state ]
                for i in items:
                    if i.id in items_id:
                        for j in self.description_related_items:
                            if j['if_item_id'] == i.id and j['state'] == self.state and i.destination == 'room':
                                room_id_in_which_to_add_related_item = j['add_item_to_room_id']
        return room_id_in_which_to_add_related_item


    def getRoomIDFromWhichToRemoveRelatedItem(self, items):
        room_id_from_which_to_remove_related_item = ''
        if self.removed_item_from_room:
            if len(self.closeact_related_items) > 0:
                items_id = [ i['if_item_id'] for i in self.closeact_related_items if i['state'] == self.state ]
                for i in items:
                    if i.id in items_id:
                        for j in self.closeact_related_items:
                            if j['if_item_id'] == i.id and j['state'] == self.state and i.destination == 'room':
                                room_id_from_which_to_remove_related_item = j['remove_item_from_room_id']
        return room_id_from_which_to_remove_related_item


    def isAddItemToRoomDefined(self):
        return self.added_item_to_room == True


    def isRemoveItemFromRoomDefined(self):
        return self.removed_item_from_room == True


    def isAggregateItemDefined(self):
        return self.aggregated_item == True


    def getCatchAct(self):
        find_it = False
        catched_text = ''
        destination = 'room'
        new_room_description_status = ''
        death = False
        i = 0
        while i < len(self.catch_act) and not find_it:
            item = self.catch_act[i]
            if item['state'] == '*' or not item['state'] or self.state in item['state']:
                destination = item['destination']
                catched_text = item['text']
                new_room_description_status = item['new_room_description_status']
                death = item['death']
                # the catch act can change the item status if a 'new_state' available
                if self.catch_act[i]['new_state']:
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


    def canCatch(self):
        return len(self.catch_act) > 0


    def getCanCatchIf(self):
        return self.can_catch_if


    def setCanCatchIf(self, assigned_state, if_item_id, in_state, else_cannot_catch_reason_state):
        self.can_catch_if = { 'if_item_id': if_item_id, 'assigned_state': assigned_state, 'in_state': in_state, 'else_cannot_catch_reason_state': else_cannot_catch_reason_state}


    def getOpenAct(self):
        find_it = False
        opened_text = ''
        destination = 'room'
        new_room_description_status = ''
        death = False
        i = 0
        while i < len(self.open_act) and not find_it:
            item = self.open_act[i]
            if item['state'] == '*' or not item['state'] or self.state in item['state']:
                destination = item['destination']
                opened_text = item['text']
                new_room_description_status = item['new_room_description_status']
                death = item['death']
                # the catch act can change the item status if a 'new_state' available
                if self.open_act[i]['new_state']:
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
        #  - room_and_inventory: it's a special item: you can put only a part of it into the inventory
        self.open_act.append({'state': state, 'text': text, 'destination': destination, 'new_room_description_status': new_room_description_status, 'new_state': new_state, 'death': death})


    # if you need a condition to open:
    #  you need a combination:
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
    def assignToOpenCondition(self, state, method_type, value, attempts, used_with_item):
        elem = {
            'state': state,
            'method': method_type,
            'value': value,
            'attempts': attempts,
            'used_with_item': used_with_item
        }
        my_elem = [i for i in self.to_open_condition if self.state == i['state']]
        if len(my_elem) == 0:
            self.to_open_condition.append(elem)
        else:
            print('open_act / to_open / state duplicated!')
            exit(1)


    def neededConditionToOpen(self):
        ret = False
        my_elem = [i for i in self.to_open_condition if self.state == i['state']]
        if len(my_elem) == 1:
            ret = True
        return ret


    def needCombination(self):
        ret = False
        my_elem = [i['method'] for i in self.to_open_condition if self.state == i['state']]
        if len(my_elem) == 1:
            if my_elem[0] == 'combination':
                ret = True
        return ret


    def getAttempts(self):
        ret = 3
        my_elem = [i['attempts'] for i in self.to_open_condition if self.state == i['state']]
        if len(my_elem) == 1:
            ret = my_elem[0]
        return ret


    def getCombination(self):
        ret = ''
        my_elem = [i['value'] for i in self.to_open_condition if self.state == i['state']]
        if len(my_elem) == 1:
            ret = my_elem[0]
        return ret


    def neededItem(self):
        ret = False
        my_elem = [i['method'] for i in self.to_open_condition if self.state == i['state']]
        if len(my_elem) == 1:
            if my_elem[0] == 'item_in_inventory':
                ret = True
        return ret


    def getNeededItemID(self):
        ret = ''
        my_elem = [i['used_with_item'] for i in self.to_open_condition if self.state == i['state']]
        if len(my_elem) == 1:
            ret = my_elem[0]
        return ret


    def usedItemWith(self, item_id):
        return item_id in self.used_with_item


    def checkCombination(self, text):
        ret = False
        method = ''
        elem = [i for i in self.to_open_condition if self.state == i['state']]
        if len(elem) == 1:
            method = elem[0]['method']
            if method == 'combination':
                if text == elem[0]['value']:
                    ret = True
        else:
            ret = True
        return ret


    def getCloseAct(self):
        find_it = False
        closed_text = ''
        destination = 'room'
        new_room_description_status = ''
        death = False
        i = 0
        while i < len(self.close_act) and not find_it:
            item = self.close_act[i]
            if item['state'] == '*' or not item['state'] or self.state in item['state']:
                destination = item['destination']
                closed_text = item['text']
                new_room_description_status = item['new_room_description_status']
                death = item['death']
                # the catch act can change the item status if a 'new_state' available
                if self.close_act[i]['new_state']:
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
        #  - room_and_inventory: it's a special item: you can put only a part of it into the inventory
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
            if item['state'] == '*' or not item['state'] or self.state in item['state']:
                destination = item['destination']
                pulled_text = item['text']
                new_room_description_status = item['new_room_description_status']
                death = item['death']
                # the catch act can change the item status if a 'new_state' available
                if self.pull_act[i]['new_state']:
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
            if item['state'] == '*' or not item['state'] or self.state in item['state']:
                destination = item['destination']
                pushed_text = item['text']
                new_room_description_status = item['new_room_description_status']
                death = item['death']
                # the catch act can change the item status if a 'new_state' available
                if self.push_act[i]['new_state']:
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
            if item['state'] == '*' or not item['state'] or self.state in item['state']:
                used_alone_text = item['text']
                new_room_description_status = item['new_room_description_status']
                death = item['death']
                # the use act can change the item status if a 'new_state' available
                if self.use_alone_act[i]['new_state']:
                    self.state = self.use_alone_act[i]['new_state']
                find_it = True
            else:
                i += 1
        return death, used_alone_text, new_room_description_status


    def addUseAloneAct(self, text, state='', new_room_description_status='', new_state='', death=False):
        self.use_alone_act.append({'state': state, 'text': text, 'new_room_description_status': new_room_description_status, 'new_state': new_state, 'death': death})


    def getUseWithAct(self, item_id):
        find_it = False
        used_with_text = ''
        new_room_description_status = ''
        death = False
        to_aggregate = False
        i = 0
        while i < len(self.use_with_act) and not find_it:
            item = self.use_with_act[i]
            if item_id == item['item']:
                if item['state'] == '*' or not item['state'] or self.state in item['state']:
                    used_with_text = item['text']
                    new_room_description_status = item['new_room_description_status']
                    death = item['death']
                    # the use act can change the item status if a 'new_state' available
                    if self.use_with_act[i]['new_state']:
                        self.state = self.use_with_act[i]['new_state']
                    find_it = True
                    if not item_id in self.used_with_item:
                        if not self.use_with_act[i]['status'] == 'failed':
                            self.used_with_item.append(item_id)
                            if item['after_use'] == 'aggregate':
                                to_aggregate = True
                else:
                    i += 1
            else:
                i += 1
        return death, used_with_text, new_room_description_status, to_aggregate


    def addUseWithAct(self, text, item, state='', new_room_description_status='', new_state='', death=False, status='', after_use=''):
        self.use_with_act.append({'state': state, 'text': text, 'item': item, 'new_room_description_status': new_room_description_status, 'new_state': new_state, 'death': death, 'status': status, 'after_use': after_use})


    def isAggregatedItemsAvailable(self):
        return len(self.aggregated_items) > 0


    def addToAggrateList(self, item_id):
        if not item_id in self.aggregated_items:
            self.aggregated_items.append(item_id)
