import pygame

def clamp(n, a, b): 
    return max(a, min(n, b))


def Lerp(a:float, b:float, t:float):
    return (a*(1-t) + b*t)

def LerpColor(a:pygame.Color, b:pygame.Color, t:float):
    _r = Lerp(a.r, b.r, t)
    _g = Lerp(a.g, b.g, t)
    _b = Lerp(a.b, b.b, t)
    _a = Lerp(a.a, b.a, t)
    return pygame.Color(int(_r), int(_g), int(_b), int(_a))
