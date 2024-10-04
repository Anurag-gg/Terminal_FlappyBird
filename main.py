import platform
import random
import time

# Cross-platform compatibility
if platform.system() == "Windows":
    try:
        import windows_curses as curses
    except ImportError:
        import curses
else:
    import curses

from curses import wrapper, textpad

# ASCII Art
BIRD = [
    " ___",
    "(-v')",
    "//)",
    "V_/_"
]

PIPE = [
    "██",
    "██",
    "██"
]

GAME_OVER = r'''
   _________    _____   ____     _______   ________
  / ___\__  \  /     \_/ __ \   /  _  \  \/ / ____/
 / /_/  > __ \|  Y Y  \  ___/  /  /_\  \   / __/
 \___  (____  /__|_|  /\___  >/    |    \ / /___
/_____/     \/      \/     \/ \____|__  // /____/
                                      \/
'''

TITLE = r'''
 ________   __                                  ______ _         __
|_   __  |[  |                                |_   _ (_)       |  ]
  | |_ \_| | | .__   _ .--..--.  _ .--..--.     | |_) |__   _ .--.| |
  |  _|    | '/ .'`\ [ `.-. .-. [ `.-. .-. |    |  __'.\ \ [ `/'`\' |
 _| |_     |  | \__. || | | | | || | | | | |   _| |__) |\ '| |     |
|_____|   [_\| '.__.'[___||__||__]___||__||__]|_______[/[__]___.' [___]
'''

class FlappyBird:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.bird_y = None
        self.bird_velocity = 0
        self.pipes = []
        self.game_speed = 50
        self.difficulty = 1
        self.gravity = 0.5
        self.jump_strength = -2.5
        self.paused = False
        self.game_state = "title"  # Can be "title", "playing", "paused", "game_over"

    def reset_game(self):
        self.score = 0
        self.bird_y = None
        self.bird_velocity = 0
        self.pipes = []
        self.game_speed = 50
        self.difficulty = 1
        self.paused = False
        self.game_state = "playing"

    def get_bird(self, max_y, action):
        if not self.bird_y:
            self.bird_y = max_y // 2

        if action == "jump":
            self.bird_velocity = self.jump_strength
        
        self.bird_velocity += self.gravity
        self.bird_y += self.bird_velocity

        # Clamp bird position
        self.bird_y = max(4, min(max_y - 7, self.bird_y))

        for pipe_x, pipe_height in self.pipes:
            if pipe_x in range(5, 10):
                if self.bird_y < pipe_height or self.bird_y > pipe_height + 8:
                    return False
        return True

    def get_pipes(self, max_y, max_x):
        self.pipes = [(x - 1, h) for x, h in self.pipes if x > 0]
        if not self.pipes or self.pipes[-1][0] < max_x - 20:
            pipe_height = random.randint(5, max_y - 15)
            self.pipes.append((max_x - 2, pipe_height))

    def draw_game(self, stdscr):
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()

        # Draw border
        textpad.rectangle(stdscr, 1, 1, max_y - 2, max_x - 2)

        # Draw bird
        for i, line in enumerate(BIRD):
            if 0 <= int(self.bird_y) + i < max_y:
                stdscr.addstr(int(self.bird_y) + i, 5, line[:max_x-5], curses.color_pair(2))

        # Draw pipes
        for pipe_x, pipe_height in self.pipes:
            for i in range(pipe_height):
                if 2 <= i + 2 < max_y and 0 <= pipe_x < max_x:
                    stdscr.addstr(i + 2, pipe_x, PIPE[i % 3], curses.color_pair(3))
            for i in range(pipe_height + 9, max_y - 2):
                if i < max_y and 0 <= pipe_x < max_x:
                    stdscr.addstr(i, pipe_x, PIPE[(i - pipe_height - 9) % 3], curses.color_pair(3))

        # Draw score and high score
        score_str = f"Score: {self.score}"
        high_score_str = f"High Score: {self.high_score}"
        if max_x > len(score_str) + 2:
            stdscr.addstr(0, 2, score_str[:max_x-2], curses.color_pair(1))
        if max_x > len(high_score_str) + 2:
            stdscr.addstr(0, max(2, max_x - len(high_score_str) - 2), high_score_str[:max_x-2], curses.color_pair(1))

        if self.paused and max_y > 2 and max_x > 8:
            pause_msg = "PAUSED"
            stdscr.addstr(max_y // 2, max(0, (max_x - len(pause_msg)) // 2), pause_msg[:max_x], curses.color_pair(1) | curses.A_BOLD)

        stdscr.refresh()

    def show_game_over(self, stdscr):
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()
        
        game_over_lines = GAME_OVER.split('\n')
        start_y = max(0, (max_y - len(game_over_lines)) // 2)
        start_x = max(0, (max_x - max(len(line) for line in game_over_lines)) // 2)
        
        for i, line in enumerate(game_over_lines):
            if start_y + i < max_y:
                stdscr.addstr(start_y + i, start_x, line[:max_x-start_x], curses.color_pair(1))
        
        if start_y + len(game_over_lines) + 2 < max_y:
            score_str = f"Your Score: {self.score}"
            stdscr.addstr(start_y + len(game_over_lines) + 2, max(0, (max_x - len(score_str)) // 2), score_str[:max_x], curses.color_pair(2))
        
        if start_y + len(game_over_lines) + 4 < max_y:
            instruction_str = "Press 'N' for new game or 'Q' to quit"
            stdscr.addstr(start_y + len(game_over_lines) + 4, max(0, (max_x - len(instruction_str)) // 2), instruction_str[:max_x], curses.color_pair(1))
        
        stdscr.refresh()

    def show_title_screen(self, stdscr):
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()
        
        title_lines = TITLE.split('\n')
        start_y = max(0, (max_y - len(title_lines)) // 2)
        start_x = max(0, (max_x - max(len(line) for line in title_lines)) // 2)
        
        for i, line in enumerate(title_lines):
            if start_y + i < max_y:
                stdscr.addstr(start_y + i, start_x, line[:max_x-start_x], curses.color_pair(2))
        
        instructions = [
            "Press 'N' to start a new game",
            "Press 'S' for settings",
            "Press 'Q' to quit"
        ]
        
        for i, instruction in enumerate(instructions):
            if start_y + len(title_lines) + 2 + i * 2 < max_y:
                stdscr.addstr(start_y + len(title_lines) + 2 + i * 2, max(0, (max_x - len(instruction)) // 2), instruction[:max_x], curses.color_pair(1))
        
        stdscr.refresh()

    def show_settings(self, stdscr):
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()

        settings = [
            ("Settings", curses.A_BOLD),
            (f"Game Speed: {self.game_speed}", curses.A_NORMAL),
            (f"Difficulty: {self.difficulty:.1f}", curses.A_NORMAL),
            ("Press 'G' to change game speed", curses.A_NORMAL),
            ("Press 'D' to change difficulty", curses.A_NORMAL),
            ("Press 'B' to go back", curses.A_NORMAL)
        ]

        start_y = max(0, (max_y - len(settings)) // 2)

        for i, (setting, attr) in enumerate(settings):
            if start_y + i < max_y:
                stdscr.addstr(start_y + i, max(0, (max_x - len(setting)) // 2), setting[:max_x], curses.color_pair(1) | attr)

        stdscr.refresh()

    def run(self, stdscr):
        curses.curs_set(0)
        stdscr.nodelay(True)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

        while True:
            if self.game_state == "title":
                self.show_title_screen(stdscr)
                while True:
                    key = stdscr.getch()
                    if key == ord('n'):
                        self.reset_game()
                        break
                    elif key == ord('s'):
                        self.show_settings(stdscr)
                        while True:
                            key = stdscr.getch()
                            if key == ord('g'):
                                self.game_speed = (self.game_speed % 90) + 10
                                self.show_settings(stdscr)
                            elif key == ord('d'):
                                self.difficulty = round((self.difficulty % 2) + 0.1, 1)
                                self.show_settings(stdscr)
                            elif key == ord('b'):
                                break
                        self.show_title_screen(stdscr)
                    elif key == ord('q'):
                        return
            
            elif self.game_state == "playing":
                last_update_time = time.time()
                while True:
                    key = stdscr.getch()
                    
                    if key == ord('p'):
                        self.paused = not self.paused
                        self.draw_game(stdscr)
                        continue

                    if self.paused:
                        if key == ord('r'):
                            self.paused = False
                        elif key == ord('n'):
                            self.reset_game()
                            break
                        elif key == ord('q'):
                            self.game_state = "title"
                            break
                        continue

                    action = "gravity"
                    if key in [ord(' '), curses.KEY_UP, ord('w')]:
                        action = "jump"
                    
                    if not self.get_bird(stdscr.getmaxyx()[0], action):
                        self.game_state = "game_over"
                        break
                    
                    current_time = time.time()
                    if current_time - last_update_time >= self.game_speed / 1000:
                        self.get_pipes(stdscr.getmaxyx()[0], stdscr.getmaxyx()[1])
                        self.draw_game(stdscr)
                        
                        self.score += 1
                        if self.score > self.high_score:
                            self.high_score = self.score
                        
                        if self.score % 100 == 0:
                            self.difficulty += 0.1
                            self.game_speed = max(10, int(self.game_speed * 0.9))
                        
                        last_update_time = current_time

            elif self.game_state == "game_over":
                self.show_game_over(stdscr)
                while True:
                    key = stdscr.getch()
                    if key == ord('n'):
                        self.reset_game()
                        break
                    elif key == ord('q'):
                        self.game_state = "title"
                        break

if __name__ == "__main__":
    game = FlappyBird()
    curses.wrapper(game.run)