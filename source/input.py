import pygame

import app



def Update():


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
        elif event.type == pygame.MOUSEBUTTONUP:
            print("MouseUp")
    
    pass