#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This file is part of FullSave Gamejam.
Copyrights 2018 by Fullsave
"""

import os

import pyxel

SPRITESHEET_IMAGE = 0
SPRITESHEET_MASK = 7


class SpriteSheet(object):
    """ A singleton class that handles sprites
    """
    def __new__(cls):
        """ Singleton.
        """
        try:
            return cls._inst
        except AttributeError:
            cls._inst = super(SpriteSheet, cls).__new__(cls)
            cls._inst.initialized = False
            return cls._inst

    def __init__(self):
        """Initialise the instance.
        """
        if self.initialized:
            return

        assets = os.path.join(os.path.dirname(__file__), 'assets')
        pyxel.image(self.image).load(
                0, 0, os.path.join(assets, 'spritesheet.png'))

        self.initialized = True

    def __getitem__(self, key):
        try:
            return getattr(self, key)
        except AttributeError as exc:
            raise KeyError(exc.message)

    def __setitem__(self, key, value):
        try:
            setattr(self, key, value)
        except AttributeError as exc:
            raise KeyError(exc.message)

    def __delitem__(self, key):
        try:
            delattr(self, key)
        except AttributeError as exc:
            raise KeyError(exc.message)


class Sprite(object):
    def __init__(self, x, y, w, h):
        self._x = x
        self._y = y
        self._w = w
        self._h = h

    def render(self):
        return SPRITESHEET_IMAGE, self._x, self._y, \
                self._w, self._h, SPRITESHEET_MASK


class Hitbox(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    @property
    def x2(self):
        return self.x + self.w

    @property
    def y2(self):
        return self.y + self.h


class Item(object):
    def __init__(self, sprite):
        """Basic Game Element

        Arguments:
            * x, y, w, h: x, y, width, height
            * spritesheet: a SpriteSheet object
            * sx, sy: the coords, in multiple of w and h in the spritesheet
        """
        # Sprite sheet rendering
        self.sprite = sprite

    def copy(self):
        # Return a copy of this element to predict movements
        return Item(self.sprite)

    def draw(self, x, y):
        # Drawn the sprite at the element coords
        pyxel.blt(x, y, *self.sprite.render())


class Element(Item):
    def __init__(self, x, y, w, h, sprite):
        """Basic Game Element

        Arguments:
            * x, y, w, h: x, y, width, height
            * spritesheet: a SpriteSheet object
            * sx, sy: the coords, in multiple of w and h in the spritesheet
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        # The element hitbox
        self.hitbox = Hitbox(x, y, w, h)

        # Sprite sheet rendering
        Item.__init__(self, sprite)

    def draw(self):
        Item.draw(self, self.x, self.y)

    def copy(self):
        # Return a copy of this element to predict movements
        return Element(
                self.x, self.y, self.w, self.h,
                self.spritesheet, self.sx, self.sy
        )

    def is_colliding(self, element):
        # Is this element colliding with element
        return self.hitbox.x < element.hitbox.x2 and \
               self.hitbox.x2 > element.hitbox.x and \
               self.hitbox.y < element.hitbox.y2 and \
               self.hitbox.y2 > element.hitbox.y
