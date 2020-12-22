# Pygame-3D
A basic 3D pygame engine with points, lines, and polygons currently

Instructions:
  Open the file with python, and make sure you have pygame installed

Controlls:
  Mouse = Rotate Camera
  E = Lock Mouse
  WASD = Move horizontally
  Spacebar/Shift = Move Up and Down

Tweaking Instructions: 
  At line 15, you will see some variables being defined.
  e = Distance the projection plane is from the cameras pinhole (See https://en.wikipedia.org/wiki/3D_projection Perspective Projection)
  sensitivity = the modifier for the camera's rotation via mouse cursor. 1 = 1 degree per pixel of mouse movement.
  speed = how quickly the camera can move while one key is pressed
  
TODO:
  add Cube class
  add render sorting algorithm
  add colision
