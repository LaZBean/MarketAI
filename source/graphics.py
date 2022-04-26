from math import log10
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

  def __init__(self, _parent=None):
    super().__init__()
    parent = _parent
  
  def Draw(self, screen):
    #print("draw")
    pass



class Window(GraphicObject):

  dirty:bool = True
  focus:bool = False
  order:int = 0
  rect:pygame.Rect = pygame.Rect(100,100,400,400)

  showRect:pygame.Rect = pygame.Rect(0,0,10000,50000)
  content:GraphicObject = []

  selected:bool = False

  def __init__(self):
    super().__init__()

  def Draw(self, screen:pygame.Surface):
    
    self.rect = Rect(100, 100, screen.get_width()-200, screen.get_height()-200)
    surface = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
    surface.fill(windowBackgroundColor)

    mpos = pygame.mouse.get_pos()
    self.selected = self.rect.collidepoint(mpos)
    #if(self.selected):
      #print("selected")


    #Grid Scale
    scaleW = (self.rect.w/self.showRect.w)
    scaleH = (self.rect.h/self.showRect.h)

    #Draw Grid
    w = surface.get_width()
    h = surface.get_height()
    
    xl:int = 1000 #log10(self.showRect.w)
    yl:int = 1000
    
    

    for x in range(0, int(self.showRect.w / xl)):
      pygame.draw.line(surface, backgroundColor, ((x*xl+self.showRect.x)*scaleW, 0), ((x*xl+self.showRect.x)*scaleW, h))

    for y in range(0, int(self.showRect.h / yl)):
      pygame.draw.line(surface, backgroundColor, (0, (y*yl+self.showRect.y)*scaleH), (w, (y*yl+self.showRect.y)*scaleH))

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
    

  def Draw(self, screen:pygame.Surface, offset:pygame.Vector2, scale:pygame.Vector2):
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

  def Draw(self, screen:pygame.Surface, offset:pygame.Vector2, scale:pygame.Vector2):
    
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

    pygame.draw.line(screen, color, ((self.indx * 50+offset.x)*scale.x, screen.get_height() - (low-offset.y)*scale.y), ((self.indx * 50+offset.x)*scale.x, screen.get_height() - (high-offset.y)*scale.y) )

    
    