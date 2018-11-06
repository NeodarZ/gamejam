#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This file is part of FullSave Gamejam.
Copyrights 2018 by Fullsave
"""

import pyxel
import random
from pyxel.constants import FONT_WIDTH, FONT_HEIGHT
from .server import Server, RAM, CPU
from .rack import Rack


TXT_COLOR = 7
TXT_SPACE = 2
BORDER_COLOR = 12
ICO_BG_COLOR = 0
FULL_ORDER_COLOR = 2
EMPTY_ORDER_COLOR = 5


class Margin(object):

    def __init__(self, top, right, down, left):
        self.top = top
        self.right = right
        self.down = down
        self.left = left


class Order(object):

    def __init__(self, rack, n_ram, n_cpu):
        self._rack = rack
        self._server = Server(ram=n_ram, cpu=n_cpu)
        self._cpuitem = CPU()
        self._ramitem = RAM()

    def validate(self, rack, server):
        errors = self._server.compare(server)
        if rack is not self._rack:
            errors += 1
        if errors > 0:
            return 0
        # else:
        return server.value

    def draw(self, x, y):
        #BG
        pyxel.rect(x+2, y+2, x+61, y+19, 1)

        #rack no
        pyxel.rect(x+4, y+4, x+10, y+10, 10)
        pyxel.text(x+6, y+5, self._rack.number, 0)

        #server
        #pyxel.rect(x+19, y+5, x+30, y+16, ICO_BG_COLOR)
        self._server.draw(x+14, y+3)

        #cpu
        if self._server._cpu:
            #pyxel.rect(x+33, y+5, x+44, y+16, ICO_BG_COLOR)
            self._cpuitem.draw(x+31, y+3)
            pyxel.text(x+44, y+14, str(self._server._cpu), TXT_COLOR)

        #ram
        if self._server._ram:
            #pyxel.rect(x+47, y+5, x+58, y+16, ICO_BG_COLOR)
            self._ramitem.draw(x+46, y+3)
            pyxel.text(x+58, y+14, str(self._server._ram), TXT_COLOR)


class ScoreBoard(object):

    def __init__(self, map):
        random.seed()
        self._map = map
        self._margin = Margin(5, 5, 5, 5)
        self._orders = []

        for i in range(0, 3):
            self._orders.append(self.generate_order())

    def get_random_rack(self):
        racks = list(filter(lambda x: not x.is_full, self._map.racks))
        return random.choice(racks)

    def generate_order(self):
        return Order(
            rack=self.get_random_rack(),
            n_ram=random.randint(0, 2),
            n_cpu=random.randint(0, 2),
        )

    def validate_server(self, rack, server):
        for order in self._orders:
            value = order.validate(rack, server)

            if value:
                self._map.score += value
                self._orders.remove(order)
                self._orders.append(self.generate_order())
                break
        # else:
        # FIXME: racked a server for free, show a warning

    def get_pos(self):
        return (0, 0)

    def get_size(self):
        return (256, 24)

    def get_margin(self):
        return self._margin

    def get_score(self):
        return self._map.score

    def get_timer(self):
        return self._map.time

    def _draw_borders(self, x, y, w, h):
        pyxel.line(x, y+h-1, x+w, y+h-1, BORDER_COLOR)
        pyxel.line(x, y+h-2, x+w, y+h-2, BORDER_COLOR)

    def _draw_score(self, x, y):
        margin = self.get_margin()
        x += margin.left
        y += margin.top
        pyxel.text(x, y, "TIME: {:.1f}".format(self.get_timer()), TXT_COLOR)
        y += FONT_HEIGHT + TXT_SPACE
        pyxel.text(x, y, "SCORE: {:d}".format(self.get_score()), TXT_COLOR)

    def _draw_order(self, x, y, order=None):
        if order:
            order.draw(x, y)
        else:
            pyxel.rectb(x+2, y+2, x+61, y+19, EMPTY_ORDER_COLOR)

    def _draw_orders(self, x, y):
        for i in range(0, 3):
            if len(self._orders) > i:
                order = self._orders[i]
            else:
                order = None
            self._draw_order(i*64+x, y, order)

    def draw(self):
        (x, y) = self.get_pos()
        (w, h) = self.get_size()
        self._draw_borders(x, y, w, h)
        self._draw_score(x, y)
        self._draw_orders(x+64, y)
