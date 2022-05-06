#pip install pandas
#pip install yfinance
#pip install yahoofinancials
#pip install pygame
#pip install python-binance


#Импорт библиотек
from pandas.core.series import Series

import threading
import pandas as pd
import numpy as np 

from datetime import datetime

import pygame

import app
import utils
import input
import graphics
import datamanager
import ai

import requests
import urllib.request
import csv
import json
from io import StringIO


from datetime import timedelta, datetime
from dateutil import parser

import os
import configparser



#print(df)

#fear and greed
#get_fng_index = "https://api.alternative.me/fng/"
#url = get_fng_index + "?limit=2000&format=csv&date_format=us"
#urllib.request.urlretrieve(url, 'data/btc_fng.csv')





def DownloadData():
	datamanager.get_all_binance('BTCUSDT', '15m', save = True)
	datamanager.get_all_binance('BTCUSDT', '30m', save = True)
	datamanager.get_all_binance('BTCUSDT', '1h', save = True)
	datamanager.get_all_binance('BTCUSDT', '1d', save = True)
	
	

def main():
	
	global width, height

	#data1h = pd.read_csv('data/BTCUSDT/BTCUSDT-1h-data.csv')
	df = pd.read_csv('data/BTCUSDT/BTCUSDT-1d-data.csv')
	#print(df)
	#Init Scenario
	
	

	window = graphics.Window()
	plot = graphics.Plot(df)
	button1 = graphics.Button()
	button1.rect = graphics.Rect(20,20,100,30)

	text1 = graphics.Text("Hello World")
	text1.rect = graphics.Rect(200,20,100,30)

	window.content.append(plot)
	#window.content.append(button1)

	graphics.objects.append(window)
	graphics.objects.append(button1)
	graphics.objects.append(text1)

	#d = df.iloc[-1]
	#print(d)
	#old = parser.parse(df["timestamp"].iloc[-1])
    #old = datetime.strptime('1 Jan 2017', '%d %b %Y')
	#v = pd.to_datetime(df['timestamp'], unit='ms')
	#print(old)

	#start = -1000
	#steps = 3
	#for x in range(0, steps):
	#	d = df.iloc[start+x]
	#	if(x == steps-1):
			
	#		print("prelast: "+str(d))
	#dl = d = df.iloc[start+steps]
	#print(dl)

	api_key_path = 'api_key.ini'

	#if not os.path.exists(api_key_path):
	#	f = open(api_key_path,"w")
	#	f.close()
		

	#READ API KEY BINANCE 
	config = configparser.ConfigParser()
	config.read(api_key_path)

	if config.has_option('DEFAULT', 'binance_api_key'):
		print(config['DEFAULT']['binance_api_key'])
	else:
		config['DEFAULT']['binance_api_key'] = '?'    # update
		config['DEFAULT']['binance_api_secret'] = '?'   # create
	
		with open(api_key_path, 'w') as configfile:    # save
			config.write(configfile)
	
	#SET API KEYS FOR DATA MANAGER
	datamanager.binance_api_key = config['DEFAULT']['binance_api_key']
	datamanager.binance_api_secret = config['DEFAULT']['binance_api_secret']

	#MAIN CYCLE
	while app.isRunning:
		screen.fill(graphics.backgroundColor)

		
		
		#t = pygame.time.get_ticks()
		# deltaTime in seconds.
		#deltaTime = (t - getTicksLastFrame) / 1000.0
		#getTicksLastFrame = t
		
		
		
		#INPUT
		mpos = pygame.mouse.get_pos()

		for event in pygame.event.get():
			if event.type == pygame.WINDOWRESIZED:
				print("Resized")
				w, h = pygame.display.get_surface().get_size()

			if event.type == pygame.QUIT:
				print("QUIT")
				app.isRunning = False
			elif event.type == pygame.KEYDOWN:
				keys = pygame.key.get_pressed()
				if event.key == pygame.K_r and keys[pygame.K_l]:
					print("Hi")
				elif event.key == pygame.K_l:
					print('bye')
				

			elif event.type == pygame.MOUSEWHEEL:
				print(event.x, event.y)
				if(window.isMouseOver()):
					window.showRect.w += -event.y*100
					window.showRect.h += -event.y*100
			elif event.type == pygame.MOUSEBUTTONUP:
				print("MouseUp")
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
				print("MouseDown")
			elif event.type == pygame.MOUSEMOTION:
				pass

		#input.Update()

		if(button1.isMouseOver()):
			
			pass

		pressed = pygame.key.get_pressed()
		if pressed[pygame.K_q]:
			window.showRect.w = np.clip(window.showRect.w+100, 1, 100000)
		if pressed[pygame.K_e]:
			window.showRect.w = np.clip(window.showRect.w-100, 1, 100000)
		if pressed[pygame.K_z]:
			window.showRect.h = np.clip(window.showRect.h-100, 1, 100000)
		if pressed[pygame.K_x]:
			window.showRect.h = np.clip(window.showRect.h+100, 1, 100000)

		if pressed[pygame.K_a]:
			window.showRect.x = window.showRect.x+100
		if pressed[pygame.K_d]:
			window.showRect.x = window.showRect.x-100
		if pressed[pygame.K_w]:
			window.showRect.y = window.showRect.y+100
		if pressed[pygame.K_s]:
			window.showRect.y = window.showRect.y-100

		


		if pressed[pygame.K_f]:
			DownloadData()

		#print(plot.rect.w)

		#screen.blit(font.render(str("bitcoin"), 1, pygame.Color("white")),(100, 100))
		#graphics.W = width
		#graphics.H = height
		#graphics.L = len(df.index)
		#for r in range(0, len(df.index)):
		#	d = df.iloc[r]
		#graphics.DrawCandle(screen,d["Open"], d["High"], d["Low"], d["Close"], r)


		#for r in df.index:
		#	d = df.loc[r]
		#	graphics.DrawCandle(screen,d["Open"], d["High"], d["Low"], d["Close"], d)

		#DRAW GRAPHICS
		for o in graphics.objects:
			o.Draw(screen)
		
		#window.Draw(screen)
	
		#
		clock.tick(60)
		pygame.display.flip()
		pass

#Init Program

#Init App	
pygame.init()
pygame.display.init()
pygame.display.set_caption('MA Terminal')
pygame.display.set_icon(graphics.icon)

width, height = 800, 600

screen = pygame.display.set_mode((width, height), flags=pygame.RESIZABLE)	#|pygame.NOFRAME
clock = pygame.time.Clock()

pygame.font.init()

main()

#DrawThread = threading.Thread(target=Update)
#DrawThread.start()
#DownloadDataThread = threading.Thread(target=DownloadData)
#DownloadDataThread.start()
#DrawThread.join() # Дождаться завершения вечного потока


	
	
































