#!/usr/bin/env python3

class Item:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.state = ''
        self.hidden = False
        self.description_act = []
        self.catch_act = []
        self.got_first_catch = False


    def set_init_state(self, init_state):
        self.state = init_state


    def set_description(self, description, state='', new_state=''):
        if new_state == '':
            if state == '':
                self.description_act.append({'state': self.state, 'description': description, 'new_state': ''})
            else:
                self.description_act.append({'state': state, 'description': description, 'new_state': ''})
        else:
            if state == '':
                self.description_act.append({'state': self.state, 'description': description, 'new_state': new_state})
            else:
                self.description_act.append({'state': state, 'description': description, 'new_state': new_state})


    def get_description(self):
        if self.hidden:
            return ''
        else:
            find_it = False
            i = 0
            while i < len(self.description_act) and not find_it:
                if self.description_act[i]['state'] == self.state:
                    find_it = True
                    if not self.description_act[i]['new_state'] == '':
                        self.state = self.description_act[i]['new_state']
                else:
                    i += 1

            if find_it:
                descr = self.description_act[i]['description']
            else:
                descr = ''

            return descr


    def get_name(self):
        return self.name


    def set_catch_act(self, text, state='', hidden_state='', new_room_description_status=''):
        self.catch_act.append({'state': state, 'text': text, 'hidden_state': hidden_state, 'new_room_description_status': new_room_description_status})


    def get_catch_act(self):
        find_it = False
        catch = ''
        new_room_description_status = ''
        i = 0
        while i < len(self.catch_act) and not find_it:
            if self.hidden:
                find_it = True
            else:
                item = self.catch_act[i]
                if item['state'] == '*' or item['state'] == self.state:
                    self.got_first_catch = True
                    if item['hidden_state'] == 'True':
                        self.hidden = True
                    catch = item['text']
                    new_room_description_status = item['new_room_description_status']
                else:
                    i += 1

        return catch, new_room_description_status
