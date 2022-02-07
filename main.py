from curses import wrapper , textpad
from ascii import BIRD , GAME_OVER
import curses
import random
score = 0
BIRD_X = 1



def endScreen(stdscr):
    global score
    stdscr.nodelay(False)
    curses.beep()
    stdscr.erase()
    lry , lrx = stdscr.getmaxyx()
    subscr = stdscr.subwin((lry-8)//2, (lrx-56)//2)
    subscr.addstr(0,0,GAME_OVER.format(score//3), curses.color_pair(1))
    stdscr.refresh()
    curses.napms(2000)
    stdscr.getkey()


def getBird(lry ,bird_y  , direction , counter , pillar):
    if not bird_y:
        bird_y = random.randint(4 , lry-15)
    else:
        if direction == curses.KEY_UP:
            bird_y -= 1
        elif direction == curses.KEY_DOWN:
            bird_y += 1
        elif direction == "gravity" and counter%3 == 0:
            bird_y += 1
        if bird_y == 0 or bird_y == lry-4:
            return "END"
    
    for start_x  , end_y in pillar:
        if start_x in range(10 , 15):
            if bird_y in range(end_y) or bird_y in range(end_y+5 , lry):
                return "END"
    
    return bird_y
    


def getPillar(pillar , lry , lrx , counter):
    temp = [(start_x- 1 , end_y) for (start_x , end_y) in pillar if start_x-1 >= 3]
    pillar = temp.copy()

    if counter%40 == 0:  
        start_x = lrx
        end_y = random.randint(2, lry-5)
        pillar.append((start_x , end_y))
        pillar.append((start_x-1 , end_y))
        pillar.append((start_x-2 , end_y))
    return pillar

def main(stdscr):
    curses.resize_term(30,120)
    curses.init_pair(1, 12 ,0)
    curses.init_pair(2, 10, 0)
    global score
    bird_y ,pillar ,counter = None ,[] ,  0
    while True:
        stdscr.bkgd(" ",curses.color_pair(1))
        direction = "gravity"
        stdscr.erase()
        lry , lrx = stdscr.getmaxyx()
        stdscr.addstr(1, (lrx- 6)//2,f"SCORE:{score//3}")
        textpad.rectangle(stdscr , 2, 2 , lry-2, lrx-2)
        curses.curs_set(False)
        stdscr.nodelay(True)

        curses.flushinp()
        curses.napms(50)
        choice = stdscr.getch()
        if choice == curses.KEY_UP or choice == curses.KEY_DOWN:
            direction = choice

        bird_y = getBird(lry , bird_y , direction , counter , pillar)
        if bird_y == 'END':
            return endScreen(stdscr)
        for idx,ele in enumerate(BIRD.split("\n")):
            if ele.strip():
                        stdscr.addstr(bird_y+idx , 10 , ele , curses.color_pair(2))
 
        pillar = getPillar(pillar , lry-3 , lrx-3 , counter)
        flag = False
        for start_x , end_y in pillar:
            if start_x == 10:
                flag = True
            for i in range(3 , end_y):
                stdscr.addstr(i , start_x , "@" , curses.color_pair(1))
            for i in range(end_y+8 , lry-2):
                stdscr.addstr(i , start_x , "@" ,curses.color_pair(1))
        
        if flag:
            score += 1

        stdscr.refresh() 
        counter += 1
        


wrapper(main)