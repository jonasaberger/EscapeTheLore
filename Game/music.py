import pygame

class Music:
    def __init__(self,music_path,volume):
        self.music_path = music_path
        self.volume = volume
        self.is_playing = False
        self.is_paused = False

        pygame.mixer.music.load(self.music_path)
        pygame.mixer.music.set_volume(self.volume)
        

    def loadMusic(self, music_path):
        self.music_path = music_path
        pygame.mixer.music.load(self.music_path)
        pygame.mixer.music.set_volume(self.volume)

        
    def toggleMusic(self):
        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
        else:
            pygame.mixer.music.play(-1)
            self.is_playing = True
            self.is_paused = False

    def stopMusic(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False