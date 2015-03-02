__author__ = 'andrew'

import math
import cabplot

TILEFILE = 'config-current.txt'
PADFILE = 'pads-current.txt'

KEEPCURRENT = True

#Dec 2013 lightning strike
#LIGHTNING = [47, 68, 81,83,84,85,86, 113,115,117,121,122,125,126, 131,133,136,138, 144]
#BADLIGHTNING = [131]

#Nov 2014 lightning strike
#LIGHTNING = [18, 28, 52,54,55,57, 71,72,73,74,75,76,76,78, 81,83,84,87,88, 91,92,93,94,95,96, 101,103,104,108, 111,117,
#             121,126,128, 131,132,134,138,141,143,144,145,151,153,166,167]
#BADLIGHTNING = [76,78, 101,103,104,108, 111, 131,161, 167]

#Jan 2015 lightning strike
LIGHTNING = [72,73,74,75,76, 81,83,84,85,86,87, 97,98, 101,102,103,104, 111,112,113,114,115,117,118, 121,122,125,126,127,128,
             134, 144,148, 153, 161,162,163,164,165,166,167,168]
BADLIGHTNING = [74,76, 101,102,103,104, 112,117, 126, 148, 166,167,168]

#LIGHTNING = []
#BADLIGHTNING = []

TILES = []
PADS = []
TDICT = {}
PDICT = {}
LMATRIX = {}
CONNECTED = []

DELAY = 0.001

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
    if 'DP' in self.name.upper():
      return True
    else:
      return len(self.inputs) < 8

  def addtile(self, tileobj, fixlength=None, manual=True, color=None):
    """Add the given tile object to the input list.

       If fixlength is given (in metres), use that as the cable length instead of
       the straight-line distance between tile and pad (for manually forcing
       connections).

       If manual is True (the default), or if a fixed length is supplied,
       indicate by arrow color that the connection has
       been manually chosen, not automatically picked by the algorithm.
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

    if fixlength is not None:
      clen = fixlength
    else:
      clen = LMATRIX[self.name][tileobj.name]

    self.inputs[tileobj.name] = (tileobj, clen)
    CONNECTED.append(tileobj.name)
    print "Connected tile %s to pad %s with cable of %5.1f m" % (tileobj.name, self.name, clen)
    if manual or (fixlength is not None):
      cabplot.update(pad=self, tname=tileobj.name, fixed=True, color=color)
    else:
      cabplot.update(pad=self, tname=tileobj.name, fixed=False, color=color)
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
    maxtilepad.addtile(maxtile, manual=False)
    cabplot.visual.sleep(DELAY)

  print "All tiles connected"
  prstats()
  while True:
    cabplot.visual.rate(2)



def load():
  global TILES, PADS, LMATRIX, PDICT, TDICT
  flines = file(TILEFILE, 'r').readlines()
  for line in flines:
    tname, teast, tnorth = line.split(',')[:3]
    tile = Tile(name=tname, east=float(teast), north=float(tnorth))
    TILES.append(tile)
    TDICT[tname] = tile

  flines = file(PADFILE, 'r').readlines()
  for line in flines:
    pname, peast, pnorth, penabled = line.split(',')
    pad = Pad(name=pname, east=float(peast), north=float(pnorth), enabled=int(penabled))
    PADS.append(pad)
    PDICT[pname] = pad

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
  ftotal = 0.0
  ctotal = 0.0
  froundtotal = 0.0
  croundtotal = 0.0
  newtotal = 0.0
  flinks = 0
  rflinks = 0
  oldlinkstotal = 0
  for pad in PADS:
    if pad.enabled:
      print pad
      cpad = 0.0
      fpad = 0.0
      pflink = 0
      newlen = 0.0
      oldlinks = 0
      for tname, tdata in pad.inputs.items():
        clen = tdata[1]
        if clen <= 525 and 'RX' in pad.name.upper():
          cpad += clen
        else:
          fpad += clen
          flinks += 1
        if tname.startswith('Tile'):
          tnum = int(''.join([c for c in tname if c.isdigit()]))
          rnum,slotnum = divmod(tnum,10)
          oldpad = PDICT['Rx%d' % rnum]
          if (oldpad.east == pad.east) and (oldpad.north == pad.north):
            oldlinks += 1
          else:
            newlen += clen
        else:
          newlen += clen

      print "  Exact cable length totals: %4.3f km of copper, %4.3f km of fibre" % (cpad/1000, fpad/1000)
      clen = pad.maxlen()[1]
      if clen <= 525 and 'RX' in pad.name.upper():
        croundtotal += clen*8
        print "  Equal length cables totals: %4.3f km of COPPER." % (clen*8/1000,)
      else:
        froundtotal += clen*8
        rflinks += 8
        print "  Equal length cables totals: %4.3f km of FIBRE." % (clen*8/1000,)
      ctotal += cpad
      ftotal += fpad
      newtotal += newlen
      oldlinkstotal += oldlinks
      if 'RX' in pad.name.upper():
        print "  %d existing tile connections re-used, %4.3f km of new cable to be found" % (oldlinks, newlen/1000)
      else:
        trlen = math.sqrt(pad.east*pad.east + pad.north*pad.north)
        print "  Trunk length to core is %4.3fkm long, %d tiles wide" % (trlen/1000, len(pad.inputs.keys()))
        cabplot.trunk(pad)

  print
  print "Totals for the whole array:"
  print "   Exact lengths   - %4.3f km of COPPER, %4.3f km of FIBRE in %d links" % (ctotal/1000, ftotal/1000, flinks)
  print "   Rounded lengths - %4.3f km of COPPER, %4.3f km of FIBRE in %d links" % (croundtotal/1000, froundtotal/1000, rflinks)
  print "   %d existing tile connections re-used, %4.3f km of new cables to be found" % (oldlinkstotal, newtotal/1000)


load()
plot(forever=False)



if (TILEFILE == 'config1.txt') and ('pads-compact' in PADFILE):   # Any case with a compact configuration and receivers moved in
  print "Force Rx12, Rx13, Rx14 to be connected to the East hexagon (leaving four copper tiles on that hexagon)."

  pad = PDICT['Rx12']
  for tname in ['HN29', 'HN33', 'HN35', 'HN31', 'HN13', 'HN17', 'HN15', 'HN27', ]:
    pad.addtile(TDICT[tname])
    cabplot.visual.sleep(DELAY)
  pad = PDICT['Rx13']
  for tname in ['HN09', 'HN03', 'HN05', 'HN11', 'HN23', 'HN02', 'HN08', 'HN20', ]:
    pad.addtile(TDICT[tname])
    cabplot.visual.sleep(DELAY)
  pad = PDICT['Rx14']
  for tname in ['HN04', 'HN06', 'HN12', 'HN24', 'HN18', 'HN16', 'HN28', 'HN32', ]:
    pad.addtile(TDICT[tname])
    cabplot.visual.sleep(DELAY)
  pad = PDICT['Rx16']
  for tname in ['HN19', 'HN22', 'HN26', 'HN30', 'HN07', 'HN10', 'HN14', 'HN34', ]:
    pad.addtile(TDICT[tname])
    cabplot.visual.sleep(DELAY)

elif (TILEFILE == 'config2.txt') and (('pads-compact2' in PADFILE) or ('pads-compact3' in PADFILE)):   # Extended configuration with Rx16 left on original pad
  print "Force longer cables and Rx16 for the 8 tiles on the far side of the airstrip"
  if 'pads-compact2' in PADFILE:
    pad = PDICT['Rx16']
  else:
    pad = PDICT['Rx10']
  for tname in ['LB_SW1', 'LB_SW2', 'LB_SW3', 'LB_SW4', 'LB_SW5', 'LB_SW6', 'LB_SW7', 'LB_SW8']:
    pad.addtile(TDICT[tname], fixlength=2650.0)
    cabplot.visual.sleep(DELAY)

elif (TILEFILE == 'config1.txt') and (PADFILE == 'pads-verycompact.txt'):
  pad = PDICT['Rx8a']
  for tname in ['HN29', 'HN33', 'HN25', 'HN13', 'HN21', 'HN09', 'HN03', 'HN19']:
    pad.addtile(TDICT[tname])
    cabplot.visual.sleep(DELAY)

  pad = PDICT['Rx9a']
  for tname in ['HN35', 'HN31', 'HN17', 'HN15', 'HN27', 'HN05', 'HN11', 'HN23']:
    pad.addtile(TDICT[tname])
    cabplot.visual.sleep(DELAY)

  pad = PDICT['Rx1a']
  for tname in ['HN07', 'HN01', 'HN22', 'HN10', 'HN04', 'HN26', 'HN14', 'HN18']:
    pad.addtile(TDICT[tname])
    cabplot.visual.sleep(DELAY)

  pad = PDICT['Rx2a']
  for tname in ['HN30', 'HN34', 'HN36', 'HN06', 'HN16', 'HN32', 'HE19', 'HE22']:
    pad.addtile(TDICT[tname])
    cabplot.visual.sleep(DELAY)

  pad = PDICT['Rx3a']
  for tname in ['HE35', 'HE31']:
    pad.addtile(TDICT[tname])
    cabplot.visual.sleep(DELAY)

  pad = PDICT['Rx4a']
  for tname in ['HE15', 'HE27', 'HE33', 'HE17', 'HE11', 'HE23', 'HE29', 'HE20']:
    pad.addtile(TDICT[tname])
    cabplot.visual.sleep(DELAY)


if KEEPCURRENT:    # Force existing tiles to connect to the receivers they are connected to now, if possible
  for tname,tile in TDICT.items():
    if tname.startswith('Tile'):
      tnum = int(''.join([c for c in tname if c.isdigit()]))
      rnum,slotnum = divmod(tnum,10)
      pname = 'Rx%d' % rnum
      if PDICT[pname].enabled and PDICT[pname].freeslot():
        tid = int(tname[4:])
        if tid in BADLIGHTNING:
          ccolor = (1.0,0.0,0.0)
        elif tid in LIGHTNING:
          ccolor = (1.0,0.8,0.0)
        elif len(BADLIGHTNING):
          ccolor = (1.0,1.0,1.0)
        else:
          ccolor = None
        PDICT[pname].addtile(tile, color=ccolor)
        cabplot.visual.sleep(DELAY)
      else:
        oldpad = PDICT[pname]
        for newpad in PADS:
          if (oldpad.east == newpad.east) and (oldpad.north == newpad.north) and (newpad.enabled) and (newpad.freeslot()):
            newpad.addtile(tile)
            cabplot.visual.sleep(DELAY)


connectall()