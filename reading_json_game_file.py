#!/usr/bin/env python3

import json
import os

class ReadingJSONGameFile:
    def __init__(self):
        self.json_filename = ''
        self.filename_games = []
        self.chooseJSONFile()
        self.loadJSONFile()
        self.game_data = self.getGameData()


    def chooseJSONFile(self):
        for fn in os.listdir('games'):
            if fn.endswith(".json"):
                self.filename_games.append(os.path.join('games', fn))
        if len(self.filename_games) > 1:
            i = 0
            for fn in self.filename_games:
                print(f"{i + 1}. {self.filename_games[i]}")
                i += 1
            try:
                game_index = int(input("Which adventure game do you want to play? "))
                self.json_filename = self.filename_games[game_index - 1]
            except KeyboardInterrupt:
                print()
                exit(1)
        else:
            self.json_filename = self.filename_games[0]


    def validateJSON(self, json_string_data):
        returnValue = True

        try:
            json.loads(json_string_data)
        except ValueError as err:
            print(err)
            returnValue = False

        return returnValue


    def loadJSONFile(self):
        contents = ""
        try:
            f = open(self.json_filename)
        except FileNotFoundError:
            print(f"file {json_filename} not found!")
            exit(1)

        contents += f.read()
        if not self.validateJSON(contents):
            print("JSON data is not valid!")
            exit(1)

        f.seek(0)
        try:
            self.game_data = json.load(f)
        except json.decoder.JSONDecodeError:
            print("JSON file has some kind of issue!")
            exit(1)

        f.close()


    def getGameData(self):
        return self.game_data
