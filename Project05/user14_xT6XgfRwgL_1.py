# implementation of card game - Memory

import simplegui
import random

card1 = -1
card2 = -1
state = 0
moves = 0

# helper function to initialize globals
def init():
    global lst_num, lst_clk, exposed, moves
    exposed = []
    lst_num = []
    lst_clk = []
    moves = 0
    label.set_text("Moves = "+str(moves))
    l1 = range(8)
    l2 = range(8)
    lst_num = l1 + l2
    random.shuffle(lst_num)
    for i in range(16):
        exposed.append(False)
        l = []
        l.append(lst_num[i])
        l.append(i)
        lst_clk.append(l)
    
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, current_index, lst_clk, lst_num, card1, card2, moves
    current_index = (pos[0] // 50)
    if exposed[current_index] != True:
        exposed[current_index] = True
        moves += 1 
        label.set_text("Moves = "+str(moves))
        if state == 0:
            state = 1
            card1 = current_index
        elif state == 1:
            state = 2
            card2 = current_index
        else:
            if lst_num[card1] == lst_num[card2]:
                card1 = current_index
            else:
                exposed[card1] = False
                exposed[card2] = False
                card1 = current_index
            state = 1   
                    
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global lst_num, current_index, lst_clk
    for i in range(0, len(lst_num)):
        if exposed[i] == True:
            l = lst_clk[i]
            canvas.draw_text(str(l[0]), (l[1]*50+25, 40), 40, "White")
        else:
            canvas.draw_polygon([(i*50, 0), ((i+1)*50, 0), ((i+1)*50, 100), (i*50, 100)], 1, "Blue", "Green")
    

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", init)
label = frame.add_label("Moves = 0")

# initialize global variables
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()


# Always remember to review the grading rubric