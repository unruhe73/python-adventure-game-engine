#!/usr/bin/env python3
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame


class GameSoundSystem:
    def __init__(self, sound_system_status):
        self.setStatus(sound_system_status)
        self.sound_filename = {}

        if self.sound_system:
            pygame.mixer.init()


    def setStatus(self, sound_system_status):
        if sound_system_status == 'On':
            self.sound_system = True
        elif sound_system_status == 'Off':
            self.sound_system = False
        else:
            self.sound_system = False


    def isEnabled(self):
        return self.sound_system


    def assignSoundDirectory(self, dirname):
        if self.sound_system:
            self.sound_directory = os.path.join('sounds', dirname)
            if not os.path.exists(self.sound_directory):
                self.sound_system = False


    def assignSoundFilename(self, sound_id, filename):
        if self.sound_system:
            filepath = os.path.join(self.sound_directory, filename)
            if os.path.exists(filepath):
                if sound_id:
                    self.sound_filename[sound_id] = filepath


    def play(self, sound_id, fade_out_seconds = ''):
        if self.sound_system:
            if sound_id:
                if self.sound_filename[id_sound]:
                    pygame.mixer.music.load(self.sound_filename[id_sound])
                    pygame.mixer.music.play()
                    if fade_out_seconds:
                        pygame.mixer.music.fadeout(fade_out_seconds * 1000)
