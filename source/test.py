import pygame
import threading
import time
from pygame import color

isRunning = True
counter = 0
downloaded = False

clock = pygame.time.Clock()

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
pygame.display.init()
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
globalI = 0
#Качаем
def DownloadData():
	print("downloading...")
	global globalI
	for i in range(0, 1000000000):
		globalI = i # на самом деле тут ошибка паралельного программирования
		# Доступ к переменной из разных потоков, но для примера сойдет
	print("complete!")

#Рисуем
def Draw():
	global isRunning
	global globalI
	while isRunning:
		screen.fill((23, 27, 38))
		global counter
		global downloaded

		counter +=1
		print(f"running! {counter}")

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				print("QUIT")
				isRunning = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					threading.Thread(target=DownloadData).start()
		print("run continue")

		# Рендер текста
		textsurface = myfont.render(f"АААААА ЗАГРУЗКА!!! {globalI}", False, (255, 0, 0))
		screen.blit(textsurface, (10,10))
		clock.tick(60)
		pygame.display.flip()


Draw()