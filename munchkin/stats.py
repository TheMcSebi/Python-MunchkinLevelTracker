from __future__ import annotations
from pygame import Surface
from pygame.locals import *
from pygame.event import Event
from pygame.draw import circle, line
from pygame.transform import flip

from .constants import *
from .components.button import Button

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .munchkin import Munchkin

class Stats:
    """
    Stats screen
    """
    def __init__(self, game : Munchkin) -> None:
        self.g = game
        self.window = self.g.window
        self.stroke_width = 5
        self.circle_radius = 10
    
    #########################################################################################
    
    def setup(self) -> None:
        self.bw = self.g.w//2
        self.bh = self.g.h//8
        self.img = Surface((self.g.w-150, self.g.h-100))
        self.img.fill(BLACK)
        self.buttons = [Button(self.g, "Back", (100, 50), (200, 100), self.button_handler, FONT_LG)]
        self.w, self.h = self.img.get_size()

        # find last timestamp
        last_timestamp = 0
        for p in self.g.players:
            for d in p["history"]:
                if d[1] > last_timestamp:
                    last_timestamp = d[1]
        
        tickmult = self.w/last_timestamp
        
        scoremult = self.h//10

        for p in self.g.players:
            color = self.g.player_colors[p["num"]]
            prev_pos = (tickmult, scoremult)
            for d in p["history"]:
                score = d[0]
                ticks = d[1]
                pos = (ticks*tickmult, score*scoremult)
                circle(self.img, color, pos, self.circle_radius)
                line(self.img, color, prev_pos, pos, self.stroke_width)
                prev_pos = pos
        
        # score lines
        for i in range(1, 11):
            line(self.img, WHITE, (0, i*scoremult), (self.w, i*scoremult), self.stroke_width//2)
        
        self.img = flip(self.img.copy(), False, True)

        minute_mark_interval = 11
        ticklines = 0
        while ticklines < 5:
            if minute_mark_interval > 1:
                minute_mark_interval -= 1
            else:
                minute_mark_interval /= 2
            ticklines = (self.w-50)/(minute_mark_interval*60*1000*tickmult)
        
        ticklines = int(ticklines) + 1
        for i in range(0, ticklines):
            tick = i*minute_mark_interval*60*1000
            xpos = tick*tickmult
            line(self.img, WHITE, (xpos, 0), (xpos, self.h-scoremult), self.stroke_width//2)
            if i == 0: # move first number a little to the right
                xpos += 20
            self.g.blit_centered(FONT_MD.render(str(i*minute_mark_interval), True, WHITE), (xpos, self.h-scoremult+20), self.img)
        # move last number a little to the left
        line(self.img, WHITE, (self.w-self.stroke_width//2, 0), (self.w-self.stroke_width//2, self.h-scoremult), self.stroke_width//2)
        self.g.blit_centered(FONT_MD.render(str(round(last_timestamp/1000/60, 1)), True, WHITE), (self.w-20, self.h-scoremult+20), self.img)
        
    
    def button_handler(self, name : str) -> None:
        if name == "Back":
            self.g.setstate(1)
            return
    
    def loop(self, events : list[Event]) -> None:
        self.g.blit_centered(self.img, (self.g.w//2, self.g.h//2+100))
        for b in self.buttons:
            b.draw()

    def keydown(self, k : int, kmods : int) -> bool:
        if k == K_q or k == K_ESCAPE:
            self.g.setstate(0)
            return True
        return False
        
    
    def click(self, pos : tuple, btn = int) -> bool:
        if btn == BUTTON_WHEELDOWN:
            for b in self.buttons:
                if not b.name == "Back":
                    b.pos = (b.pos[0], b.pos[1]-self.bh//3)
        
        elif btn == BUTTON_WHEELUP:
            for b in self.buttons:
                if not b.name == "Back":
                    b.pos = (b.pos[0], b.pos[1]+self.bh//3)
        
        elif btn == BUTTON_LEFT:
            for b in self.buttons:
                if b.click(pos):
                    return True
        return False
    
    #########################################################################################