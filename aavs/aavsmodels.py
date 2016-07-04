
from PIL import ImageGrab

import visual
from visual import color
from visual import materials
from visual import Polygon as P
from visual import vector as V

scene = visual.display(x=0, y=0, width=1024, height=768)
scene.autoscale = False
scene.forward = (0, 1, -1)
scene.up = (0, 0, 1)
scene.range = 25

MOVIE = False   # Do we capture frames to disk?

# Base object
square = P([(-0.5, -0.475), (-0.5, 0.475), (0.5, 0.475), (0.5, -0.475)])
circle = visual.shapes.circle(pos=(0.0,0.0), radius=0.525)
cutout = P([(-0.315, 0.24), (-0.24, 0.315), (0.24, 0.315), (0.315, 0.24),
            (0.315, -0.24), (0.24, -0.315), (-0.24, -0.315), (-0.315, -0.24)])
straight = [(0.0, 0.0, 0.0), (0.0, 0.0, 0.065)]  # Shape will be created at (0,0,0) with this path

basep = (square & circle) - cutout

WIRER = 0.0025   # Radius of dipole loop wires
PIPER = 0.01     # Radius of dipole diagonal poles
POLER = 0.015    # Radius of central vertical conduit

WIREMAT = None
PIPEMAT = None
POLEMAT = materials.plastic
GMAT = materials.texture(data=materials.loadTGA('mro.tga'))

GCOLOR = V(0.95, 0.59, 0.42)


# A single pole, with loops:
A = V(0, 0.38, 0)
A1 = V(-0.29, 1.22, 0)
B = V(0, 0.59, 0)
B1 = V(-0.29, 1.31, 0)
C = V(0, 0.74, 0)
C1 = V(0.23, 1.38, 0)
D = V(0, 0.89, 0)
D1 = V(0.23, 1.45, 0)
E = V(0, 1.02, 0)
E1 = V(-0.17, 1.5, 0)
F = V(0, 1.13, 0)
F1 = V(-0.17, 1.55, 0)
G = V(0, 1.22, 0)
G1 = V(0.14, 1.59, 0)
H = V(0, 1.31, 0)
H1 = V(0.14, 1.63, 0)
I = V(0, 1.38, 0)
I1 = V(-0.1, 1.66, 0)
J = V(0, 1.45, 0)
J1 = V(-0.1, 1.69, 0)
K = V(0, 1.5, 0)
K1 = V(0.07, 1.71, 0)
L = V(0, 1.55, 0)
L1 = V(0.07, 1.73, 0)
M = V(0, 1.59, 0)
N = V(0, 1.63, 0)
O = V(0, 1.66, 0)
P = V(0, 1.69, 0)
Q = V(0, 1.71, 0)
R = V(0, 1.73, 0)
S = V(0.6, 0.09, 0)
T = V(0.6, 0.59, 0)
U = V(-0.5, 0.74, 0)
Vp = V(-0.5, 0.89, 0)
W = V(0.37, 1.02, 0)
Z = V(0.37, 1.13, 0)

def getelement(frame=None, which='E'):
  element = visual.frame(frame=frame, axis=V(1,0,0))
  pipe = visual.curve(frame=element, pos=[V(0,0,0), R], radius=PIPER, material=PIPEMAT, color=color.gray(0.7))
  d1 = visual.curve(frame=element, pos=[A, S, T, B], radius=WIRER, material=WIREMAT, color=color.gray(0.7))
  d3 = visual.curve(frame=element, pos=[E, W, Z, F], radius=WIRER, material=WIREMAT, color=color.gray(0.7))
  d5 = visual.curve(frame=element, pos=[I, C1, D1, J], radius=WIRER, material=WIREMAT, color=color.gray(0.7))
  d7 = visual.curve(frame=element, pos=[M, G1, H1, N], radius=WIRER, material=WIREMAT, color=color.gray(0.7))
  d9 = visual.curve(frame=element, pos=[Q, K1, L1, R], radius=WIRER, material=WIREMAT, color=color.gray(0.7))

  d2 = visual.curve(frame=element, pos=[C, U, Vp, D], radius=WIRER, material=WIREMAT, color=color.gray(0.7))
  d4 = visual.curve(frame=element, pos=[G, A1, B1, H], radius=WIRER, material=WIREMAT, color=color.gray(0.7))
  d6 = visual.curve(frame=element, pos=[K, E1, F1, L], radius=WIRER, material=WIREMAT, color=color.gray(0.7))
  d8 = visual.curve(frame=element, pos=[O, I1, J1, P], radius=WIRER, material=WIREMAT, color=color.gray(0.7))

  element.rotate(angle=visual.pi/2, axis=V(1,0,0), pos=V(0,0,0))

  if which == 'E':
    element.pos = V(0, -0.354, 0)
    element.rotate(angle=-0.20184, axis=V(1,0,0), pos=element.pos)
  elif which == 'W':
    element.rotate(angle=visual.pi, axis=V(0,0,1))
    element.pos = V(0, 0.354, 0)
    element.rotate(angle=0.20184, axis=V(1,0,0), pos=element.pos)
  elif which == 'N':
    element.rotate(angle=-visual.pi/2, axis=V(0,0,1))
    element.pos = V(-0.354, 0, 0)
    element.rotate(angle=0.20184, axis=V(0,1,0), pos=element.pos)
  elif which == 'S':
    element.rotate(angle=visual.pi/2, axis=V(0,0,1))
    element.pos = V(0.354, 0, 0)
    element.rotate(angle=-0.20184, axis=V(0,1,0), pos=element.pos)
  return element, [pipe, d1, d2, d3, d4, d5, d6, d7, d8, d9]


def getxmas():
  xmas = visual.frame()
  elements = []
  for direction in ['E', 'W', 'N', 'S']:
    ef, olist = getelement(frame=xmas, which=direction)
    elements.append(ef)
    elements.append(olist)
  s1 = visual.curve(pos=[V(-0.233,-0.233,0.59), V(0.233,-0.233,0.59), V(0.233,0.233,0.59),
                         V(-0.233,0.233,0.59), V(-0.233,-0.233,0.59)],
                    frame=xmas,
                    radius=0.02,
                    material=materials.plastic,
                    color=color.white)
  s2 = visual.curve(pos=[V(-0.233,0,0.59), V(0.233,0,0.59)],
                    frame=xmas,
                    radius=0.02,
                    material=materials.plastic,
                    color=color.white)
  s3 = visual.curve(pos=[V(0, -0.233, 0.59), V(0, 0.233, 0.59)],
                    frame=xmas,
                    radius=0.02,
                    material=materials.plastic,
                    color=color.white)
  lna = visual.box(pos=V(0, 0, 1.63),
                   frame=xmas,
                   height=0.03, length=0.03, width=0.08,
                   material=materials.plastic,
                   color=color.white)
  pole = visual.curve(pos=[V(0, 0, 0.38), V(0,0,1.73)], frame=xmas, radius=POLER, material=POLEMAT, color=color.white)
  elements.append([s1, s2, s3, lna, pole])
  return xmas, elements


def getbundle(spos=None):   # spos is  position that cable centre exits the box
  blist = []
  cframe = visual.frame()
  startz = spos.z   # Height above ground that cable centre exits the APIU box
  carc1 = visual.paths.arc(radius=startz / 2, angle1=visual.pi, angle2=visual.pi/2, up=(0,-1,0))
  carc1.pos = [p + spos + V(0, 0, -startz / 2) for p in carc1.pos]
  c1 = visual.curve(frame=cframe, pos=carc1, radius=0.08 / 2, color=color.blue)
  carc2 = visual.paths.arc(radius=startz / 2, angle1=visual.pi, angle2=visual.pi/2, up=(0,1,0))
  carc2.pos = [p + spos + V(startz, 0, -startz / 2) for p in carc2.pos]
  c2 = visual.curve(frame=cframe, pos=carc2, radius=0.08 / 2, color=color.blue)
  c2.append(pos=spos + V(1.5, 0, -startz), color=GCOLOR)
  blist.append(c1)
  return cframe, blist


def getapiu():
  box = visual.box(pos=V(0, 0, 0.800/2 + 0.12), length=0.800, height=1.050, width=0.800, color=color.white)
  hat = visual.pyramid(pos=V(0, 0, 0.800 + 0.12), size=V(0.06, 1.050, 0.800), axis=V(0,0,1), color=color.white)
  rv1 = visual.box(pos=V(-0.3, 0, 0.055), length=0.01, height=1.250, width=0.10, color=color.white)
  rt1 = visual.box(pos=V(-0.3, 0, 0.115), length=0.10, height=1.250, width=0.01, color=color.white)
  rb1 = visual.box(pos=V(-0.3, 0, 0.005), length=0.10, height=1.250, width=0.01, color=color.white)
  rv2 = visual.box(pos=V(0.3, 0, 0.055), length=0.01, height=1.250, width=0.10, color=color.white)
  rt2 = visual.box(pos=V(0.3, 0, 0.115), length=0.10, height=1.250, width=0.01, color=color.white)
  rb2 = visual.box(pos=V(0.3, 0, 0.005), length=0.10, height=1.250, width=0.01, color=color.white)
  sss = visual.box(pos=V(0, -1.050 / 2 - 0.030, 0.800 / 2 + 0.12), length=0.800, height=0.003, width=0.800, color=color.white)
  ssn = visual.box(pos=V(0, 1.050 / 2 + 0.030, 0.800 / 2 + 0.12), length=0.800, height=0.003, width=0.800, color=color.white)
  sse = visual.box(pos=V(-0.800 / 2 - 0.030, 0, 0.600 / 2 + 0.12), length=0.003, height=1.050, width=0.600, color=color.white)
  ssw = visual.box(pos=V(0.800 / 2 + 0.030, 0, 0.600 / 2 + 0.12), length=0.003, height=1.050, width=0.600, color=color.white)
  cbylist = [-0.2775, -0.1255, 0.1255, 0.2775]
  cblist = []
  for cy in cbylist:
    cblist.append(visual.cylinder(pos=V(-0.800/2, cy, 0.700 + 0.120), axis=(-0.100, 0, 0), radius=0.01))
    cblist.append(visual.helix(pos=V(-0.800 / 2 - 0.150, cy, 0.700 + 0.120 - 0.05),
                               axis=(0.05, 0, 0),
                               radius=0.050,
                               thickness=0.01,
                               coils=1,
                               up=(0,1,0),
                               color=color.white))
    cb, tlist = getbundle(spos=V(-0.800 / 2, cy, 0.700 + 0.120 - 0.05))
    cblist += tlist
    cb.rotate(angle=visual.pi, axis=(0,0,1), origin=V(-0.800 / 2, cy, 0.700 + 0.120 - 0.05))
  for cy in cbylist:
    cblist.append(visual.cylinder(pos=V(0.800 / 2, cy, 0.700 + 0.120), axis=(0.100, 0, 0), radius=0.01))
    cblist.append(visual.helix(pos=V(0.800 / 2 + 0.10, cy, 0.700 + 0.120 - 0.05),
                               axis=(0.05, 0, 0),
                               radius=0.050,
                               thickness=0.01,
                               coils=1,
                               up=(0, 1, 0),
                               color=color.white))
    cb, tlist = getbundle(spos=V(0.800 / 2, cy, 0.700 + 0.120 - 0.05))
    cblist += tlist


def gettreecable(treepos=V(0,0,0)):
  cframe = visual.frame()
  cstartpos = treepos + (0, 0, 0.4)    # Where the cable leaves the xmas tree trunk
  theta = visual.atan2(treepos.y, treepos.x)

  carc = visual.paths.arc(radius=0.37, angle1=-visual.pi/2, angle2=0, up=(0,-1,0))
  carc.pos = [p + treepos + V(0.37, 0, 0.4) for p in carc.pos[::-1]]

  c1 = visual.curve(frame=cframe, pos=carc, radius=0.0129 / 2, color=color.blue)
  c1.append(pos=treepos + V(1.5, 0, -0.065), color=GCOLOR)
  cframe.rotate(angle=theta + visual.pi, axis=(0, 0, 1), origin=cstartpos)


recording = False
playing = False
framenumber = 0
capnumber = 1
viewlist = []


def processClick(event):
  global framenumber, capnumber, recording, playing, scene, viewlist
  try:      # Key pressed:
    s = event.key
  except AttributeError:
    s = None

  if s is not None:
    if s == 'c':
      visual.sleep(0.05)
      im = ImageGrab.grab((10,40, 1260,924))
      im.save('frames/aavs%05d.png' % capnumber)
      capnumber += 1
    elif s == 'r':
      viewlist = []
      recording = True
      framenumber = 0
      playing = False
      print "Recording views"
    elif s == 's':
      recording = False
      playing = False
      framenumber = 0
      print "Stopped, we have %d frames of viewpoints recorded" % len(viewlist)
      print viewlist
    elif s == 'p':
      recording = False
      if playing:
        playing = False
        print "Playing paused at frame number %d of %d" % (framenumber, len(viewlist))
      else:
        playing = True
        print "Playing started at frame number %d of %d" % (framenumber, len(viewlist))
    elif s == 'left':
      f = visual.rotate(vector=scene.forward, angle=visual.pi / 180, axis=V(0, 0, 1))
      scene.forward = f
    elif s == 'right':
      f = visual.rotate(vector=scene.forward, angle=-visual.pi / 180, axis=V(0, 0, 1))
      scene.forward = f
    else:
      print "Key pressed: '%s'" % s
  else:             # Mouse clicked:
    clickedpos = event.pickpos   # The 3D position on the surface of the object clicked on
    if clickedpos:
      scene.center = clickedpos  # Change the camera centre position


scene.bind('click keydown', processClick)

apiu = getapiu()

ground = visual.cylinder(pos=V(0,0,-0.2), radius=20.0, axis=V(0,0,0.2),
                         material=GMAT)
#                         color=(0.95, 0.59, 0.42))

posfile = open('aavspositions.txt', 'r')
lines = posfile.readlines()
bases = []
for line in lines:
  x, y = tuple(map(float, line.split()))
  b = visual.extrusion(pos=[V(x, y, 0.0), V(x, y, 0.065)], shape=basep, material=materials.rough, color=color.gray(0.4))
  bases.append(b)
  tree, elist = getxmas()
  tree.pos = (x, y, 0.065)
  cable = gettreecable(tree.pos)

eaxis = visual.arrow(pos=V(0, 0, 0), axis=V(2, 0, 0), color=color.blue, shaftwidth=0.1, fixedwidth=True, opacity=0.2)
naxis = visual.arrow(pos=V(0, 0, 0), axis=V(0, 2, 0), color=color.blue, shaftwidth=0.1, fixedwidth=True, opacity=0.2)


framenumber = 0
while True:
  if recording:
    viewlist.append(scene.forward.astuple())

  if playing:
    if framenumber < len(viewlist):
      f = viewlist[framenumber]
      scene.forward = f
      print framenumber, f, scene.forward

    if MOVIE:
      visual.sleep(0.1)
      im = ImageGrab.grab((10, 40, 1260, 924))
      im.save('frames/aavs%05d.png' % framenumber)

    framenumber += 1

  if not (MOVIE and playing):
    visual.rate(10)