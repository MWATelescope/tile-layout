__author__ = 'andrew'

import visual
from visual import color

pdict = {}

simplist = []
complist = []

ARROWWIDTH = 1.0

seltile = None
tlabel = None

def getdipole(cpos=None):
  width = 0.35  # Center to edge of batwing
  height = 0.4  # Top of batwing corner to ground
  standoff = 0.1 # ground to bottom of batwing triangle
  cylen = 0.15  # length of LNA cylinder
  cydia = 0.15  # diameter of LNA cylinder
  cpoint = visual.vector(0,0,(height/2.0 + standoff))
  boxw = 0.05   # thickness of dipole arms
  tubeoff = standoff  # gap between bottom of wire tube and the ground
  if cpos is None:
    cpos = visual.vector((0,0,0))
  elif type(cpos) == tuple:
    cpos = visual.vector(cpos)

  xl = visual.box(pos=visual.vector(-width,0,(height+standoff)/2) + cpos, axis=(0,0,1), height=boxw, width=boxw, length=height+boxw, color=visual.color.gray(0.8), visible=False)
  xlt = visual.box(pos=visual.vector(0,0,cpoint.z) + cpos, axis=(visual.vector(width,0,standoff)-visual.vector(-width,0,height)), height=boxw, width=boxw, color=visual.color.gray(0.8), visible=False)
  xlb = visual.box(pos=visual.vector(0,0,cpoint.z) + cpos, axis=(visual.vector(width,0,height)-visual.vector(-width,0,standoff)), height=boxw, width=boxw, color=visual.color.gray(0.8), visible=False)
  xr = visual.box(pos=visual.vector(width,0,(height+standoff)/2) + cpos, axis=(0,0,1), height=boxw, width=boxw, length=height+boxw, color=visual.color.gray(0.8), visible=False)

  yl = visual.box(pos=visual.vector(0,-width,(height+standoff)/2) + cpos, axis=(0,0,1), height=boxw, width=boxw, length=height+boxw, color=visual.color.gray(0.8), visible=False)
  ylt = visual.box(pos=visual.vector(0,0,cpoint.z) + cpos, axis=(visual.vector(0,width,standoff)-visual.vector(0,-width,height)), height=boxw, width=boxw, color=visual.color.gray(0.8), visible=False)
  ylb = visual.box(pos=visual.vector(0,0,cpoint.z) + cpos, axis=(visual.vector(0,width,height)-visual.vector(0,-width,standoff)), height=boxw, width=boxw, color=visual.color.gray(0.8), visible=False)
  yr = visual.box(pos=visual.vector(0,width,(height+standoff)/2) + cpos, axis=(0,0,1), height=boxw, width=boxw, length=height+boxw, color=visual.color.gray(0.8), visible=False)

  lna = visual.cylinder(pos=visual.vector(0,0,cpoint.z-cylen/2) + cpos, axis=(0,0,cylen), radius=cydia/2.0, color=color.white, visible=False)
#  tube = visual.cylinder(pos=visual.vector(0,0,tubeoff) + cpos, radius=boxw/2.0, axis=(0,0,cpoint.z-standoff), color=color.white, visible=False)
  return [xl,xlt,xlb,xr, yl,ylt,ylb,yr, lna]

def gettile(cpos=None):
  if cpos is None:
    cpos = visual.vector((0,0,0))
  elif type(cpos) == tuple:
    cpos = visual.vector(cpos)

  dip_sep = 1.10       # dipole separations in meters
  xoffsets = [0.0] * 16   # offsets of the dipoles in the W-E 'x' direction
  yoffsets = [0.0] * 16   # offsets of the dipoles in the S-N 'y' direction
  xoffsets[0] = -1.5 * dip_sep
  xoffsets[1] = -0.5 * dip_sep
  xoffsets[2] = 0.5 * dip_sep
  xoffsets[3] = 1.5 * dip_sep
  xoffsets[4] = -1.5 * dip_sep
  xoffsets[5] = -0.5 * dip_sep
  xoffsets[6] = 0.5 * dip_sep
  xoffsets[7] = 1.5 * dip_sep
  xoffsets[8] = -1.5 * dip_sep
  xoffsets[9] = -0.5 * dip_sep
  xoffsets[10] = 0.5 * dip_sep
  xoffsets[11] = 1.5 * dip_sep
  xoffsets[12] = -1.5 * dip_sep
  xoffsets[13] = -0.5 * dip_sep
  xoffsets[14] = 0.5 * dip_sep
  xoffsets[15] = 1.5 * dip_sep

  yoffsets[0] = 1.5 * dip_sep
  yoffsets[1] = 1.5 * dip_sep
  yoffsets[2] = 1.5 * dip_sep
  yoffsets[3] = 1.5 * dip_sep
  yoffsets[4] = 0.5 * dip_sep
  yoffsets[5] = 0.5 * dip_sep
  yoffsets[6] = 0.5 * dip_sep
  yoffsets[7] = 0.5 * dip_sep
  yoffsets[8] = -0.5 * dip_sep
  yoffsets[9] = -0.5 * dip_sep
  yoffsets[10] = -0.5 * dip_sep
  yoffsets[11] = -0.5 * dip_sep
  yoffsets[12] = -1.5 * dip_sep
  yoffsets[13] = -1.5 * dip_sep
  yoffsets[14] = -1.5 * dip_sep
  yoffsets[15] = -1.5 * dip_sep

  gp = visual.box(pos=visual.vector(0,0,0) + cpos, axis=(0,0,1), height=5.0, width=5.0, length=0.05, color=color.gray(0.5), visible=False)
  olist = [gp]
  for i in range(16):
    dlist = getdipole(cpos=visual.vector(xoffsets[i], yoffsets[i], 0) + cpos)
    olist += dlist
  return olist


def plot(tiles=None, pads=None):
  global simplist, complist, pdict
  visual.scene.autocenter = False   # Disable autocentering and point the camera at the origin to start
  visual.scene.center = (0,0,0)
  visual.scene.show_rendertime = True

  # Draw a transparent grey ground plane, and transparent blue axis arrows and labels
  ground = visual.box(pos=(0,0,0), length=3000, height=3000, width=0.1, color=(0.8,0,0), opacity=0.2)

  eaxis = visual.arrow(pos=(0,0,0), axis=(1600,0,0), color=color.blue, shaftwidth=2, fixedwidth=True, opacity=0.2)
  eaxislabel = visual.text(text='East', pos=(1580,20,0), height=40, depth=10, color=color.blue)

  naxis = visual.arrow(pos=(0,0,0), axis=(0,1600,0), color=color.blue, shaftwidth=2, fixedwidth=True, opacity=0.2)
  naxislabel = visual.text(text='North', pos=(20,1580,0), height=40, depth=10, color=color.blue)

#  aaxis = visual.arrow(pos=(0,0,0), axis=(0,0,100), color=color.blue, shaftwidth=2, fixedwidth=True, opacity=0.2)
#  aaxislabel = visual.text(text='Up', pos=(0,20,80), height=40, depth=10, color=color.blue)

  for tile in tiles:
    complist += gettile(cpos=(tile.east, tile.north, 0.0))
    tcolor = color.green
    if tile.color is not None:
      tcolor = tile.color
    simplist.append(visual.box(pos=(tile.east, tile.north, 0.0), axis=(0,0,1), height=5.0, width=5.0, length=0.2, color=tcolor))
    simplist[-1].name = tile.name

  for pad in pads:
    pobj = visual.box(pos=(pad.east, pad.north, 0.0), length=1.0, height=2.0, width=1.0, color=color.white)
    if not pad.enabled:
      pobj.color = (0.5,0.5,0.5)
    num = int(''.join([c for c in pad.name if c.isdigit()]))
    if divmod(num,2)[1] == 0:
      xoffset = 12
    else:
      xoffset = -12
    if pad.name.endswith('a'):
      yoffset = -8
    else:
      yoffset = 8
#    pobj.label = visual.label(pos=pobj.pos, text=pad.name, xoffset=xoffset, yoffset=yoffset, box=False, line=False, opacity=0.2)
    pobj.label = visual.label(pos=(pobj.pos.x+xoffset, pobj.pos.y+yoffset, pobj.pos.z+10), text=pad.name, height=9)
    pobj.cables = {}
    for tname, tdata in pad.inputs.items():
      tpos = visual.vector(tdata[0].east, tdata[0].north, 0.0)
      cobj = visual.arrow(pos=pobj.pos, axis=(tpos-pobj.pos), shaftwidth=ARROWWIDTH, fixedwidth=True)
      pobj.cables[tname] = cobj
    pdict[pad.name] = pobj

  # Bind mouse click events and key presses to the callback function
  visual.scene.bind('click keydown', processClick)


def update(pad=None, tname=None, fixed=False, color=None):
  pobj = pdict[pad.name]
  if fixed:
    ccolor = visual.color.orange
  else:
    ccolor = visual.color.white
  if (color is not None):
    ccolor = color
    if (color != (1.0,1.0,1.0)):
#      wmult = 3   # only useful for plots showing lightning
      wmult = 1
    else:
      wmult = 1
  else:
    wmult = 1
  if (tname is not None) and (tname in pad.inputs):
    tpos = visual.vector(pad.inputs[tname][0].east, pad.inputs[tname][0].north, 0.0)
    cobj = visual.arrow(pos=pobj.pos, axis=(tpos-pobj.pos), shaftwidth=ARROWWIDTH*wmult, fixedwidth=True, color=ccolor)
    pobj.cables[tname] = cobj
  else:
    for cable in pobj.cables.values():
      cable.visible = False
    pobj.cables = {}
    for tname, tdata in pad.inputs.items():
      tpos = visual.vector(tdata[0].east, tdata[0].north, 0.0)
      cobj = visual.arrow(pos=pobj.pos, axis=(tpos-pobj.pos), shaftwidth=ARROWWIDTH*wmult, fixedwidth=True, color=ccolor)
      pobj.cables[tname] = cobj

def trunk(pad=None):
  pobj = pdict[pad.name]
  trcolor = (0.0,0.9,0.9)
  trobj = visual.arrow(pos=visual.vector(0,0,0), axis=pobj.pos, shaftwidth=ARROWWIDTH*3, fixedwidth=True, color=trcolor)
  trobj.visible = True


def processClick(event):
  global seltile, tlabel
  try:      # Key pressed:
    s = event.key
    if s == 'c':
      for ob in simplist:
        ob.visible = False
      for ob in complist:
        ob.visible = True
    elif s == 's':
      for ob in complist:
        ob.visible = False
      for ob in simplist:
        ob.visible = True
  except AttributeError:             # Mouse clicked:
    clickedpos = event.pickpos   # The 3D position on the surface of the object clicked on
    if clickedpos:
      visual.scene.center = clickedpos  # Change the camera centre position
    ob = event.pick
    try:    
      name = ob.name
      if seltile is not None:
        seltile.color = color.green
        tlabel.visible = False
        del tlabel
      seltile = ob
      seltile.color = color.red
      tlabel = visual.label(pos=(seltile.pos.x, seltile.pos.y, seltile.pos.z+10), text=name, height=10)
    except AttributeError:
      pass


