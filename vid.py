import sqlite3
import pygame
import tkinter as tk
from tkinter import messagebox
import sys
import time
import random

# Initialize pygame
pygame.init()

# SQLite Setup
conn = sqlite3.connect("car_game.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS HighScores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        score INTEGER
    )
""")
conn.commit()

# Function to save a high score
def save_high_score(score):
    cursor.execute("INSERT INTO HighScores (score) VALUES (?)", (score,))
    conn.commit()

# Function to get top 5 high scores
def get_high_scores():
    cursor.execute("SELECT score FROM HighScores ORDER BY score DESC LIMIT 5")
    return [row[0] for row in cursor.fetchall()]

# Define colors and screen dimensions
gray = (119, 118, 110)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 200, 0)
blue = (0, 0, 200)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
bright_blue = (0, 0, 255)
display_width = 800
display_height = 600

# Create the display surface
gamedisplays = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Car Game")

# Clock object for managing frame rate
clock = pygame.time.Clock()

# Load images
carimg = pygame.image.load('car1.jpg')
backgroundpic = pygame.image.load("download12.jpg")
yellow_strip = pygame.image.load("yellow strip.jpg")
strip = pygame.image.load("strip.jpg")
intro_background = pygame.image.load("background.jpg")
instruction_background = pygame.image.load("background2.jpg")

car_width = 56
pause = False

# Function to display the intro screen
def intro_loop():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()

        gamedisplays.blit(intro_background, (0, 0))
        largetext = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("CAR GAME", largetext)
        TextRect.center = (400, 100)
        gamedisplays.blit(TextSurf, TextRect)

        # Display high scores
        scores = get_high_scores()
        smalltext = pygame.font.Font('freesansbold.ttf', 20)
        y_offset = 200
        for idx, score in enumerate(scores, 1):
            score_text = f"{idx}. {score}"
            textsurf, textrect = text_objects(score_text, smalltext)
            textrect.center = (400, y_offset)
            gamedisplays.blit(textsurf, textrect)
            y_offset += 30

        button("START", 150, 520, 100, 50, green, bright_green, "play")
        button("QUIT", 550, 520, 100, 50, red, bright_red, "quit")
        button("INSTRUCTION", 300, 520, 200, 50, blue, bright_blue, "intro")
        pygame.display.update()
        clock.tick(50)

# Function to display the crash screen and save the score
def crash(score):
    save_high_score(score)
    message_display("YOU CRASHED")

# Other functions (button, introduction, countdown, game_loop, etc.) remain the same.
# Ensure to pass the `score` variable appropriately in the `crash` function call.
