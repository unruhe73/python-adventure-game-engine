#!/usr/bin/env python3
import json
import os

class ReadingJSONGameFile:
    def __init__(self):
        self.json_filename = os.path.join('games', 'datagame.json')
        self.loadJSONFile()
        self.game_data = self.getGameData()

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
            f = open (self.json_filename)
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
