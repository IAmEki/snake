# Copyright 2019 Erik Nossborn

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from microbit import *
import random

difficulty = 1
display.show("1")
while True:
    difficulty += button_b.get_presses()
    difficulty -= button_a.get_presses()
    if difficulty < 1:
        difficulty = 1
    if difficulty > 5:
        difficulty = 5
    display.show(str(difficulty))
    if button_a.is_pressed() and button_b.is_pressed():
        sleep(500)
        break
    sleep(100)

display.clear()
#reset buttons
button_a.was_pressed()
button_b.was_pressed()


#should be using a deque
worm = [[0,0]] #list representing the worm
display.set_pixel(0,0,9)

#very inefficient
def new_apple():
    while True:
        new = [random.randint(0,4),random.randint(0,4)]
        if display.get_pixel(new[0],new[1]) == 0:
            break
    return new

apple = [random.randint(1,4),random.randint(1,4)] #first apple not on row/column 0
display.set_pixel(apple[0],apple[1],7)

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

direction = RIGHT

while True:
    if button_a.was_pressed():
        direction = direction - 1
        if direction < 0:
            direction = 3
    if button_b.was_pressed():
        direction = direction + 1
        if direction > 3:
            direction = 0
            
    nextspot = list(worm[-1]) #last spot
            
    if direction == RIGHT:
        nextspot[0] = nextspot[0]+1
        if nextspot[0] > 4:
            nextspot[0] = 0
    if direction == LEFT:
        nextspot[0] = nextspot[0]-1
        if nextspot[0] < 0:
            nextspot[0] = 4
    if direction == DOWN:
        nextspot[1] = nextspot[1]+1
        if nextspot[1] > 4:
            nextspot[1] = 0
    if direction == UP:
        nextspot[1] = nextspot[1]-1
        if nextspot[1] < 0:
            nextspot[1] = 4
    if display.get_pixel(nextspot[0],nextspot[1]) > 0:
        if nextspot[0] == apple[0] and nextspot[1] == apple[1]:
            #we have found an apple!
            display.set_pixel(worm[-1][0],worm[-1][1],5)
            display.set_pixel(nextspot[0],nextspot[1],9)
            worm.append(nextspot)
            apple = new_apple()
            display.set_pixel(apple[0],apple[1],7)
        else:
            #we have hit ourselves!
            break
    else:
        display.set_pixel(nextspot[0],nextspot[1],9)
        display.set_pixel(worm[-1][0],worm[-1][1],5)
        display.set_pixel(worm[0][0],worm[0][1],0)
        worm.append(nextspot)
        worm.pop(0)
    sleep(1000//difficulty)
display.scroll(str(len(worm)))

