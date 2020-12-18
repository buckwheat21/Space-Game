import pgzrun
from random import *

WIDTH = 1000
HEIGHT = 600
score = 0
additional_speed = 0
JUNK_SPEED = 5
SATELLITE_SPEED = 9
DEBRIS_SPEED = 9
LASER_SPEED = -5
Red = (255,0,0)

BACKGROUND_IMAGE = "space_b"

JUNK_IMG = "space_junk"

SATELLITE_IMG = 'satellite'

DEBRIS_IMG = 'space_debris2'

LASER_IMG = 'laser_red'


sounds.spacelife.play(-1)
# initialize junks
junks = [] # created a list to store our junks
score_board_height = 60
for i in range(5):  # make 5 junks
   junk = Actor(JUNK_IMG)
   x_pos = randint(-500, -50)
   y_pos = randint(score_board_height, HEIGHT - junk.height)
   junk.pos = (x_pos, y_pos)  # rect_position = (x, y)
   junks.append(junk)  # add each junk to our list

#initialize satellite sprite
satellite = Actor(SATELLITE_IMG)
x_sat = randint (-500, -50)
y_sat = randint ( score_board_height, HEIGHT - satellite.height)
satellite.topright = (x_sat, y_sat)

#initialize debris sprite
debris = Actor(DEBRIS_IMG)
x_deb = randint (-500, -50)
y_deb = randint ( score_board_height, HEIGHT - debris.height)
debris.topright = (x_deb, y_deb)

#intialize lazers
lasers = []


player = Actor('ufo')
player.midright = (WIDTH - 15, HEIGHT/2)
def junk_update():
   global score
   global additional_speed
   score_board_height = 60
   for junk in junks:
       junk.x += JUNK_SPEED
       junk.x += additional_speed
       collision = player.colliderect(junk)
       if (junk.left > WIDTH or collision == 1):
           x_pos = randint(-150,-50)
           y_pos = randint(score_board_height, HEIGHT-junk.height)
           junk.topleft = (x_pos,y_pos)  
       if (collision ==1):
           if (score >=10 and score%10 == 0):
               additional_speed+= 2
               print (additional_speed)
           score+=1
           sounds.collect_pep.play()

def satellite_update():
   global score
   satellite.x+= SATELLITE_SPEED

   collision = player.colliderect(satellite)
   if satellite.left > WIDTH or collision == 1:
       x_sat = randint (-500, -50)
       y_sat = randint (score_board_height, HEIGHT - satellite.height)
       satellite.topright = (x_sat, y_sat)

   if collision == 1:
       score+= -10
       sounds.explosion.play()
def debris_update():
   global score
   debris.x+= DEBRIS_SPEED

   collision = player.colliderect(debris)
   if debris.left > WIDTH or collision == 1:
       x_deb = randint (-500, -50)
       y_deb = randint (score_board_height, HEIGHT - debris.height)
       debris.topright = (x_sat, y_sat)

   if collision == 1:
       score+= -5
       sounds.explosion.play()


def updateLasers():
   global score
   for laser in lasers:
      laser.x += LASER_SPEED
      if laser.right < 0:
         lasers.remove(laser)
      if satellite.colliderect(laser) == 1:
         lasers.remove(laser)
         x_sat = randint (-500, -50)
         y_sat = randint (score_board_height, HEIGHT - satellite.height)
         satellite.topright = (x_sat, y_sat)
         score += -10
         sounds.explosion.play()
      if debris.colliderect(laser) == 1:
         lasers.remove(laser)
         x_deb = randint (-500, -50)
         y_deb = randint (score_board_height, HEIGHT - debris.height)
         debris.topright = (x_deb, y_deb)
         score += 10
         sounds.collect_pep.play()

      if junk in junks:
         if junk.colliderect(laser)== 1:
            lasers.remove(laser)
            x_pos = randint(-150,-50)
            y_pos = randint(score_board_height, HEIGHT-junk.height)
            junk.topleft = (x_pos,y_pos)
            score += 5

         

             
player.laserActive = 1
   
   
       
   
def player_update():
   if (keyboard.up == 1):
       player.y += (-5)
   elif (keyboard.down == 1):
       player.y += (5)

   if player.top < 60:
       player.top = 60

   if player.bottom > HEIGHT:
       player.bottom = HEIGHT

   if keyboard.space == 1:
       laser = Actor (LASER_IMG)
       laser.midright = (player.midleft)
       fireLasers(laser)



def update():
   #if score>= 0:
      player_update()
      junk_update()
      satellite_update()
      debris_update ()
      updateLasers()


def draw():
   screen.clear()
   screen.blit(BACKGROUND_IMAGE,(0,0))
   player.draw()
   for junk in junks:
       junk.draw()
   satellite.draw()
   debris.draw()

   for laser in lasers:
      laser.draw()

   #if score < 0:
      #game_over_text = 'GAME OVER!'
      #screen.draw.text(game_over_text, center=(WIDTH/2, HEIGHT/2), fontsize=80,color='red', ocolor='white', owidth=0.5)

   #if score > 200:
      #game_won_text = 'YOU WIN!'
      #screen.draw.text(game_won_text, center=(WIDTH/2, HEIGHT/2), fontsize=80,color='green', ocolor='white', owidth=0.5)
   
   show_score = "Score: " + str(score)
   screen.draw.text(show_score, topleft=(700,15), fontsize = 35, color="black")




# activating lasers (template code)
player.laserActive = 1  # add laserActive status to the player

def makeLaserActive():  # when called, this function will make lasers active again
    global player
    player.laserActive = 1

def fireLasers(laser):
    if player.laserActive == 1:  # active status is used to prevent continuous shoot when holding space key
        player.laserActive = 0
        clock.schedule(makeLaserActive, 0.2)  # schedule an event (function, time afterwhich event will occur)
        sounds.laserfire02.play()  # play sound effect
        lasers.append(laser)  # add laser to lasers list




pgzrun.go()
