__author__ = 'andrew'

"""Tile optimisation for MWA phase 2

   Note - needs 'classic' VPython. Currently, under Windows, do:

   conda install -c mwcraig vpython

   This shouldn't conflict with the glowscript version of python (pip install vpython), because
   the glowscript version installs as 'vpython' and classic installs as 'visual'.

   Classic VPython under Linux is pretty much dead (ancient, and not being developed any more).
"""

import math
import time

import cabplot

#TILEFILE = 'config-compact.txt'   # Hex configuration for Q3 2016 onwards
#PADFILE = 'pads-verycompact.txt'

#TILEFILE = 'config-current.txt'
#PADFILE = 'pads-current.txt'

# TILEFILE = 'config-longbaseline.txt'   # Long-baseline Phase 2 configuration
TILEFILE = 'config-longbaselinenew.txt'  # Adjusted long baseline positions

#PADFILE = 'pads-current.txt'
PADFILE = 'pads-newLB.txt'

OUTFILE = 'topt-run.txt'
CSVFILE = 'topt-run.csv'

KEEPCURRENT = True

#KEEPCURRENT = False   # Don't use KEEPCURRENT=True for long baselines, becuase it would leave the
                      # new LB tiles connected to receivers in the core, with fibres that are too long.

LIGHTNING = []
BADLIGHTNING = []

#Dec 2013 lightning strike
#LIGHTNING = [47, 68, 81,83,84,85,86, 113,115,117,121,122,125,126, 131,133,136,138, 144]
#BADLIGHTNING = [131]

#Nov 2014 lightning strike
#LIGHTNING = [18, 28, 52,54,55,57, 71,72,73,74,75,76,76,78, 81,83,84,87,88, 91,92,93,94,95,96, 101,103,104,108, 111,117,
#             121,126,128, 131,132,134,138,141,143,144,145,151,153,166,167]
#BADLIGHTNING = [76,78, 101,103,104,108, 111, 131,161, 167]

#Jan 2015 lightning strike
#LIGHTNING = [72,73,74,75,76, 81,83,84,85,86,87, 97,98, 101,102,103,104, 111,112,113,114,115,117,118, 121,122,125,126,127,128,
#             134, 144,148, 153, 161,162,163,164,165,166,167,168]
#BADLIGHTNING = [74,76, 101,102,103,104, 112,117, 126, 148, 166,167,168]

# March 2016 lightning strike
#LIGHTNING = [52, 54, 55,
#             72, 75, 76,
#             81, 83, 84, 85, 86, 87,
#             91, 92, 93, 94, 95, 96, 97, 98,   # 93 is intermittent
#             111, 113,
#             122, 128,
#             131, 132, 133, 134,
#             142, 144, 145, 147, 148,
#             151, 152, 158]

# Jan 2017 lightning strike
LIGHTNING = [11, 18,               # rec01
             31, 32,               # rec02
             1021,                 # rec03
             1027, 1032,           # rec04
             1057, 1063,           # rec05
             1050, 1051, 1056,     # rec06
             1041, 1045,           # rec07
             1068, 1072,           # rec10
             68,                   # rec11
             44, 46, 48,           # rec12
             1011, 1015, 1016,     # rec15
             1036
             ]
BADLIGHTNING = [81, 82, 83, 84, 85, 86, 87, 88,   # reC08
                91, 92, 93, 94, 95, 96, 97, 98,   # rec09
                1004, 1005, 1006, 1008,           # rec13
                21, 22, 23, 24, 25, 26, 47, 28    # rec14
               ]
TILEFILE = 'config-compact.txt'   # Hex configuration for Q3 2016 onwards
PADFILE = 'pads-verycompact.txt'

TILES = []
PADS = []
TDICT = {}
PDICT = {}
LMATRIX = {}
CONNECTED = []

FLENGTHS = [90, 150, 230, 320, 400, 524]
FLAVORS = {90:'RG6_90', 150:'RG6_150', 230:'RG6_230', 320:'LMR400_320', 400:'LMR400_400', 524:'LMR400_524'}
FNAMES = [FLAVORS[length] for length in FLENGTHS]

LMULT = 1.00   # Multiply line-of-sight lengths by this, to determine actual cable length
LADD = 10.0    # Add this length (in metres) to scaled line-of-sight length to determine actual cable length

DELAY = 0.05


def tid2name(tid=0):
  """Given a tile ID, return the name of the tile as defined in the config-....txt file. Note that this is NOT
     necessarily the actual tile name as used in the MWA configuration database, hence the quick hack here instead
     of using the metadata service. Generally, this code is being run before the tiles are actually built, let alone
     configured into the metadata.
  """
  if tid < 1000:
    return '%02d' % tid
  elif tid < 1037:
    return 'EastHex%d' % (tid - 1000)
  elif tid < 2000:
    return 'SouthHex%d' % (tid - 1036)
  else:
    return 'Tile%d' % tid


def name2tid(tname=''):
  """Given a tile name as defined in the config-....txt file, return the id of the tile. Note that this is NOT
     necessarily the actual tile name as used in the MWA configuration database, hence the quick hack here instead
     of using the metadata service. Generally, this code is being run before the tiles are actually built, let alone
     configured into the metadata.
  """
  if len(tname) == 2:
    return int(tname)
  elif tname.startswith('EastHex'):
    return int(tname[7:]) + 1000
  elif tname.startswith('SouthHex'):
    return int(tname[8:]) + 1036
  else:
    return 0


class Pad(object):
  """Represents a single receiver pad, which can handle up to 8 inputs from tiles.
  """
  def __init__(self, name='', east=0.0, north=0.0, enabled=False):
    self.name = name
    self.east = east
    self.north = north
    self.enabled = enabled
    self.inputs = {}   # Dict with tile name as key, and tuples of (tileobject,cablelength,flavor) as value.

  def __repr__(self):
    if self.enabled:
      s = "%s:\n  " % self.name + '\n  '.join(["%7s with %s (%2.0f m LoS)" % (tname, tdata[2], tdata[1]) for tname,tdata in self.inputs.items()]) + "\n"
      mindist, maxdist = 9e99, 0.0
      for tname, tdata in self.inputs.items():
        if tdata[1] < mindist:
          mindist = tdata[1]
        if tdata[1] > maxdist:
          maxdist = tdata[1]
      s += "  Max = %2.1f, Min = %2.1f, difference = %2.1f\n" % (maxdist, mindist, maxdist - mindist)
      return s
    else:
      return "%s: Disabled\n" % self.name

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

    flavor = None
    for len in FLENGTHS:
      if (clen * LMULT) + LADD < len:
        flavor = FLAVORS[len]
        break
    if flavor is None:
      flavor = 'FIBRE'

    oldlink = False
    if tileobj.name.startswith('Tile') or tileobj.name[0].isdigit():
      tnum = int(''.join([c for c in tileobj.name if c.isdigit()]))
      rnum, slotnum = divmod(tnum,10)
      oldpad = PDICT['Rx%d' % rnum]
      if (oldpad.east == self.east) and (oldpad.north == self.north):
        oldlink = True

    if color is None and oldlink:
      color = (1.0, 1.0, 0.0)

    tid = name2tid(tileobj.name)
    if tid in BADLIGHTNING:
      color = (1.0, 0.0, 0.0)
      print "%s:%d bad ligtning" % (tileobj.name, tid)
    elif tid in LIGHTNING:
      color = (1.0, 0.3, 0.0)
      print "%s:%d lightning" % (tileobj.name, tid)

    self.inputs[tileobj.name] = (tileobj, clen, flavor)
    CONNECTED.append(tileobj.name)
    print "Connected tile %s to pad %s with cable %s (LoS=%5.1f m)" % (tileobj.name, self.name, flavor, clen)
    if manual or (fixlength is not None):
      cabplot.update(pad=self, tname=tileobj.name, fixed=True, color=color)
    else:
      cabplot.update(pad=self, tname=tileobj.name, fixed=False, color=color)
    cabplot.visual.sleep(DELAY)
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
    self.color = None
    tid = name2tid(self.name)
    if tid in BADLIGHTNING:
      self.color = (1.0, 0.0, 0.0)
      print "%s:%d bad ligtning" % (self.name, tid)
    elif tid in LIGHTNING:
      self.color = (1.0, 0.3, 0.0)
      print "%s:%d lightning" % (self.name, tid)



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
  newtotal = 0.0
  flinks = 0
  rflinks = 0
  oldlinkstotal = 0
  fhist = {}
  ofhist = {}
  for flavor in FNAMES:
    fhist[flavor] = 0
    ofhist[flavor] = 0
  fibrelist = []
  outf = open(OUTFILE, 'w')
  csvf = open(CSVFILE, 'w')
  header = "Tile optimisation run at %s\nTiles=%s, pad configuration=%s\n\n" % (time.ctime(), TILEFILE, PADFILE)
  print header
  outf.write(header)
  csvf.write('# Run at %s, Tiles=%s, Pads=%s\n' % (time.ctime(), TILEFILE, PADFILE))
  for pad in PADS:
    if pad.enabled:
      print pad
      outf.write(str(pad))
      cpad = 0.0
      fpad = 0.0
      newlen = 0.0
      oldlinks = 0
      for tname, tdata in pad.inputs.items():
        tileobj, clen, flavor = tdata
        if flavor == 'FIBRE':
          fibrelist.append(clen)   # Add a fibre of this length to the list
        else:
          fhist[flavor] += 1    # One more cable of this flavor
        if clen <= 525 and 'RX' in pad.name.upper():
          cpad += clen
        else:
          fpad += clen
          flinks += 1
        if tname.startswith('Tile') or tname[0].isdigit():
          tnum = int(''.join([c for c in tname if c.isdigit()]))
          rnum,slotnum = divmod(tnum,10)
          oldpad = PDICT['Rx%d' % rnum]
          if (oldpad.east == pad.east) and (oldpad.north == pad.north):
            oldlinks += 1
            ofhist[flavor] += 1
          else:
            csvf.write('%s, %5.1f, %s\n' % (tileobj.name, clen, flavor))
            newlen += clen
        else:
          csvf.write('%s, %5.1f, %s\n' % (tileobj.name, clen, flavor))
          newlen += clen

      print "  LoS length totals: %4.3f km of copper, %4.3f km of fibre" % (cpad/1000, fpad/1000)
      outf.write("  LoS length totals: %4.3f km of copper, %4.3f km of fibre\n" % (cpad/1000, fpad/1000))
#      clen = pad.maxlen()[1]
#      if clen <= 525 and 'RX' in pad.name.upper():
#        croundtotal += clen*8
#        print "  Equal length cables totals: %4.3f km of COPPER." % (clen*8/1000,)
#      else:
#        froundtotal += clen*8
#        rflinks += 8
#        print "  Equal length cables totals: %4.3f km of FIBRE." % (clen*8/1000,)
      ctotal += cpad
      ftotal += fpad
      newtotal += newlen
      oldlinkstotal += oldlinks
      if 'RX' in pad.name.upper():
        print "  %d existing cables re-used, plus ~%4.3f km of new cable\n" % (oldlinks, newlen/1000)
        outf.write("  %d existing cables re-used, plus ~%4.3f km of new cable\n\n" % (oldlinks, newlen/1000))
      else:
        trlen = math.sqrt(pad.east*pad.east + pad.north*pad.north)
        print "  Trunk length to core is %4.3fkm long, %d tiles wide\n" % (trlen/1000, len(pad.inputs.keys()))
        outf.write("  Trunk length to core is %4.3fkm long, %d tiles wide\n\n" % (trlen/1000, len(pad.inputs.keys())))
        cabplot.trunk(pad)

  summary = '\n'
  summary += "Totals for the whole array:\n"
  summary += "   LoS lengths: %4.3f km of COPPER, %4.3f km of FIBRE\n" % (ctotal/1000, ftotal/1000)
  summary += "   %d existing tile connections re-used, %4.3f km new cables.\n" % (oldlinkstotal, newtotal/1000)
  for flavor in FNAMES:
    summary += "  Cable %s: %d lengths in total, %d of them are re-used.\n" % (flavor, fhist[flavor], ofhist[flavor])
  fibrelist.sort()
  summary += "  Fibre: %d lengths, with Line of Sight (LOS) distances:\n    %s\n" % (len(fibrelist), fibrelist)
  print summary
  outf.write(summary)
  outf.close()
  csvf.close()


if __name__ == '__main__':
  load()
  plot(forever=False)

  #####  Manual connections between tiles and pads, for different configurations ############
  if (TILEFILE == 'config1.txt') and ('pads-compact' in PADFILE):   # Any case with a compact configuration and receivers moved in
    print "Force Rx12, Rx13, Rx14 to be connected to the East hexagon (leaving four copper tiles on that hexagon)."

    pad = PDICT['Rx12']
    for tname in ['HN29', 'HN33', 'HN35', 'HN31', 'HN13', 'HN17', 'HN15', 'HN27', ]:
      pad.addtile(TDICT[tname])
    pad = PDICT['Rx13']
    for tname in ['HN09', 'HN03', 'HN05', 'HN11', 'HN23', 'HN02', 'HN08', 'HN20', ]:
      pad.addtile(TDICT[tname])
    pad = PDICT['Rx14']
    for tname in ['HN04', 'HN06', 'HN12', 'HN24', 'HN18', 'HN16', 'HN28', 'HN32', ]:
      pad.addtile(TDICT[tname])
    pad = PDICT['Rx16']
    for tname in ['HN19', 'HN22', 'HN26', 'HN30', 'HN07', 'HN10', 'HN14', 'HN34', ]:
      pad.addtile(TDICT[tname])

  elif ( ('longbaseline' in TILEFILE) and
         ((PADFILE == 'pads-longbaseline.txt') or (PADFILE == 'pads-newLB.txt')) ):   # Extended configuration with Rx16 left on original pad
    print "Force longer cables and Rx10/Rx16 for the 8 tiles on the far side of the airstrip"
    pad = PDICT['Rx7a']
    for tname in ['LBSW1', 'LBSW2', 'LBSW3', 'LBSW4', 'LBSW5', 'LBSW6', 'LBSW7', 'LBSW8']:
      pad.addtile(TDICT[tname], fixlength=2650.0)

  elif (TILEFILE == 'config1.txt') and (PADFILE == 'pads-verycompact.txt'):
    pad = PDICT['Rx8a']
    for tname in ['HN29', 'HN33', 'HN25', 'HN13', 'HN21', 'HN09', 'HN03', 'HN19']:
      pad.addtile(TDICT[tname])

    pad = PDICT['Rx9a']
    for tname in ['HN35', 'HN31', 'HN17', 'HN15', 'HN27', 'HN05', 'HN11', 'HN23']:
      pad.addtile(TDICT[tname])

    pad = PDICT['Rx1a']
    for tname in ['HN07', 'HN01', 'HN22', 'HN10', 'HN04', 'HN26', 'HN14', 'HN18']:
      pad.addtile(TDICT[tname])

    pad = PDICT['Rx2a']
    for tname in ['HN30', 'HN34', 'HN36', 'HN06', 'HN16', 'HN32', 'HE19', 'HE22']:
      pad.addtile(TDICT[tname])

    pad = PDICT['Rx3a']
    for tname in ['HE35', 'HE31']:
      pad.addtile(TDICT[tname])

    pad = PDICT['Rx4a']
    for tname in ['HE15', 'HE27', 'HE33', 'HE17', 'HE11', 'HE23', 'HE29', 'HE20']:
      pad.addtile(TDICT[tname])

  # Final layout for new hex positions and very compact receiver positions
  elif (TILEFILE == 'config-compact.txt') and (PADFILE == 'pads-verycompact.txt'):
    pad = PDICT['Rx9a']
    for tname in ['EastHex%d' % i for i in [1,2,3,4, 5,6,7,8]]:
      pad.addtile(TDICT[tname])

    pad = PDICT['Rx3']
    for tname in ['EastHex%d' % i for i in [9,10,11,12, 13,14,15,16]]:
      pad.addtile(TDICT[tname])

    pad = PDICT['Rx3a']
    for tname in ['EastHex%d' % i for i in [17,18,19,20, 21,22,23,24]]:
      pad.addtile(TDICT[tname])

    pad = PDICT['Rx4']
    for tname in ['EastHex%d' % i for i in [25,26,27,28, 29,30,31,32]]:
      pad.addtile(TDICT[tname])

    pad = PDICT['Rx4a']
    for tname in (['EastHex%d' % i for i in [33,34,35,36]] +
                  ['SouthHex%d' % i for i in [1,2,3,4]]):
      pad.addtile(TDICT[tname])

    pad = PDICT['Rx5']
    for tname in ['SouthHex%d' % i for i in [5,6,7,8, 9,10,11,12]]:
      pad.addtile(TDICT[tname])

    pad = PDICT['Rx5a']
    for tname in ['SouthHex%d' % i for i in [13,14,15,16, 17,18,19,20]]:
      pad.addtile(TDICT[tname])

    pad = PDICT['Rx6']
    for tname in ['SouthHex%d' % i for i in [21,22,23,24, 25,26,27,28]]:
      pad.addtile(TDICT[tname])

    pad = PDICT['Rx6a']
    for tname in ['SouthHex%d' % i for i in [29,30,31,32, 33,34,35,36]]:
      pad.addtile(TDICT[tname])

    pad = PDICT['Rx1a']
    for tname in ['%d' % i for i in [61,62,63,64, 65,66,67,68]]:
      pad.addtile(TDICT[tname])

    pad = PDICT['Rx2a']
    for tname in ['%d' % i for i in [31,32,33,34, 35,36,37,38]]:
      pad.addtile(TDICT[tname])

    pad = PDICT['Rx1']
    for tname in ['%d' % i for i in [11,12,13,14, 15,16,17,18]]:
      pad.addtile(TDICT[tname])

    pad = PDICT['Rx2']
    for tname in ['%d' % i for i in [27,41,42,43, 44,45,46,48]]:
      pad.addtile(TDICT[tname])

  if KEEPCURRENT:    # Force existing tiles to connect to the receivers they are connected to now, if possible
    for tname,tile in TDICT.items():
      if tname.startswith('Tile') or tname[0].isdigit():
        tnum = int(''.join([c for c in tname if c.isdigit()]))
        rnum,slotnum = divmod(tnum,10)
        pname = 'Rx%d' % rnum
        if PDICT[pname].enabled and PDICT[pname].freeslot():
          tid = tnum
          if tid in BADLIGHTNING:
            ccolor = (1.0,0.0,0.0)
            print "%s:%d bad ligtning" % (pname, tid)
          elif tid in LIGHTNING:
            ccolor = (1.0,0.3,0.0)
            print "%s:%d lightning" % (pname, tid)
#          elif len(BADLIGHTNING):
#            ccolor = (1.0,1.0,1.0)
          else:
            ccolor = (1.0, 1.0, 0.0)
          PDICT[pname].addtile(tile, color=ccolor)
        else:
          oldpad = PDICT[pname]
          for newpad in PADS:
            if (oldpad.east == newpad.east) and (oldpad.north == newpad.north) and (newpad.enabled) and (newpad.freeslot()):
              newpad.addtile(tile)

  connectall()
