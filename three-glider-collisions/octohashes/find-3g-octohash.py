# find-octo3g.py
# Dave Greene, 15 August 2022 (Golly Python3)
######## Download hash files from https://drive.google.com/drive/folders/1l6TQEgNpXpFd6ATU7Tgrf7k-76MJcVi3
######## Then update line 10 below with your chosen location for the downloaded files

import golly as g
import hashlib


basepath = "C:/path/to/3-glider-collisions/octohashes"  ###### UPDATE THIS TO MATCH YOUR DOWNLOAD LOCATION


searchfiles = "octohashes3g_0.txt,octohashes3g_1.txt,octohashes3g_2.txt,octohashes3g_3.txt,octohashes3g_4.txt," + \
              "octohashes3g_5.txt,octohashes3g_6.txt,octohashes3g_7.txt,octohashes3g_8.txt,octohashes3g_9.txt," + \
              "octohashes3g_10.txt,octohashes3g_11.txt,octohashes3g_12.txt,octohashes3g_13.txt,octohashes3g_14.txt," + \
              "octohashes3g_15.txt,octohashes3g_16.txt,octohashes3g_17.txt,octohashes3g_18.txt,octohashes3g_19.txt"
searchlist = searchfiles.split(",")

NUMLINES = 464746

chardict = {}
for i in range(37, 127):
  chardict[i-37] = chr(i)

chardict[92-37] = "!"  # backslash
chardict[39-37] = "#"  # apostrophe
chardict[44-37] = "$"  # comma

def get9char(inputstr):
  h = hashlib.sha1()
  h.update(inputstr.encode())
  i = 0  # convert first seven bytes of SHA1 digest to an integer
  for char in h.digest()[:7]:
    i = i*256 + char
  s = ""
  while len(s)<9:
    d = i//90
    r = i - d*90
    s = chardict[r] + s
    i = (i - r) // 90
  return s

def getoctohash(clist):
  ptr = 0
  g.new("Octotest"+str(count))
  for orientation in [[1,0,0,1],[0,-1,1,0],[-1,0,0,-1],[0,1,-1,0],[-1,0,0,1],[1,0,0,-1],[0,1,1,0],[0,-1,-1,0]]:
    g.putcells(clist,ptr*2048,0,*orientation)
    ptr += 1
  for j in range(8):
    g.select([2048*j-1024,-1024,2048,2048])
    g.shrink()
    r = g.getselrect()
    if r == []: r = [0,0,1,1]
    pat = g.getcells(r)
    deltax, deltay = 0, 0
    if pat != []:
      deltax, deltay = -pat[0], -pat[1]
    if j==0:
      minstr = str(g.transform(pat, deltax, deltay))
    else:
      strpat = str(g.transform(pat, deltax, deltay))
      if  strpat < minstr:
        minstr = strpat
  return " " + get9char(minstr)

g.setalgo("HashLife")
g.setrule("B3/S23")

try:
  g.fitsel()
except:
  pass
r = g.getselrect()
if r==[]:
  r = g.getrect()
  if r==[0]:
    g.exit("No pattern found to search for.")
  g.select(r)

count = NUMLINES
outptr = 0
pat = g.getcells(r)

g.addlayer()  # do tests in a new layer, then put results there
hash = getoctohash(pat)
g.new("Output")
g.putcells(pat,-pat[0]-128,-pat[1])
g.fit()
g.update()

for fingerprintfile in searchlist:
  with open(basepath+fingerprintfile, "r") as f:
    for line in f:
      count -= 1
      if hash in line:
        matchingpat = line[:line.index(" ")]
        g.putcells(g.parse(matchingpat),outptr*64,0)
        outptr+=1
        g.fit()
        g.update()
      if count % 1000 == 0:
        g.show("Searching.  Lines remaining: " + str(count/1000) + "K lines.")
plural = "" if outptr==1 else "s"
g.show("Found " + str(outptr) + " line" + plural + " matching " + hash + " in " + str(NUMLINES) + " lines of the octo3obj database.")
g.setclipstr(str(count))
