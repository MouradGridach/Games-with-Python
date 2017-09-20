
# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
paddle1_pos = [0, 0]
paddle2_pos = [0, 0]
paddle1_vel = [0, 0]
paddle2_vel = [0, 0]
ball_pos = [0, 0]
ball_vel = [0, 0]
score1 = 0
score2 = 0

# helper function that spawns a ball by updating the 
# ball's position vector and velocity vector
# if right is True, the ball's velocity is upper right, else upper left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos[0] = WIDTH/2
    ball_pos[1] = HEIGHT/2
    h_vel = random.randrange(120, 240)/60
    v_vel = random.randrange(60, 180)/60
    if right:
        ball_vel = [h_vel, -v_vel]
    else:
        ball_vel = [-h_vel, v_vel]  

# define event handlers

def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are floats
    global score1, score2  # these are ints
    ball_init(True)
    pos1 = random.randrange(0, 220)
    pos2 = random.randrange(0, 220)
    paddle1_pos[0] = pos1
    paddle1_pos[1] = pos1 + PAD_HEIGHT
    paddle2_pos[0] = pos2
    paddle2_pos[1] = pos2 + PAD_HEIGHT
    score1 = 0
    score2 = 0
    
def restart():
    new_game()
    
def draw(c):
    global vel, score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos[1] += paddle1_vel[1];    
    paddle1_pos[0] += paddle1_vel[0];
    paddle2_pos[1] += paddle2_vel[1];    
    paddle2_pos[0] += paddle2_vel[0];

    if paddle1_pos[0] < 0:
        paddle1_pos = [0, PAD_HEIGHT]
    elif paddle1_pos[1] > HEIGHT:
        paddle1_pos = [HEIGHT - PAD_HEIGHT, HEIGHT]
        
    if paddle2_pos[0] < 0:
        paddle2_pos = [0, PAD_HEIGHT]
    elif paddle2_pos[1] > HEIGHT:
        paddle2_pos = [HEIGHT - PAD_HEIGHT, HEIGHT]
        
    
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # draw paddles
    c.draw_line((0, paddle1_pos[0]), (0, paddle1_pos[1]), 2*PAD_WIDTH, "White")
    c.draw_line((600, paddle2_pos[0]), (600, paddle2_pos[1]), 2*PAD_WIDTH, "White")
     
    # update ball 
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        ball_vel[0] = -ball_vel[0]
    elif ball_pos[0] >= (WIDTH -1) - BALL_RADIUS-PAD_WIDTH:
        ball_vel[0] = -ball_vel[0]
    elif ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]   
    elif ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    #c.draw_circle(ball_pos,BALL_RADIUS, 2, "Green", "Red")
    
    # update scores
    cond1 = paddle1_pos[0] > ball_pos[1] or paddle1_pos[1] < ball_pos[1]
    cond2 = (ball_pos[0] - BALL_RADIUS) <= PAD_WIDTH
    cond3 = paddle2_pos[0] > ball_pos[1] or paddle2_pos[1] < ball_pos[1]
    cond4 = (ball_pos[0] + BALL_RADIUS) >= WIDTH - PAD_WIDTH -1
    
    if ((not cond1) and cond2) or ((not cond3) and cond4):
        #print "yeeeeees"
        ball_vel[0] = ball_vel[0] + ball_vel[0]*0.1
        #print ball_vel[0], ball_vel[0]
        ball_pos[0] += ball_vel[0]
    
    if cond1 and cond2:
        score2 +=1
        ball_init(True)
    elif cond3 and cond4:
        score1 +=1
        ball_init(False)
    # draw ball and scores
    c.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    c.draw_text(str(score1), (150, 40), 42, "White")
    c.draw_text(str(score2), (450, 40), 42, "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    acc = 8
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel[0]+= acc
        paddle2_vel[1]+= acc
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel[0]-= acc
        paddle2_vel[1]-= acc
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel[0]+= acc
        paddle1_vel[1]+= acc
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel[0]-= acc
        paddle1_vel[1]-= acc
        
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle2_vel[0] = 0
    paddle2_vel[1] = 0
    paddle1_vel[0] = 0
    paddle1_vel[1] = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.add_button("Restart", restart, 100)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()
