        for i in self.game_data['items']
            try:
                if not type(i['open_act']) is str:
                    for j in i['open_act']:
                        try:
                            state = j['state']
                        except KeyError:
                            state = ''

                        value = ''
                        try:
                            to_open = j['to_open']
                            method = to_open['method']
                            if method == 'combination':
                                value = self.getValue(to_open['value'])
                                attempts = to_open['attempts']
                            elif method == 'item_in_inventory':
                                used_with_item = to_open['used_with_item']
                            item.assignToOpenCondition(state, method, value, attempts, used_with_item)
                        except KeyError:
                            # just in case of a 'safe' or 'doors' item or similar you can have an access condition
                            pass
                        item.addOpenAct(j['text'], destination, state, new_room_description_status, new_state, death)
            except KeyError:
                # open act not always defined
                pass


