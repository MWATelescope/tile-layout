
import os

import visual
from visual import color
from visual import materials
from visual import Polygon as P
from visual import vector as V

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

eaxis = visual.arrow(pos=V(0, 0, 0), axis=V(2, 0, 0), color=color.blue, shaftwidth=0.1, fixedwidth=True, opacity=0.2)
naxis = visual.arrow(pos=V(0, 0, 0), axis=V(0, 2, 0), color=color.blue, shaftwidth=0.1, fixedwidth=True, opacity=0.2)

framenumber = 0
while True:
  os.system('screencapture.exe frames/aavs%05d.jpg VPython' % framenumber)
  visual.rate(1)