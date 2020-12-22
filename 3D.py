import pygame
import math
pg = pygame
clock = pygame.time.Clock()
from pygame.math import Vector3 as Vec

pg.init()
width = 800
height = 600
screen = pg.display.set_mode((width, height))
pointlist = []
linelist = []
polylist = []

e = 200
sensitivity = .5
speed = 10

def clamp(x,minn,maxx):
  return min([max([x,minn]),maxx])

def project(pos,pitch,yaw,cam):
  global e
  x = pos[0]-cam.x
  y = pos[1]-cam.y
  z = pos[2]-cam.z
  d = Vec(x,y,z)
  d = d.rotate(-pitch, Vec(1,0,0).rotate(yaw, Vec(0,1,0)))
  d = d.rotate(-yaw, Vec(0,1,0))
  if d.z > 0.1:
    return (e/d.z*d.x+width/2,e/d.z*d.y+height/2)
  else: return 0

class Point:
  def __init__(self,pos):
    global pointlist
    self.pos = Vec(pos)
    pointlist += [self]
  def draw(self,pitch,yaw,cam,color):
    a = project(self.pos,pitch,yaw,cam)
    if a != 0 :pg.draw.circle(screen, color, (int(a[0]), int(a[1])), 10)

class Line:
  def __init__(self,pos1,pos2):
    global linelist
    self.pos1 = Vec(pos1)
    self.pos2 = Vec(pos2)
    linelist += [self]
  def draw(self,pitch,yaw,cam,color):
    a = project(self.pos1,pitch,yaw,cam)
    b = project(self.pos2,pitch,yaw,cam)
    if a != 0 and b != 0 :pg.draw.line(screen, color, (int(a[0]), int(a[1])), (int(b[0]), int(b[1])), 5)

class Poly:
  def __init__(self,points,thickness):
    global polylist
    self.points = points
    self.thick = thickness
    polylist += [self]
  def draw(self,pitch,yaw,cam,color):
    proj = []
    for point in self.points: proj += [project(point,pitch,yaw,cam)]
    if not(0 in proj): pg.draw.polygon(screen, color, proj, self.thick)

UP = pg.K_UP
DOWN = pg.K_DOWN
LEFT = pg.K_LEFT
RIGHT = pg.K_RIGHT
W = pg.K_w
S = pg.K_s
A = pg.K_a
D = pg.K_d
SP = pg.K_SPACE
SH = pg.K_LSHIFT
up = False
down = False
left = False
right = False
w = False
s = False
a = False
d = False
sp = False
sh = False

lockmouse = False
running = True

pitch = 0
yaw = 0
threeD = True

cam = Vec(0,0,-200)
camv = Vec(0,0,0)

p1 = Point((100,100,100))
p2 = Point((-100,100,100))
p3 = Point((100,-100,100))
p4 = Point((100,100,-100))
p5 = Point((-100,-100,100))
p6 = Point((100,-100,-100))
p7 = Point((-100,100,-100))
p8 = Point((-100,-100,-100))
l1 = Line((100,100,100),(100,-100,100))
l2 = Line((-100,100,100),(-100,-100,100))
l3 = Line((100,100,-100),(100,-100,-100))
l4 = Line((-100,100,-100),(-100,-100,-100))
l5 = Line((100,100,100),(-100,100,100))
l6 = Line((100,-100,100),(-100,-100,100))
l7 = Line((100,100,-100),(-100,100,-100))
l8 = Line((100,-100,-100),(-100,-100,-100))
l9 = Line((100,100,100),(100,100,-100))
l10 = Line((-100,100,100),(-100,100,-100))
l11 = Line((100,-100,100),(100,-100,-100))
l12 = Line((-100,-100,100),(-100,-100,-100))
pl1 = Poly([(-100,-100,-100),(100,-100,-100),(100,100,-100),(-100,100,-100)],0)


print("ready")
while running:

  screen.fill((0,0,0))

  for event in pygame.event.get():
    #print(event)
    if event.type == pg.QUIT:
      running = False
      pygame.display.quit()
      
    if event.type == pg.MOUSEMOTION:
      pitch -= event.rel[1] * sensitivity
      yaw += event.rel[0] * sensitivity
      pitch = clamp(pitch,-90,90)

    if event.type == pg.KEYDOWN:
      key = event.key
      if key == UP: up = True
      if key == DOWN: down = True
      if key == LEFT: left = True
      if key == RIGHT: right = True
      if key == W: w = True
      if key == S: s = True
      if key == A: a = True
      if key == D: d = True
      if key == SP: sp = True
      if key == SH: sh = True
      if key == pg.K_e: lockmouse = not(lockmouse)

    if event.type == pg.KEYUP:
      key = event.key
      if key == UP: up = False
      if key == DOWN: down = False
      if key == LEFT: left = False
      if key == RIGHT: right = False
      if key == pg.K_w: w = False
      if key == pg.K_s: s = False
      if key == pg.K_a: a = False
      if key == pg.K_d: d = False
      if key == SP: sp = False
      if key == SH: sh = False

  pygame.event.set_grab(lockmouse)
  pygame.mouse.set_visible(not(lockmouse))

  if pitch < 90: pitch += up
  if pitch > -90: pitch -= down
  yaw += right-left
  cam = cam + Vec((d-a)*speed,(sh-sp)*speed,(w-s)*speed).rotate(yaw, Vec(0,1,0))
  #cam += camv
  #if camv.length()>.5:
  #  camv = camv.scale_to_length(camv.length()*.9)
  #print([pitch,yaw],cam,camv)
  caml = cam+Vec(10,0,0).rotate(yaw, Vec(0,1,0))
  camr = cam+Vec(-10,0,0).rotate(yaw, Vec(0,1,0))
  for point in pointlist:
    if not(threeD):
      point.draw(pitch,yaw,cam,(255,255,255))
    else:
      point.draw(pitch,yaw,caml,(0,255,255))
      point.draw(pitch,yaw,camr,(255,0,0))
  for line in linelist:
    if not(threeD):
      line.draw(pitch,yaw,cam,(255,255,255))
    else:
      line.draw(pitch,yaw,caml,(0,255,255))
      line.draw(pitch,yaw,camr,(255,0,0))
  for poly in polylist:
    if not(threeD):
      poly.draw(pitch,yaw,cam,(200,200,200))
    else:
      poly.draw(pitch,yaw,caml,(0,200,200))
      poly.draw(pitch,yaw,camr,(200,0,0))
    
  pg.display.flip()

  clock.tick(30)
