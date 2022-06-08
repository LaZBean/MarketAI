
from distutils.log import debug
from email.errors import NonPrintableDefect
import utils
from math import log10
import string
from pandas.core import series
from pandas.core.frame import DataFrame
import pygame
import pygame.gfxdraw

import pandas as pd
import numpy as np 
import csv

from pygame.rect import Rect




#Colors
backgroundColor = (23, 27, 38, 255)
windowBackgroundColor = (43, 47, 58, 255)

candleRedColor = (239, 83, 80, 255)

candleGreenColor = (38, 166, 154, 255)

#Images
icon = pygame.image.load('res/icon.png')



orange = (255,152,0)
blue = (39,94,240)
green = (76,175,80)
red = (255, 82, 82)

W = 0
H = 0
L = 24

#def Load():
#=========================================================




class GraphicObject():

  parent:pygame.Surface = None
  rect:pygame.Rect = pygame.Rect(0,0,50,50)

  anchor_min:pygame.Vector2 = pygame.Vector2(0,1)
  anchor_max:pygame.Vector2 = pygame.Vector2(0,1)
  pivot:pygame.Vector2 = pygame.Vector2(0,0)

  def __init__(self, _parent=None):
    super().__init__()
    self.parent = _parent
    
  
  def Draw(self, screen, offset:pygame.Vector2=pygame.Vector2(0,0), scale:pygame.Vector2=pygame.Vector2(1,1)):
    pass

  def isMouseOver(self):
    mpos = pygame.mouse.get_pos()
    return bool(self.rect.collidepoint(mpos))



#OBJECTS
objects:GraphicObject = []


#TEXT
class Text(GraphicObject):

  def __init__(self, _text:string="", _parent=None):
    super().__init__()
    self.text = _text
    self.font_size = 16
    self.font = pygame.font.SysFont("Arial", self.font_size)
    self.color = (255,255,255,255)
    self.background_color = (76,175,80, 100)
    self.background_text_color = None
  
  def Draw(self, screen, offset:pygame.Vector2=pygame.Vector2(0,0), scale:pygame.Vector2=pygame.Vector2(1,1)):

    #self.rect = Rect(100, 100, screen.get_width()-200, screen.get_height()-300)

    surface = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
    surface.fill(self.background_color)
    screen.blit(surface, (self.rect.x, self.rect.y))

    text_surface = self.font.render(self.text, True, self.color, self.background_text_color)
    
    offs = pygame.Vector2(
      (self.rect.w/2 - text_surface.get_rect().w/2),
      (self.rect.h/2 - text_surface.get_rect().h/2))
    
    screen.blit(text_surface, (self.rect.x+offs.x, self.rect.y+offs.y))
    pass


#BUTTON
class Button(GraphicObject):
  
  #_color = None
  _pressed = False

  def __init__(self, _parent=None):
    super().__init__()
    self.color:pygame.Color = pygame.Color("#242B2E")
    self.color_hover:pygame.Color = pygame.Color("#758283") 
    self.color_active:pygame.Color = pygame.Color("#E07C24")

    self._color = self.color
    self.command = None

    
  
  def Draw(self, screen, offset:pygame.Vector2=pygame.Vector2(0,0), scale:pygame.Vector2=pygame.Vector2(1,1)):
    
    #self.rect = Rect(100, 100, screen.get_width()-200, screen.get_height()-300)

    #INPUT UPDATE
    c = self.color
    if(self.isMouseOver()):
      c = self.color_hover
      
      for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
          self._pressed = True
        if event.type == pygame.MOUSEBUTTONUP and event.button==1:
          self._pressed = False
          #CLICK
          if(self.command!=None):
            self.command()
    else:
      if(self._pressed):
        self._pressed = False

    if(self._pressed):
      c = self.color_active

    #DRAW
    self._color = utils.LerpColor(self._color, c, 0.2)

    surface = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
    surface.fill(self._color)

    screen.blit(surface, (self.rect.x, self.rect.y))
    pass

#WINDOW
class Window(GraphicObject):

  order:int = 0
  

  showRect:pygame.Rect = pygame.Rect(0,0,10000,10000)
  content:GraphicObject = []

  selected:bool = False

  def __init__(self):
    super().__init__()

  def Draw(self, screen:pygame.Surface, offset:pygame.Vector2=pygame.Vector2(0,0), scale:pygame.Vector2=pygame.Vector2(1,1)):
    #
    self.rect = Rect(100, 100, screen.get_width()-200, screen.get_height()-300)

    surface = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
    surface.fill(windowBackgroundColor)



    #Grid Scale
    scaleW = (self.rect.w/self.showRect.w)
    scaleH = (self.rect.h/self.showRect.h)

    #Draw Grid
    w = surface.get_width()
    h = surface.get_height()
    
    xl:int = 1000 #log10(self.showRect.w)
    yl:int = 1000
    
    

    for xx in range(0, int(self.showRect.w / xl)):
      a = ((xx*xl+self.showRect.x)*scaleW, 0)
      b = ((xx*xl+self.showRect.x)*scaleW, h)
      pygame.draw.line(surface, backgroundColor, a, b)

    for yy in range(0, int(self.showRect.h / yl)):
      a = (0, (self.showRect.h-yy*yl+self.showRect.y)*scaleH)
      b = (w, (self.showRect.h-yy*yl+self.showRect.y)*scaleH)
      pygame.draw.line(surface, backgroundColor, a, b)

    #Draw other window`s content
    for e in self.content:
      e.Draw(surface, pygame.Vector2(self.showRect.x, self.showRect.y), pygame.Vector2(scaleW, scaleH))

    screen.blit(surface, (self.rect.x, self.rect.y))



class Plot(GraphicObject):

  scale:pygame.Vector2 = pygame.Vector2(100,100)
  
  content:GraphicObject = []
  data:DataFrame = None

  def __init__(self, _data:DataFrame):
    super().__init__()
    self.data is _data

    for i in range(0, len(_data.index)):
      d = _data.iloc[i]
      cd = [d["open"], d["high"], d["low"], d["close"]]

      #for r in df.index:
		  #	d = df.loc[r]

      candle = Candle(i, cd)
      self.content.append(candle)
    

  def Draw(self, screen:pygame.Surface, offset:pygame.Vector2=pygame.Vector2(0,0), scale:pygame.Vector2=pygame.Vector2(1,1)):

    pygame.draw.rect(screen, candleGreenColor, pygame.Rect((300+offset.x)*scale.x, screen.get_height() - (200+500-offset.y)*scale.y, 500*scale.x, 500*scale.y))
    

    for e in self.content:
      
      e.Draw(screen, offset, scale)



class Candle(GraphicObject):
  
  data = [] #open, low, high, close
  
  indx = 0
  

  def __init__(self, i, _data):
    super().__init__()
    self.indx = i
    self.data = _data

  def Draw(self, screen:pygame.Surface, offset:pygame.Vector2=pygame.Vector2(0,0), scale:pygame.Vector2=pygame.Vector2(1,1)):
    
    w, h = screen.get_size()

    color = candleGreenColor
    if self.data[0] > self.data[3]:
      color = candleRedColor


    minVisible = 32000
    maxVisible = 48000
    dif = maxVisible - minVisible

    high = self.data[2]# - minVisible
    low = self.data[1]# - minVisible
    open = self.data[0]# - minVisible
    close = self.data[3]# - minVisible

  

    y1 = (h-(low/dif) * h)
    y2 = (h-(high/dif) * h)

    #pygame.draw.line(screen, color,(self.indx*2, y1),(self.indx*2, y2))
    x = ((self.indx * 50+offset.x)*scale.x, screen.get_height() - (low-offset.y)*scale.y)
    y = ((self.indx * 50+offset.x)*scale.x, screen.get_height() - (high-offset.y)*scale.y)
    pygame.draw.line(screen, color, x, y )


    
    ww = 30
    hh = abs(close-open)
    xx = (self.indx * 50+offset.x) - (ww/2)
    yy = (open-offset.y + hh)

    if open > close:
      yy = (close-offset.y + hh)
    

    pygame.draw.rect(screen, color, pygame.Rect(xx*scale.x, screen.get_height() - yy*scale.y, ww*scale.x, (hh)*scale.y))

    
    