import pygame
import turtle
import numpy as np
import time
pygame.mixer.init(frequency=44100, size=-16, channels=2)

def make_crunchy_blip(frequency=800, duration_ms=50, volume=0.5):
    sample_rate = 44100
    duration = duration_ms / 1000
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    # Base sine + harmonics
    wave = np.sin(2 * np.pi * frequency * t)
    wave += 0.5 * np.sin(2 * np.pi * 2 * frequency * t)
    wave += 0.25 * np.sin(2 * np.pi * 3 * frequency * t)
    wave += 0.125 * np.sin(2 * np.pi * 4 * frequency * t)  # extra harmonic
    
    # Soft distortion for crunch
    wave = np.tanh(3 * wave)  # increase multiplier for more crunch
    
    # Quick exponential decay
    wave *= np.exp(-40 * t)
    
    # Convert to 16-bit stereo
    wave = np.clip(wave, -1, 1)
    wave_int16 = np.int16(wave * 32767 * volume)
    wave_stereo = np.column_stack((wave_int16, wave_int16))
    return pygame.sndarray.make_sound(wave_stereo)

class scoreBoard:
    def __init__(self):
        self.scoreboard = turtle.Turtle()
        self.scoreboard.ht()
        self.scoreboard.penup()
        self.scoreboard.setpos(0,250)

    def updateScoreboard(self,score1=0,score2=0):
        self.scoreboard.clear()
        self.scoreboard.write(f"{score1}            {score2}", False, "center", ("Bit5x3", 50, "bold"))

def drawCenterline():
    centerLine = turtle.Turtle()
    centerLine.seth(90)
    centerLine.penup()
    centerLine.setpos(0,337.5)
    centerLine.pensize(3)
    centerLine.speed(0)
    for i in range(0,34):
        centerLine.seth(270)
        centerLine.pendown()
        centerLine.forward(5)
        centerLine.penup()
        centerLine.forward(15)
    centerLine.ht()