#!/usr/bin/env python3

import json
import os

class ReadingJSONGameFile:
    def __init__(self):
        self.json_filename = ''
        self.chooseJSONFile()
        self.loadJSONFile()
        self.game_data = self.getGameData()


    def getFileName(self):
        return self.json_filename[0:len(self.json_filename) - 5]


    def chooseJSONFile(self):
        games = []
        i = 1
        for fn in os.listdir('games'):
            if fn.endswith(".json"):
                self.json_filename = os.path.join('games', fn)
                self.loadJSONFile()
                try:
                    game_name = self.game_data['name'] + " v" + self.game_data['version']
                    elem = {'index': i, 'name': game_name, 'filename': self.json_filename}
                    games.append(elem)
                    del self.game_data
                    i += 1
                except KeyError:
                    # the JSON file is not an adventure game
                    pass
        if len(games) > 1:
            print('Available games:')
            for game in games:
                print(f"\t{game['index']}. {game['name']}")
            try:
                i = int(input("Which adventure game do you want to play? ")) - 1
                self.json_filename = games[i]['filename']
                del games
            except KeyboardInterrupt:
                print()
                exit(1)
        else:
            self.json_filename = games[0]['filename']


    def validateJSON(self, json_string_data):
        returnValue = True
        try:
            json.loads(json_string_data)
        except ValueError as err:
            print(err)
            returnValue = False
        return returnValue


    def loadJSONFile(self):
        try:
            f = open(self.json_filename)
        except FileNotFoundError:
            print(f"file {json_filename} not found!")
            exit(1)
        if not self.validateJSON(f.read()):
            print('JSON data is not valid for file ' + self.json_filename + '!')
            exit(1)
        f.seek(0)
        try:
            self.game_data = json.load(f)
        except json.decoder.JSONDecodeError:
            print('JSON file has some kind of issue!')
            exit(1)
        f.close()


    def getGameData(self):
        return self.game_data
