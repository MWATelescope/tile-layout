
import visual
from visual import color
from visual import Polygon as P

# Base object
square = P([(-0.5, -0.475), (-0.5, 0.475), (0.5, 0.475), (0.5, -0.475)])
circle = visual.shapes.circle(pos=(0.0,0.0), radius=0.525)
cutout = P([(-0.315, 0.24), (-0.24, 0.315), (0.24, 0.315), (0.315, 0.24),
            (0.315, -0.24), (0.24, -0.315), (-0.24, -0.315), (-0.315, -0.24)])
straight = [(0.0, 0.0, 0.0), (0.0, 0.0, 0.065)]  # Shape will be created at (0,0,0) with this path

basep = (square & circle) - cutout

# A single pole, with loops:
A = (0, 0.38, 0)
A1 = (-0.29, 1.22, 0)
B = (0, 0.59, 0)
B1 = (-0.29, 1.31, 0)
C = (0, 0.74, 0)
C1 = (0.23, 1.38, 0)
D = (0, 0.89, 0)
D1 = (0.23, 1.45, 0)
E = (0, 1.02, 0)
E1 = (-0.17, 1.5, 0)
F = (0, 1.13, 0)
F1 = (-0.17, 1.55, 0)
G = (0, 1.22, 0)
G1 = (0.14, 1.59, 0)
H = (0, 1.31, 0)
H1 = (0.14, 1.63, 0)
I = (0, 1.38, 0)
I1 = (-0.1, 1.66, 0)
J = (0, 1.45, 0)
J1 = (-0.1, 1.69, 0)
K = (0, 1.5, 0)
K1 = (0.07, 1.71, 0)
L = (0, 1.55, 0)
L1 = (0.07, 1.73, 0)
M = (0, 1.59, 0)
N = (0, 1.63, 0)
O = (0, 1.66, 0)
P = (0, 1.69, 0)
Q = (0, 1.71, 0)
R = (0, 1.73, 0)
S = (0.6, 0.09, 0)
T = (0.6, 0.59, 0)
U = (-0.5, 0.74, 0)
V = (-0.5, 0.89, 0)
W = (0.37, 1.02, 0)
Z = (0.37, 1.13, 0)

def getelement(frame=None, which='E'):
  element = visual.frame(frame=frame, axis=(1,0,0))
  pole = visual.curve(frame=element, pos=[(0,0,0), R], radius=0.02)
  d1 = visual.curve(frame=element, pos=[A, S, T, B], radius=0.01)
  d3 = visual.curve(frame=element, pos=[E, W, Z, F], radius=0.01)
  d5 = visual.curve(frame=element, pos=[I, C1, D1, J], radius=0.01)
  d7 = visual.curve(frame=element, pos=[M, G1, H1, N], radius=0.01)
  d9 = visual.curve(frame=element, pos=[Q, K1, L1, R], radius=0.01)

  d2 = visual.curve(frame=element, pos=[C, U, V, D], radius=0.01)
  d4 = visual.curve(frame=element, pos=[G, A1, B1, H], radius=0.01)
  d6 = visual.curve(frame=element, pos=[K, E1, F1, L], radius=0.01)
  d8 = visual.curve(frame=element, pos=[O, I1, J1, P], radius=0.01)

  element.rotate(angle=visual.pi/2, axis=(1,0,0), pos=(0,0,0))

  if which == 'E':
    element.pos = (0, -0.354, 0)
    element.rotate(angle=-0.20184, axis=(1,0,0), pos=element.pos)
  elif which == 'W':
    element.rotate(angle=visual.pi, axis=(0,0,1))
    element.pos = (0, 0.354, 0)
    element.rotate(angle=0.20184, axis=(1,0,0), pos=element.pos)
  elif which == 'N':
    element.rotate(angle=-visual.pi/2, axis=(0,0,1))
    element.pos = (-0.354, 0, 0)
    element.rotate(angle=0.20184, axis=(0,1,0), pos=element.pos)
  elif which == 'S':
    element.rotate(angle=visual.pi/2, axis=(0,0,1))
    element.pos = (0.354, 0, 0)
    element.rotate(angle=-0.20184, axis=(0,1,0), pos=element.pos)
  return element, [pole, d1, d2, d3, d4, d5, d6, d7, d8, d9]


def getxmas():
  xmas = visual.frame()
  elements = []
  for direction in ['E', 'W', 'N', 'S']:
    ef, olist = getelement(frame=xmas, which=direction)
    elements.append(ef)
    elements.append(olist)
  return xmas, elements

apiu = visual.box(pos=(0,0,0.980/2), length=0.850, height=1.250, width=0.980, color=color.red)
posfile = open('aavspositions.txt', 'r')
lines = posfile.readlines()
bases = []
for line in lines:
  x, y = tuple(map(float, line.split()))
  b = visual.extrusion(pos=[(x, y, 0.0), (x, y, 0.065)], shape=basep, color=color.gray(0.5))
  bases.append(b)
  tree, elist = getxmas()
  tree.pos = (x, y, 0.065)

eaxis = visual.arrow(pos=(0, 0, 0), axis=(2, 0, 0), color=color.blue, shaftwidth=0.1, fixedwidth=True, opacity=0.2)
naxis = visual.arrow(pos=(0, 0, 0), axis=(0, 2, 0), color=color.blue, shaftwidth=0.1, fixedwidth=True, opacity=0.2)

while True:
  visual.rate(20)