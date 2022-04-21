from __future__ import annotations
from datetime import timedelta

from pygame.locals import *
from pygame.event import Event
from pygame.draw import line

from .constants import *
from .components.button import Button

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .munchkin import Munchkin

class Game:
    """
    Level board screen
    """
    def __init__(self, game : Munchkin) -> None:
        self.g = game
        self.window = self.g.window
    
    #########################################################################################

    def setup(self) -> None:
        self.aa = True

        if self.g.pcount == 0:
            self.g.setstate(0)
            return
        
        self.segwidth = self.g.w / self.g.pcount
        self.buttons = [
            Button(self.g, "Back", (100, 50), (200, 100), self.button_handler, FONT_LG),
            Button(self.g, "Stats", (300, 50), (200, 100), self.button_handler, FONT_LG)
        ]
    
    def button_handler(self, name : str) -> None:
        if name == "Back":
            self.g.setstate(0)
        elif name == "Stats":
            self.g.setstate(3)
            return

    def loop(self, events : list[Event]) -> None:
        for b in self.buttons:
            b.draw()
        for p in self.g.players:
            lpos = self.g.w//self.g.pcount*p["num"]
            tpos = lpos - self.segwidth//2

            color = WHITE
            
            if self.g.players_by_score[0]["score"] == p["score"]:
                color = GREEN
            elif self.g.players_by_score[-1]["score"] == p["score"]:
                color = RED
        
            # lines
            if p["num"] < self.g.pcount:
                line(self.window, WHITE, (lpos, 0), (lpos, self.g.h), 5)
            
            # name, +, - and score
            self.g.blit_centered(FONT_LG.render(p["name"], self.aa, self.g.player_colors[p["num"]]), (tpos, self.g.h//2 - self.g.h//6))
            self.g.blit_centered(FONT_XL.render("+", self.aa, color), (tpos, self.g.h//2 - self.g.h//3))
            self.g.blit_centered(FONT_XL.render("-", self.aa, color), (tpos, self.g.h//2 + self.g.h//3))
            self.g.blit_centered(FONT_XL.render(str(p["score"]), self.aa, color), (tpos, self.g.h//2))
        
        # game timer
        game_time = FONT_MD.render(str(timedelta(seconds=self.g.get_game_time()//1000)), self.aa, WHITE)
        self.window.blit(game_time, (self.g.w - game_time.get_size()[0] - 5, 5))
    
    def keydown(self, k : int, kmods : int) -> bool:
        if k > K_0 and k <= K_9:
            idx = k - K_1
            if idx < len(self.g.players):
                p = self.g.players[idx]
                
                _mod = 1
                if kmods & KMOD_SHIFT:
                    _mod = -1
                
                self.update_score(p, _mod)
                return True

        elif k == K_q or k == K_ESCAPE:
            self.g.setstate(0)
            return True
        
        return False
    
    def click(self, pos : tuple, btn = int) -> bool:
        (x, y) = pos
        if btn == BUTTON_LEFT:
            # catch button clicks
            for b in self.buttons:
                if b.click(pos):
                    return True
            # modify player level
            _mod = 1
            if y > self.g.h//2:
                _mod = -1
            
            p = self.get_player_clicked(x)
            self.update_score(p, _mod)
            return True
    
    #########################################################################################
    
    def get_player_clicked(self, x) -> dict:
        for p in self.g.players:
            lpos = self.g.w//self.g.pcount*p["num"]
            if x > lpos - self.segwidth and x < lpos:
                return p
        return None
    
    def update_score(self, p : dict, _mod : int) -> None:
        if p is None:
            return

        new_score = p["score"] + _mod
        if new_score >= 1 and new_score <= 10:
            p["score"] = new_score
            self.g.playerdata_changed(p)