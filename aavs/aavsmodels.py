
import visual
from visual import color
from visual import materials
from visual import Polygon as P
from visual import vector as V

# Constants defining dipole wire/pole/pipe thickness, materials, and colours
WIRER = 0.0025   # Radius of dipole loop wires
PIPER = 0.01     # Radius of dipole diagonal poles
POLER = 0.015    # Radius of central vertical conduit

WIREMAT = None
PIPEMAT = None
POLEMAT = None

SPACERMAT = None    # Material for the white plastic spacer in the dipole tree

# Cover ground with an photo of the MRO, and define a matching color
GMAT = materials.texture(data=materials.loadTGA('mro.tga'))
GCOLOR = V(0.95, 0.59, 0.42)

# Define the window size and initial camera orientation
scene = visual.display(x=0, y=0, width=1024, height=768)
scene.forward = (0, 1, -1)
scene.up = (0, 0, 1)
scene.range = 25

# Concrete base object shape definitions
square = P([(-0.5, -0.475), (-0.5, 0.475), (0.5, 0.475), (0.5, -0.475)])
circle = visual.shapes.circle(pos=(0.0,0.0), radius=0.525)
cutout = P([(-0.315, 0.24), (-0.24, 0.315), (0.24, 0.315), (0.315, 0.24),
            (0.315, -0.24), (0.24, -0.315), (-0.24, -0.315), (-0.315, -0.24)])
straight = [(0.0, 0.0, 0.0), (0.0, 0.0, 0.065)]  # Shape will be created at (0,0,0) with this path

# The 2D shape of the concrete base (viewed from above) is the intersection between a square and a circle,
# minus the octagonal cutout in the middle
basep = (square & circle) - cutout

# Points definining the dipoles - these points represent a single pole, with loops.
# Four of these, rotated in the cardinal directions, and angled in towards the centre at
# the top, define a 'Christmas Tree'.
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
  """This returns a single dipole arm, positioned at (0,0,0). It is returned in the 'frame'
     object provided. The value of 'which' (either 'N', 'S', 'E', or 'W') determines
     the orientation and position of the dipole returned.

     Call this function four times, for each of N,S,E, and W with the same frame
     object to build up a complete Christmas Tree.

     A tuple of (element, olist) is returned, where element is the frame containing the dipole arm,
     and olist is a list containing all the component objects in the element.
  """
  element = visual.frame(frame=frame, axis=V(1,0,0))  # Create a sub-frame for this dipole arm
  # The pipe object is the 'vertical' from base to top centre
  pipe = visual.curve(frame=element, pos=[V(0,0,0), R], radius=PIPER, material=PIPEMAT, color=color.gray(0.7))

  # These define the nine dipole loops, odd numbers on one side and even on the other.
  d1 = visual.curve(frame=element, pos=[A, S, T, B], radius=WIRER, material=WIREMAT, color=color.gray(0.7))
  d3 = visual.curve(frame=element, pos=[E, W, Z, F], radius=WIRER, material=WIREMAT, color=color.gray(0.7))
  d5 = visual.curve(frame=element, pos=[I, C1, D1, J], radius=WIRER, material=WIREMAT, color=color.gray(0.7))
  d7 = visual.curve(frame=element, pos=[M, G1, H1, N], radius=WIRER, material=WIREMAT, color=color.gray(0.7))
  d9 = visual.curve(frame=element, pos=[Q, K1, L1, R], radius=WIRER, material=WIREMAT, color=color.gray(0.7))

  d2 = visual.curve(frame=element, pos=[C, U, Vp, D], radius=WIRER, material=WIREMAT, color=color.gray(0.7))
  d4 = visual.curve(frame=element, pos=[G, A1, B1, H], radius=WIRER, material=WIREMAT, color=color.gray(0.7))
  d6 = visual.curve(frame=element, pos=[K, E1, F1, L], radius=WIRER, material=WIREMAT, color=color.gray(0.7))
  d8 = visual.curve(frame=element, pos=[O, I1, J1, P], radius=WIRER, material=WIREMAT, color=color.gray(0.7))

  # Rotate the dipole arm so it's vertical (parallel to Z axis), instead of in the XY plane.
  element.rotate(angle=visual.pi/2, axis=V(1,0,0), pos=V(0,0,0))

  if which == 'E':
    element.pos = V(0, -0.354, 0)   # Shift it so it's above the East mounting point
    element.rotate(angle=-0.20184, axis=V(1,0,0), pos=element.pos)  # Rotate it so the top is above (0,0,0)
  elif which == 'W':
    element.rotate(angle=visual.pi, axis=V(0,0,1))  # Rotate it vertically so the dipoles face in the right direction
    element.pos = V(0, 0.354, 0)   # Shift it so it's above the West mounting point
    element.rotate(angle=0.20184, axis=V(1,0,0), pos=element.pos)  # Rotate it so the top is above (0,0,0)
  elif which == 'S':
    element.rotate(angle=-visual.pi/2, axis=V(0,0,1))  # Rotate it vertically so the dipoles face in the right direction
    element.pos = V(-0.354, 0, 0)   # Shift it so it's above the South mounting point
    element.rotate(angle=0.20184, axis=V(0,1,0), pos=element.pos)  # Rotate it so the top is above (0,0,0)
  elif which == 'N':
    element.rotate(angle=visual.pi/2, axis=V(0,0,1))  # Rotate it vertically so the dipoles face in the right direction
    element.pos = V(0.354, 0, 0)   # Shift it so it's above the North mounting point
    element.rotate(angle=-0.20184, axis=V(0,1,0), pos=element.pos)  # Rotate it so the top is above (0,0,0)
  return element, [pipe, d1, d2, d3, d4, d5, d6, d7, d8, d9]


def getxmas():
  """Creates a complete Christmas Tree dipole assembly (minus base) at (0,0,0)

     Returned value is a tuple of (xmas, olist), where xmas is the frame containing the
     complete Christmas Tree dipoles, and olist is a list of all of the component objects."""
  xmas = visual.frame()
  olist = []
  for direction in ['E', 'W', 'N', 'S']:  # Create the four dipole arms
    ef, elist = getelement(frame=xmas, which=direction)
    olist.append(ef)
    olist.append(elist)

  # These objects (s1-s3) are the white plastic space assembly
  s1 = visual.curve(pos=[V(-0.233,-0.233,0.59), V(0.233,-0.233,0.59), V(0.233,0.233,0.59),
                         V(-0.233,0.233,0.59), V(-0.233,-0.233,0.59)],
                    frame=xmas,
                    radius=0.02,
                    material=SPACERMAT,
                    color=color.white)
  s2 = visual.curve(pos=[V(-0.233,0,0.59), V(0.233,0,0.59)],
                    frame=xmas,
                    radius=0.02,
                    material=SPACERMAT,
                    color=color.white)
  s3 = visual.curve(pos=[V(0, -0.233, 0.59), V(0, 0.233, 0.59)],
                    frame=xmas,
                    radius=0.02,
                    material=SPACERMAT,
                    color=color.white)

  # This is an approximation to the LNA and feedhorn at the top of the tree
  lna = visual.box(pos=V(0, 0, 1.63),
                   frame=xmas,
                   height=0.03, length=0.03, width=0.08,
                   material=SPACERMAT,
                   color=color.white)

  # This is the cable duct going vertically down the centre of the tree from the LNA
  pole = visual.curve(pos=[V(0, 0, 0.38), V(0,0,1.73)], frame=xmas, radius=POLER, material=POLEMAT, color=color.white)

  olist.append([s1, s2, s3, lna, pole])
  return xmas, olist


def getbundle(spos=None, bframe=None):   # spos is  position that cable centre exits the box
  """Returns a single bundle of 64 dipole cables as they exit the APIU. The parameter 'spos'
     is the point at which they exit the SPIU box.

     If the 'bframe' parameter is given, all objects are created inside this frame.

     Note that the cable bundle returned always faces East - it most be rotated around
     'spos' after it's created for bundles exiting the West side of the APIU.

     Returned is a tuple of (cframe, blist) where cframe is the frame containing the cable
     bundle, and blist is the list of component objects."""
  cframe = visual.frame(frame=bframe)
  startz = spos.z   # Height above ground that cable centre exits the APIU box

  # Arc from the entry point (horizontal) to halfway to the ground (vertical)
  carc1 = visual.paths.arc(radius=startz / 2, angle1=visual.pi, angle2=visual.pi / 2, up=(0, -1, 0))
  carc1.pos = [p + spos + V(0, 0, -startz / 2) for p in carc1.pos]
  c1 = visual.curve(frame=cframe, pos=carc1, radius=0.08 / 2, color=color.blue)

  # Arc from halfway to the ground (vertical) to the ground (horizontal)
  carc2 = visual.paths.arc(radius=startz / 2, angle1=visual.pi, angle2=visual.pi / 2, up=(0, 1, 0))
  carc2.pos = [p + spos + V(startz, 0, -startz / 2) for p in carc2.pos]
  c2 = visual.curve(frame=cframe, pos=carc2, radius=0.08 / 2, color=color.blue)

  # Append a point to the curve 1.5m out in the desert, fading from blue to the ground color
  c2.append(pos=spos + V(1.5, 0, -startz), color=GCOLOR)

  blist = [c1, c2]
  return cframe, blist


def getapiu():
  """Returns an APIU box at (0,0,0), with sun shields, cable suppports, lid, cable bundles.

     Returned value is a tuple of (apiu, olist) where apiu is the frame containing the APIU, and
     olist is the list of component objects
  """
  apiu = visual.frame()
  # Main APIU box object
  box = visual.box(frame=apiu,
                   pos=V(0, 0, 0.800/2 + 0.12),
                   length=0.800, height=1.050, width=0.800,
                   color=color.white)

  # Pyramid shaped lid on box
  hat = visual.pyramid(frame=apiu, pos=V(0, 0, 0.800 + 0.12), size=V(0.06, 1.050, 0.800), axis=V(0,0,1), color=color.white)

  # These objects define the I beams that the box is resting on
  rv1 = visual.box(frame=apiu, pos=V(-0.3, 0, 0.055), length=0.01, height=1.250, width=0.10, color=color.white)
  rt1 = visual.box(frame=apiu, pos=V(-0.3, 0, 0.115), length=0.10, height=1.250, width=0.01, color=color.white)
  rb1 = visual.box(frame=apiu, pos=V(-0.3, 0, 0.005), length=0.10, height=1.250, width=0.01, color=color.white)
  rv2 = visual.box(frame=apiu, pos=V(0.3, 0, 0.055), length=0.01, height=1.250, width=0.10, color=color.white)
  rt2 = visual.box(frame=apiu, pos=V(0.3, 0, 0.115), length=0.10, height=1.250, width=0.01, color=color.white)
  rb2 = visual.box(frame=apiu, pos=V(0.3, 0, 0.005), length=0.10, height=1.250, width=0.01, color=color.white)

  # These objects define the sun-shield plates with an air-gap around the sides of the box
  sss = visual.box(frame=apiu, pos=V(0, -1.050 / 2 - 0.030, 0.800 / 2 + 0.12), length=0.800, height=0.003, width=0.800, color=color.white)
  ssn = visual.box(frame=apiu, pos=V(0, 1.050 / 2 + 0.030, 0.800 / 2 + 0.12), length=0.800, height=0.003, width=0.800, color=color.white)
  sse = visual.box(frame=apiu, pos=V(-0.800 / 2 - 0.030, 0, 0.600 / 2 + 0.12), length=0.003, height=1.050, width=0.600, color=color.white)
  ssw = visual.box(frame=apiu, pos=V(0.800 / 2 + 0.030, 0, 0.600 / 2 + 0.12), length=0.003, height=1.050, width=0.600, color=color.white)

  # Add all the above to the component object list:
  olist = [box, hat, rv1, rt1, rb1, rv2, rt2, rb2, sss, ssn, sse, ssw]

  # Create four fibre cable bundles exiting the East side of the APIU
  cbylist = [-0.2775, -0.1255, 0.1255, 0.2775]
  cblist = []
  for cy in cbylist:
    # Bridle support for fibre bundle, with helical cable support
    cblist.append(visual.cylinder(frame=apiu, pos=V(-0.800/2, cy, 0.700 + 0.120), axis=(-0.100, 0, 0), radius=0.01))
    cblist.append(visual.helix(frame=apiu,
                               pos=V(-0.800 / 2 - 0.150, cy, 0.700 + 0.120 - 0.05),
                               axis=(0.05, 0, 0),
                               radius=0.050,
                               thickness=0.01,
                               coils=1,
                               up=(0,1,0),
                               color=color.white))
    # Cable bundle itself
    cb, tlist = getbundle(bframe=apiu, spos=V(-0.800 / 2, cy, 0.700 + 0.120 - 0.05))
    cblist += tlist
    cb.rotate(angle=visual.pi, axis=(0,0,1), origin=V(-0.800 / 2, cy, 0.700 + 0.120 - 0.05))  # Rotate bundle to face East

  # Create four fibre cable bundles exiting the West side of the APIU
  for cy in cbylist:
    # Bridle support for fibre bundle, with helical cable support
    cblist.append(visual.cylinder(frame=apiu, pos=V(0.800 / 2, cy, 0.700 + 0.120), axis=(0.100, 0, 0), radius=0.01))
    cblist.append(visual.helix(frame=apiu,
                               pos=V(0.800 / 2 + 0.10, cy, 0.700 + 0.120 - 0.05),
                               axis=(0.05, 0, 0),
                               radius=0.050,
                               thickness=0.01,
                               coils=1,
                               up=(0, 1, 0),
                               color=color.white))
    # Cable bundle itself
    cb, tlist = getbundle(bframe=apiu, spos=V(0.800 / 2, cy, 0.700 + 0.120 - 0.05))
    cblist += tlist

  olist += cblist
  return apiu, olist


def gettreecable(treepos=V(0,0,0)):
  """Returns a single arc of cable from vertical (exiting duct at centre of dipole) to
     horizontal (short distance from base, shading to the ground color).

     The cable is positioned for a Christmas Tree positioned at 'treepos', and the
     cable points towards the APIU at (0,0,0).

     Returned is a tuple (cable, olist) where cable is the frame containing the
     curve (we need a frame for a single curve object, because curve objects can't
     be rotated), and a list containing the single component object.
  """
  cframe = visual.frame()
  cstartpos = treepos + (0, 0, 0.4)    # Where the cable leaves the xmas tree trunk
  theta = visual.atan2(treepos.y, treepos.x)  # Angle to the APIU at (0,0,0)

  carc = visual.paths.arc(radius=0.37, angle1=-visual.pi/2, angle2=0, up=(0,-1,0))
  carc.pos = [p + treepos + V(0.37, 0, 0.4) for p in carc.pos[::-1]]

  c1 = visual.curve(frame=cframe, pos=carc, radius=0.0129 / 2, color=color.blue)
  c1.append(pos=treepos + V(1.5, 0, -0.065), color=GCOLOR)
  cframe.rotate(angle=theta + visual.pi, axis=(0, 0, 1), origin=cstartpos)

  return cframe, [c1]



def processClick(event):
  """Called if a key was pressed, or a mouse button clicked.

     Currently only used to handle a left mouse click somewhere in the field of view. The
     3D position on the object under the cursor is used as the new 'centre' position around
     which mouse movement rotates and zooms the view.
  """
  try:      # Key pressed:
    s = event.key   # Returns a string if a key has been pressed
  except AttributeError:
    s = None     # Must have been a mouse click

  if s is not None:  # We have a keypress:
    print "Key pressed: '%s'" % s   # Handle keypresses here, if we want to
  else:             # Mouse clicked:
    clickedpos = event.pickpos   # The 3D position on the surface of the object clicked on
    if clickedpos:
      scene.center = clickedpos  # Change the camera centre position


if __name__ == '__main__':
  scene.bind('click keydown', processClick)   # Capture mouse clicks and key presses

  apiu = getapiu()  # Create the central APIU box at (0,0,0)

  # Create the ground sheet, and show a photo of the MRO as a surface texture
  ground = visual.cylinder(pos=V(0,0,-0.2), radius=20.0, axis=V(0,0,0.2),
                           material=GMAT)

  posfile = open('aavspositions.txt', 'r')
  lines = posfile.readlines()
  bases = []
  for line in lines:   # Loop over all AAVS1.0 dipole positions
    x, y = tuple(map(float, line.split()))   # Get the N/S and E/W coordinates, in meters from the centre

    # Create the base object at that position, by extruding the 2D shape (basep) up in the Z direction by 0.065m.
    b = visual.extrusion(pos=[V(x, y, 0.0), V(x, y, 0.065)], shape=basep, material=materials.rough, color=color.gray(0.4))
    bases.append(b)

    # Create a Christmas Tree object at that position
    tree, elist = getxmas()
    tree.pos = (x, y, 0.065)
    cable = gettreecable(tree.pos)  # And add a cable tail from the Christmas Tree, pointing towards the centre

  eaxis = visual.arrow(pos=V(0, 0, 0), axis=V(2, 0, 0), color=color.blue, shaftwidth=0.1, fixedwidth=True, opacity=0.2)
  naxis = visual.arrow(pos=V(0, 0, 0), axis=V(0, 2, 0), color=color.blue, shaftwidth=0.1, fixedwidth=True, opacity=0.2)
  eaxislabel = visual.text(text='E', pos=(2, 0 ,0.2), height=0.5, depth=0.1, color=color.blue, opacity=0.2)
  naxislabel = visual.text(text='N', pos=(0, 2 ,0.2), height=0.5, depth=0.1, color=color.blue, opacity=0.2)

  while True:
    visual.rate(10)