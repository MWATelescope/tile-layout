import math

f = open('newpos.csv','r')
pointlist = []
for line in f.readlines()[1:]:
  print line
  pointlist.append((line.split(',')[0], map(float, line.split(',')[1:])))

#tlist = [map(float, t.split(',')) for t in f.readlines()[1:]]


def sexstring(value=0, sp=':', fixed=False, dp=None):
  """Convert the floating point 'value' into a sexagecimal string.
     The character in 'sp' is used as a spacer between components. Useful for
     within functions, not on its own.
     eg: sexstring(status.TJ.ObjRA,' ')
  """
  if fixed:
    dp = 0
  if dp is None:
    dp = 1
  else:
    if dp is None:
      dp = 1
    dp = int(dp)
  try:
    aval = abs(value)
    error = 0
  except TypeError:
    aval = 0.0
    error = 1
  if value < 0:
    outs = '-'
  else:
    outs = ''
  D = int(aval)
  M = int((aval - float(D)) * 60)
  S = (aval - float(D) - (float(M)/60)) * 3600
  Si = int(S)
  Sf = round(S-Si,dp)
  if Sf == 1.0:
    Si += 1
    if Si == 60:
      Si = 0
      M += 1
      if M == 60:
        M = 0
        D += 1
    Sf = 0.0
  outs += '%02i%s%02i%s%02i' % (D, sp, M, sp, Si)
  if dp > 0:
    fstr = ".%%0%id" % dp
    outs += fstr % int(Sf*(10**dp))
  if error:
    return ''
  else:
    return outs


def stringsex(value=""):
  """Convert the sexagesimal coordinate 'value' into a floating point
     result. Handles either a colon or a space as seperator, but currently
     requires all three components (H:M:S not H:M or H:M.mmm).
  """
  try:
    value = value.strip()
    components = value.split(':')
    if len(components)<>3:
      components=value.split(' ')
    if len(components)<>3:
      return None

    h,m,s = tuple([s.strip() for s in components])
    sign=1
    if h[0]=="-":
      sign=-1
    return float(h) + (sign*float(m)/60.0) + (sign*float(s)/3600.0)
  except:
    return None



#Northernmost
LAT111 = stringsex('-26:41:18.07773')
LONG111 = stringsex('116:40:2.77319')
E111 = 466914.118
N111 = 7048038.428

#Southermost
LAT151 = stringsex('-26:42:45.74414')
LONG151 = stringsex('116:40:38.49408')
E151 = 467908.111
N151 = 7045343.868

#Westernmost
LAT107 = stringsex('-26:42:9.20244')
LONG107 = stringsex('116:39:35.79371')
E107 = 466172.717
N107 = 7046463.588

#Easternmost
LAT133 = stringsex('-26:41:54.05104')
LONG133 = stringsex('116:41:2.35744')
E133 = 468563.507
N133 = 7046935.881

SLAT = (LAT111-LAT151)/(N111-N151)
SLONG = (LONG133-LONG107)/(E133-E107)



class Pos(object):
  def __init__(self, e=None, n=None, h=None, lat=None, long=None):
    self.h = h
    if (e is not None) and (n is not None):
      self.lat = 0.0
      self.long = 0.0
      self.e = e
      self.n = n
      self.calclatlong()
    elif (lat is not None) and (long is not None):
      self.lat = lat
      self.long = long
      self.e = 0.0
      self.n = 0.0

  def calclatlong(self):
    de = self.e - E107
    dn = self.n - N151
    self.lat = dn*SLAT + LAT151
    self.long = de*SLONG + LONG107

  def __repr__(self):
    return "Pos: E=%15.3f, N=%15.3f, Lat=%s, Long=%s" % (self.e, self.n, sexstring(self.lat,dp=6), sexstring(self.long,dp=6))


TEMPLATE = """
   <waypoint>
      <name id="%(name)s">%(name)s</name>
      <coord lat="%(lat)f" lon="%(long)f"/>
      <type>Waypoint</type>
   </waypoint>
"""

#tiles = {}
#recs = {}

waypoints = {}

#for i in range(len(tlist)):
#  t = tlist[i]
#  tiles[int(t[0])] = Pos(t[1],t[2],t[3])
#  if t[0].start
#  if divmod(i,8)[1] == 0:
#    recs[divmod(i,8)[0]+1] = Pos(t[4],t[5],t[3])

for point in pointlist:
  name, coords = point
  p = Pos(h=coords[3], long=coords[4], lat=coords[5])
  waypoints[name] = p

outf = open('mwawaypoints.loc', 'w')

outf.write('<?xml version="1.0" encoding="UTF-8"?>\n <loc version="1.0" src="Groundspeak">\n')

nlist = waypoints.keys()
nlist.sort()

for n in nlist:
  p = waypoints[n]
  outf.write(TEMPLATE % {'name':n, 'lat':p.lat, 'long':p.long})

#for id,t in tiles.items():
#  r = recs[divmod(id,10)[0]]
#  outf.write(TEMPLATE % {'name':'T'+str(id), 'lat':t.lat, 'lon':t.long})

outf.write('</loc>\n')

outf.close()

#outf = open('recs.loc', 'w')
#outf.write('<?xml version="1.0" encoding="UTF-8"?>\n <loc version="1.0" src="Groundspeak">\n')

#for id,r in recs.items():
#  outf.write(TEMPLATE % {'name':'REC'+str(id), 'lat':r.lat, 'lon':r.long})

#outf.write('</loc>\n')

#outf.close()

