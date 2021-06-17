#Dominic DaCosta - dld5mxn

#Importing necessary modules
import pygame
import gamebox

###################################### SCENERY/CHARACTERS ##############################################
'''
Creating camera size. This section creates all character sprites to be used in the game by players, as well as creating the maze
background that is going to be used
'''
camera = gamebox.Camera(800,600)

background = gamebox.from_image(340,310, 'Pacman backgroun(3).png')
background.scale_by(0.7)

red_ghost = gamebox.from_image(470, 390, 'Pacman_RedGhost(2).png')
ghosts = [
    red_ghost
]
red_ghost.scale_by(0.03)
camera.draw(red_ghost)

pacman = gamebox.from_image(210, 230, 'Pacman(2).png')
pacman.scale_by(0.022)

#################### GAME SETUP ###############
'''
Creates all walls that will stop players from phasing through boundaries. Hearts and coins are set into lists to be later used easily in for loops 
to create game functionality.
'''
#bottom wall
ground = gamebox.from_color(450, 430, "red", 900, 50)
#right wall
outer_wall1 = gamebox.from_color(500, 400, 'red', 50, 900)
#left wall
outer_wall2 = gamebox.from_color(175, 400, 'red', 50, 900)
#top wall
outer_wall3 = gamebox.from_color(200, 180, 'red', 900, 50)
#leftmost rectangle
inside_wall1 = gamebox.from_color(260, 305, 'red', 40 ,110) #vertical portion
inside_wall2 = gamebox.from_color(340, 345,'red', 180, 35)  #horizontial portion

#leftmost square
inside_wall3 = gamebox.from_color(340, 270, 'red', 40, 40)
#rightmost square
inside_wall4 = gamebox.from_color(415, 270, 'red', 40, 40)


#Heart sprites created
'''
Hearts created then placed into a list to be iterated
'''
#heart_1 = gamebox.from_color(290, 130, 'red', 40, 40)
heart_2 = gamebox.from_color(360, 130, 'red', 40, 40)
#heart_3 = gamebox.from_color(430, 130, 'red', 40, 40)
hearts = [
    #heart_1,
    heart_2
    #heart_3
]
#Creating coins to be collected
coins = [
    gamebox.from_color(480, 380, "yellow", 12, 12),
    gamebox.from_color(410, 230, "yellow", 12, 12),
    gamebox.from_color(230, 350, "yellow", 12, 12),
    gamebox.from_color(190, 270, "yellow", 12, 12),
    gamebox.from_color(210, 350, "yellow", 12, 12),
    gamebox.from_color(350, 380, "yellow", 12, 12),
    gamebox.from_color(450, 380, "yellow", 12, 12),
    gamebox.from_color(220, 340, "yellow", 12, 12),
    gamebox.from_color(210, 310, "yellow", 12, 12),
    gamebox.from_color(300, 310, "yellow", 12, 12)
]
#creating walls to establish game boundaries
walls = [
    ground,
    outer_wall1,
    outer_wall2,
    outer_wall3,
    inside_wall1,
    inside_wall2,
    inside_wall3,
    inside_wall4
]
#Setting Values for functions
total_hearts = 3
total_coins = 10
score = 0
timer = 91
start_screen_on = True
instructions_screen = False
###################################### INTERACTIVE ELEMENTS ##################################

#control mechanics
def tick(keys):
    #Calling all neccesarry global values declared to be used in tick function
    global total_coins, coins, total_hearts, score
    global start_screen_on, timer ,instructions_screen
    #Start of game functionality
    if start_screen_on == False:
        '''
        Enters when start screen is exited by pressing space
        '''
        # Text Boxes
        camera.clear('black')
        game_win = gamebox.from_text(300, 300, 'GAME OVER. You Win!', 40, 'blue')
        timer_box = gamebox.from_text(400, 500, 'Timer: '+ str(int(timer)) + 'seconds left', 60, 'Blue')
        return_box = gamebox.from_text(400, 560, 'To return to Start Screen, press Backspace.', 40, 'White')
        score_box = gamebox.from_text(400, 50, 'Score: ' + str(score) + '/10 coins collected', 60, 'Blue')  #Coin counter created
        health_box = gamebox.from_text(370, 90, 'Hearts Remaining:', 60, 'Red')     #Health bar showing total hearts left created
        #time goes down every second
        timer -= 0.05
        if timer <= 0:
            gamebox.pause()
        '''
        Loops through list of coins created. For every coin listed, if pacman touches one of the specified coins, score is psoitively incremented by one and 
        coin that is touched is removed from list as well as from being displayed on screen
        '''
        for coin in coins:
            if pacman.touches(coin):
                total_coins -= 1
                score += 1
                coins.remove(coin)
            camera.draw(coin)
        if total_coins == 0:
            camera.draw(game_win)
            gamebox.pause()

        for heart in hearts:
            if pacman.touches(red_ghost):
                total_hearts -= 1
                hearts.remove(heart)

        for ghost in ghosts:
            if ghost.touches(pacman):
                total_hearts -= 1
                pacman.move_to_stop_overlapping(red_ghost)

        if pacman.touches(red_ghost):
            gamebox.pause()

        #player 1 controls (pacman)
        if pygame.K_UP in keys:
            pacman.top -= 5
        if pygame.K_DOWN in keys:
            pacman.top += 5
        if pygame.K_LEFT in keys:
            pacman.x -= 5
        if pygame.K_RIGHT in keys:
            pacman.x += 5
        # player 2 controls (ghost)
        if pygame.K_w in keys:
            red_ghost.top -= 3
        if pygame.K_s in keys:
            red_ghost.top += 3
        if pygame.K_a in keys:
            red_ghost.x -= 3
        if pygame.K_d in keys:
            red_ghost.x += 3
        # Game Physics - creating game boundaries
        for wall in walls:
            # Pacman Boundaries
            if pacman.bottom_touches(wall):
                pacman.yspeed = 0
                if pygame.K_UP in keys:
                    pacman.yspeed = -15
            if pacman.touches(wall):
                pacman.move_to_stop_overlapping(wall)
            camera.draw(wall)
            # Red Ghost Boundaries
            if red_ghost.bottom_touches(wall):
                red_ghost.yspeed = 0
                if pygame.K_UP in keys:
                    red_ghost.yspeed = -15
            if red_ghost.touches(wall):
                red_ghost.move_to_stop_overlapping(wall)
            camera.draw(wall)
        # Drawing all sprites onto game plane
        camera.clear('black')
        gamebox.from_text(700, 200, 'Score: ' + str(score), 70, 'Red')
        camera.draw(background)
        camera.draw(coin)
        camera.draw(red_ghost)
        camera.draw(pacman)
        camera.draw(timer_box)
        camera.draw(return_box)
        camera.draw(score_box)
        camera.draw(health_box)
        #camera.draw(heart_1)
        camera.draw(heart_2)
        #camera.draw(heart_3)
        camera.display()
        #User exits to starting screen using backspace key
        if pygame.K_BACKSPACE in keys:
            #resets settings
            timer = 91
            start_screen_on = True
    else:
        '''
        Should be used when start screen is active. A text displaying the "start screen" text as well as instructions should appear.
        Player exits start screen by pressing spacebar
        '''
        start_screen = gamebox.from_text(400, 200, "Welcome to Pacman! Press Space to begin.", 30, 'Blue')
        student_ID = gamebox.from_text(400, 250, 'Created by: Dominic DaCosta (dld5mxn)', 30, 'Blue')
        instructions_prompt = gamebox.from_text(400, 400, 'Press tab to view instructions', 30, 'Red')
        start_image = gamebox.from_image(400, 300, 'pacman_start.png')
        start_image.scale_by(1.5)
        #drawing start screen
        camera.clear('Black')
        camera.draw(start_screen)
        camera.draw(student_ID)
        camera.draw(start_image)
        camera.draw(instructions_prompt)
        camera.display()
        #turning start screen on
        if pygame.K_SPACE in keys:
            start_screen_on = False
        #going to instructions screen
        if pygame.K_TAB in keys:
            instructions_screen = True
        if instructions_screen == True:
            '''
            Instructions screen. Displays rules using text. User can escape back to original starting screen using the backspace key.
            '''
            camera.clear('Black')
            rules = gamebox.from_image(400, 100, 'Pacman Rules.png')
            rules.scale_by(0.3)
            instructions_1 = gamebox.from_text(400, 350, 'Player 1 moves Pacman with Arrow Keys. Player 2 moves ghost with AWSD.', 30, 'Blue')
            instructions_2 = gamebox.from_text(400, 400, 'Pacman must collect all coins before time expires to win.', 30, 'Blue' )
            instructions_3 = gamebox.from_text(400, 450, 'Ghost must catch Pacman to win. If he catches pacman, game will end. Good Luck!', 25, 'Blue')
            exit_instructions = gamebox.from_text(400, 500, 'Press Backspace to return to start screen', 35, 'White' )
            if pygame.K_BACKSPACE in keys:
                instructions_screen = False
            #displaying instructions screen
            camera.draw(rules)
            camera.draw(instructions_1)
            camera.draw(instructions_2)
            camera.draw(instructions_3)
            camera.draw(exit_instructions)
            camera.display()
# tell gamebox to call the tick method 30 times per second
ticks_per_second = 30
gamebox.timer_loop(ticks_per_second, tick)