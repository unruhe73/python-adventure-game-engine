#!/usr/bin/env python3
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

class GameSoundSystem:
    def __init__(self, sound_system_status):
        if sound_system_status == 'On':
            self.sound_system = True
        elif sound_system_status == 'Off':
            self.sound_system = False
        else:
            self.sound_system = False

        if self.sound_system:
            import pygame
            pygame.mixer.init()
            self.soud_directory = 'sounds'

    def isEnabled(self):
        return self.sound_system
