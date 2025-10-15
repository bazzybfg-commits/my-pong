import turtle
from turtle import speed, penup, shape, shapesize, xcor, ycor
import time
import random
import math
import pygame
import goof
from math import cos, sin


HITBOXPENSIZE = 4
step = 5 # how far the players should move each frame (pixels)
HEIGHT = 675 #default 675
WIDTH = 900 #default 900
PADDLE_HEIGHT = 100
DEBUG_MODE = False
multiplayer = False
FPS = 150

ladVsLad = False
if ladVsLad:
    multiplayer = False



if not multiplayer:
    difficulty = int(turtle.textinput("Difficulty","Please enter a difficulty from 0-5")) # higher difficulty = ai is better at detecting stuff, ball moves quicker. 0 is default
    while difficulty < 0 or difficulty > 5:
        difficulty = int(turtle.textinput("Invalid difficulty!","Please enter a difficulty from 0-5")) # higher difficulty = ai is better at detecting stuff, ball moves quicker. 0 is default
    if difficulty >= 3:
        ai_prediction = True
        ai_prediction_offset = 100*(difficulty)
    else:
        ai_prediction = False
else:
    difficulty = 5
ballSpeed = 5
max_ball_speed = 10 + difficulty 
AI_offset = int(30 * (0.5 ** difficulty))
ai_speed = 5+(difficulty/10)


collisionSound = goof.make_crunchy_blip(600)
turtle.delay(0)
# class for AI opponent logic
class aiLad:
    def __init__(self,player,speed=ai_speed): 
        self.frame_counter = 0
        self.player = player
        self.target = ball.ycor()
        self.player.speed = speed
    
    def update(self): # all the ai logic that includes flaws in its targeting and stuff
        # works out angles and stuff for predicting where the ball will be when it reaches the ai
        ballHeadingDeg = ball.heading()
        ballHeadingRad = math.radians(ballHeadingDeg)

        dx = ballSpeed * cos(ballHeadingRad)
        dy = ballSpeed * sin(ballHeadingRad)

        self.frame_counter += 1
        if self.frame_counter % 15 == 0: # only updates AI target every 5 frames so he has a low reaction time
            if ai_prediction and self.player.turtle.xcor() - ball.xcor() <= ai_prediction_offset:
    # Check if ball is moving toward AI
                if (self.player.side == "right" and dx > 0) or (self.player.side == "left" and dx < 0):
                    self.target = ball.ycor() + ((dy / abs(dx)) * (self.player.turtle.xcor() - ball.xcor()))
                    self.target = max(-height+25, min(height-25, self.target))
                else:
                    self.target = ball.ycor() + random.randint(-AI_offset, AI_offset)
                #print(f"tgt: {self.target}, loc: {self.player.turtle.ycor()}")
                
                # yP = yC + (dy ) * (xAI - xC)
                #           (/dx)  
                # where yP is the predicted, yC is the balls current, dy and dx are the amount the ball moves per frame
                # xAI is the paddle's x coord and xC is the balls x
            else:
                self.target = ball.ycor() + random.randint(-AI_offset,AI_offset)
        # movement logic
        if self.target > self.player.turtle.ycor(): 
            self.player.stopMovingDown()
            self.player.startMovingUp()
            #print("up")
        
        if self.target < self.player.turtle.ycor():
            self.player.stopMovingUp()
            self.player.startMovingDown()
            #print("down")
        
        if self.player.turtle.ycor() - 10 <= self.target <= self.player.turtle.ycor() + 10:
            self.player.stopMovingUp()
            self.player.stopMovingDown()
            #print("stop moving down")
        self.player.update(ai_speed)
# Class for paddle movement and other player logic
class Player:
    def __init__(self,turtleObj, side, speed=step): # defines all the necessary shenanigans about it, side tells it which side the player is on
        self.side = side
        
        self.speed = speed
        self.movingUp = False
        self.movingDown = False
        self.turtle = turtleObj
        self.ycor = turtleObj.ycor()
        self.turtle.speed(0)
        self.turtle.penup()
        self.turtle.shape("square")        # Set the shape to square 
        self.turtle.shapesize(stretch_wid=PADDLE_HEIGHT/20, stretch_len=0.5)  # 5 times taller, normal width
        self.score = 0
        if self.side == "right":
            self.maxX = self.turtle.xcor() - 5
        else:
            self.maxX = self.turtle.xcor() + 5
        self.maxY = self.turtle.ycor() + 50
        self.minY = self.turtle.ycor() - 50

    def startMovingUp(self):
        self.movingUp = True

    def stopMovingUp(self):
        self.movingUp = False

    def startMovingDown(self):
        self.movingDown = True

    def stopMovingDown(self):
        self.movingDown = False

    def sety(self,amount):
        self.turtle.sety(amount)
    
    def draw_hitbox(self, hitbox_turtle):
        hitbox_turtle.clear()
        hitbox_turtle.goto(self.turtle.xcor() - 5, self.turtle.ycor() + 50)
        hitbox_turtle.pendown()
        hitbox_turtle.goto(self.turtle.xcor() + 5, self.turtle.ycor() + 50)
        hitbox_turtle.goto(self.turtle.xcor() + 5, self.turtle.ycor() - 50)
        hitbox_turtle.goto(self.turtle.xcor() - 5, self.turtle.ycor() - 50)
        hitbox_turtle.goto(self.turtle.xcor() - 5, self.turtle.ycor() + 50)
        hitbox_turtle.penup()

    def update(self, speed=5): 
        if self.side == "right":
            self.maxX = self.turtle.xcor() - 5
        else:
            self.maxX = self.turtle.xcor() + 5
        self.maxY = self.turtle.ycor() + PADDLE_HEIGHT/2
        self.minY = self.turtle.ycor() - PADDLE_HEIGHT/2
        '''fix the PADDLE_HEIGHT thijng'''
        # makes 2 arrays with the coords of the top/bottom corner of the player
        if self.movingUp and height >= self.turtle.ycor()+(PADDLE_HEIGHT/2):  # makes sure that turtle isnt offscreen
            self.sety(self.turtle.ycor() + speed)
        if self.movingDown and -height <= self.turtle.ycor()-(PADDLE_HEIGHT/2): # again makes sure that the turtle that represents the playet isnt offscreen
            self.sety(self.turtle.ycor() - speed)
            #print(f"Player moving down from {self.turtle.ycor()}")
        
def checkCollisions():
    global ballSpeed
    # logic for bouncing off bottom
    collision = False
    if ball.ycor() <= -(height-17.5) or ball.ycor() >= height - 2.5 : # bottom then top
        ball.setheading(-ball.heading())
        collision = True
    # logic for bouncing off players ahead:

    if (player1.maxX -30<= ball.xcor() <= player1.maxX) and (player1.minY <= ball.ycor() <= player1.maxY):
        ball.seth(180-ball.heading())
        #print(ball.ycor())
        collision = True
    
    if (player2.maxX <= ball.xcor() <= player2.maxX + 30) and (player2.minY <= ball.ycor() <= player2.maxY):
        ball.seth(180-ball.heading())
        collision = True
    if collision:
        collisionSound.play() # plays a sound when theres a collision
        if ballSpeed <= max_ball_speed:
            ballSpeed += 0.15
# gonna try hitboxes for the player1 to try and debug

if DEBUG_MODE:
    hitbox1 = turtle.Turtle()
    hitbox1.pensize(HITBOXPENSIZE)
    hitbox1.hideturtle()
    hitbox1.penup()
    hitbox1.pencolor("red")
    hitbox1.speed(0)

    hitbox2 = turtle.Turtle()
    hitbox2.hideturtle()
    hitbox2.pensize(HITBOXPENSIZE)
    hitbox2.penup()
    hitbox2.pencolor("red")
    hitbox2.speed(0)
    


def update():
    # full loop that accounts for player movement and ball movement.
    global height, ballSpeed
    if player1.movingUp or player1.movingDown:
        player1.update()
    if not multiplayer:
        opponent.update()
        if ladVsLad:
            opponent2.update()
    else:
        if player2.movingUp or player2.movingDown:
            player2.update()
    
    
    ball.forward(ballSpeed)
    checkCollisions()

    
    if DEBUG_MODE:
        player1.draw_hitbox(hitbox1)
        player2.draw_hitbox(hitbox2)

    # logic for detecting if ball is out of bounds
    if ball.xcor() > width or ball.xcor() < -width:
        if ball.xcor() > width:
            player1.score = player1.score + 1
        else:
            player2.score = player2.score + 1
        screen.title(f"Player 1:  {player1.score} Player 2:  {player2.score}")
        score.updateScoreboard(player1.score,player2.score)
        ball.setpos(0,0)
        ballSpeed = 5
        ball.setheading(random.choice(ballRotations)) # sets the ball to face a random direction
        time.sleep(1)
    #print(ball.ycor(), ball.heading())
    screen.update()
    turtle.ontimer(update, int(1000/FPS))

# initialise player 1
player1Turtle = turtle.Turtle()    # initialise player1 as its own turtle
player1 = Player(player1Turtle, "left")
player1Turtle.setpos(-(WIDTH/2)+50,0)
# initialises player 2
player2Turtle = turtle.Turtle()
player2 = Player(player2Turtle, "right")
player2Turtle.setpos((WIDTH/2)-50,0)
player2.xcor = player2Turtle.xcor()
# initialise the ball
ball = turtle.Turtle() # initialises the ball as a turtle
ball.speed(0)
ball.shape("square") # sets the shape and size of the ball
ball.shapesize(0.5,0.5)
ball.setheading(45)
ball.tilt(-45) # makes the ball look like its constantly facing up, not rotated in the direction its travelling
ball.penup()
ball.resizemode("user")
ballRotations = [45,135,225,315]

player1.update()
player2.update()

# makes a screen and listens for w/s to move up and down
screen = turtle.Screen()
screen.setup(WIDTH,HEIGHT)  # makes the window that the game is in the correct size
screen.tracer(0) # makes the screen no longer auto update
height = screen.window_height()/2
width = screen.window_width()/2
screen.title(f"Player 1:  {player1.score} Player 2:  {player2.score}")
screen.listen() # makes the screen listen for inputs
if not ladVsLad:
    screen.onkeypress(player1.startMovingUp, "w") # detects w/s key presses
    screen.onkeyrelease(player1.stopMovingUp, "w")
    screen.onkeypress(player1.startMovingDown, "s")
    screen.onkeyrelease(player1.stopMovingDown, "s")
else:
    opponent2 = aiLad(player1)
    multiplayer = False
# detects inputs from arrow keys for player 2
if multiplayer:
    screen.onkeypress(player2.startMovingUp, "Up")
    screen.onkeyrelease(player2.stopMovingUp, "Up")
    screen.onkeypress(player2.startMovingDown, "Down")
    screen.onkeyrelease(player2.stopMovingDown, "Down")
else:
    opponent = aiLad(player2)

score = goof.scoreBoard() # initialises the scoreboard
score.updateScoreboard()

goof.drawCenterline() # draws the center line

update()  # Start the update loop

turtle.mainloop() # keeps turtle window responsive
