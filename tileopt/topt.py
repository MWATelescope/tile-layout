__author__ = 'andrew'

import math
import cabplot

TILEFILE = 'config1.txt'
PADFILE = 'pads.txt'

TILES = []
PADS = []
LMATRIX = {}
CONNECTED = []

DELAY = 0.01

class Pad(object):
  """Represents a single receiver pad, which can handle up to 8 inputs from tiles.
  """
  def __init__(self, name='', east=0.0, north=0.0, enabled=False):
    self.name = name
    self.east = east
    self.north = north
    self.enabled = enabled
    self.inputs = {}   # Dict with tile name as key, and tuples of (tileobject,cablelength) as value.

  def __repr__(self):
    if self.enabled:
      s = "%s:\n  " % self.name + '\n  '.join(["%7s = %2.0f m" % (tname, tdata[1]) for tname,tdata in self.inputs.items()]) + "\n"
      mindist, maxdist = 9e99, 0.0
      for tname, tdata in self.inputs.items():
        if tdata[1] < mindist:
          mindist = tdata[1]
        if tdata[1] > maxdist:
          maxdist = tdata[1]
      s += "  Max = %2.1f, Min = %2.1f, difference = %2.1f" % (maxdist, mindist, maxdist - mindist)
      return s
    else:
      return "%s: Disabled" % self.name

  def maxlen(self):
    """Returns the maximum cable length for any connected tile.
    """
    maxl = ('',0.0)
    for tname, tdata in self.inputs.items():
      if tdata[1] > maxl[1]:
        maxl = (tname, tdata[1])
    return maxl

  def minlen(self):
    """Returns the minimum cable length for any connected tile.
    """
    minl = ('',9e99)
    for tname, tdata in self.inputs.items():
      if tdata[1] < minl[1]:
        minl = (tname, tdata[1])
    return minl

  def maxdiff(self):
    return self.maxlen() - self.minlen()

  def freeslot(self):
    """Returns true if there is a free input.
    """
    return len(self.inputs) < 8

  def addtile(self,tileobj):
    """Add the given tile object to the input list.
    """
    if not self.freeslot():
      print "No free slots in pad %s for tile %s" % (self.name, tileobj.name)
      return False

    if tileobj.name in self.inputs:
      print "Tile %s already connected to pad %s" % (tileobj.name, self.name)
      return False

    if tileobj.name in CONNECTED:
      print "Tile %s already connected to a different pad" % (tileobj.name,)
      return False

    clen = LMATRIX[self.name][tileobj.name]
    self.inputs[tileobj.name] = (tileobj, clen)
    CONNECTED.append(tileobj.name)
    print "Connected tile %s to pad %s with cable of %5.1f m" % (tileobj.name, self.name, clen)
    cabplot.update(pad=self, tname=tileobj.name)
    return True

  def findclosest(self):
    """Loop over all unconnected tiles and return the closest one to this receiver
    """
    mindist = 9e99
    mintile = None
    for tileobj in TILES:
      clen = LMATRIX[self.name][tileobj.name]
      if (clen < mindist) and tileobj.name not in CONNECTED:
        mindist = clen
        mintile = tileobj
    return mintile

class Tile(object):
  """Represents a single tile.
  """
  def __init__(self, name='', east=0.0, north=0.0):
    self.name = name
    self.east = east
    self.north = north


def bestinput(tileobj):
  """Given a tile object, find the closest pad with a free input, and return pad object and distance as a tuple.
  """
  mindist = 9e99
  minpad = None
  for pad in PADS:
    clen = LMATRIX[pad.name][tileobj.name]
    if (clen < mindist) and pad.enabled and pad.freeslot():
      mindist = clen
      minpad = pad
  return (minpad,mindist)


def findlongest():
  """Loop over all tiles, and find the one that has the _longest_ distance to its _closest_ receiver.

     The 'connected' argument contains a list of all tile names that have already been connected to pads.
  """
  maxlen = 0.0
  maxtile = None
  maxtilepad = None
  for tileobj in TILES:
    if tileobj.name not in CONNECTED:
      pad, dist = bestinput(tileobj)
      if dist > maxlen:
        maxlen = dist
        maxtile = tileobj
        maxtilepad = pad
  return maxtile, maxlen, maxtilepad


def connectall():
  """Connect all tiles, going from longest cables to shortest.
  """
  connected = []
  while True:
    maxtile, maxlen, maxtilepad = findlongest()
    if maxtile is None:
      break
    maxtilepad.addtile(maxtile)
    cabplot.visual.sleep(DELAY)

  print "All tiles connected"
  prstats()
  while True:
    cabplot.visual.rate(2)



def load():
  global TILES, PADS, LMATRIX
  flines = file(TILEFILE, 'r').readlines()
  for line in flines:
    tname, teast, tnorth = line.split(',')[:3]
    TILES.append(Tile(name=tname, east=float(teast), north=float(tnorth)))

  flines = file(PADFILE, 'r').readlines()
  for line in flines:
    pname, peast, pnorth, penabled = line.split(',')
    PADS.append(Pad(name=pname, east=float(peast), north=float(pnorth), enabled=int(penabled)))

  for tile in TILES:
    for pad in PADS:
      clen = math.sqrt( (tile.east - pad.east)**2 + (tile.north - pad.north)**2)
      if pad.name not in LMATRIX:
        LMATRIX[pad.name] = {}
      LMATRIX[pad.name][tile.name] = clen


def plot(forever=True):
  cabplot.plot(tiles=TILES, pads=PADS)
  if forever:
    while True:
      cabplot.visual.rate(2)



def prstats():
  ctotal = 0.0
  roundtotal = 0.0
  for pad in PADS:
    if pad.enabled:
      print pad
      padtotal = 0.0
      for tname, tdata in pad.inputs.items():
        padtotal += tdata[1]
      roundmax = pad.maxlen()[1] * 8
      print "  total cable: %6.3f km exact, or 8*maxlen = %6.3f km\n" % (padtotal/1000, roundmax/1000)
      ctotal += padtotal
      roundtotal += roundmax
  print "Total cable overall: %7.3f km, or %7.3f km rounded to receiver max lengths" % (ctotal/1000, roundtotal/1000)


load()
plot(forever=False)

if TILEFILE == 'config1.txt':
  for padname in ['Rx12', 'Rx13', 'Rx14']:
    for pad in PADS:
      if pad.name == padname:
        while pad.freeslot():
          tile = pad.findclosest()
          pad.addtile(tile)
          cabplot.visual.sleep(DELAY)


connectall()