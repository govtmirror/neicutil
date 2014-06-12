#!/usr/bin/python

from numpy import *
import copy

class GMTColormapException:
      """Used to handle errors in the GMTColormap class"""

class GMTColormap:
      ZValues = array([])
      ColorList = array([])
      ColorDict = {'red':[],'green':[],'blue':[]}

      def __init__(self,cptfile):
            f = open(cptfile,'rt')
            clines = f.readlines()
            f.close()
            ncolors = 0
            for line in clines:
                  if line.find('#') >= 0:
                        continue
                  ncolors += 1
            ncolors += 1

            self.ColorList = zeros((ncolors,3))
            self.ZValues = zeros(ncolors)
            idx = 0
            lastDmax = 0
            rlow = zeros(ncolors)
            rhigh = zeros(ncolors)
            glow = zeros(ncolors)
            ghigh = zeros(ncolors)
            blow = zeros(ncolors)
            bhigh = zeros(ncolors)
            dmin = zeros(ncolors)
            dmax = zeros(ncolors)
            for line in clines:

                  #deal with "#" comments
                  pidx = line.find('#')
                  if pidx >= 0:
                        line = line[0:pidx].strip()
                        if line == '':
                              continue
                  parts = line.split()
                  dmin[idx] = float(parts[0])
                  rlow[idx] = float(parts[1])/255.0
                  glow[idx] = float(parts[2])/255.0
                  blow[idx] = float(parts[3])/255.0
                  dmax[idx] = float(parts[4])
                  rhigh[idx] = float(parts[5])/255.0
                  ghigh[idx] = float(parts[6])/255.0
                  bhigh[idx] = float(parts[7])/255.0
                  self.ColorList[idx,:] = array([rlow[idx],glow[idx],blow[idx]])
                  self.ZValues[idx] = dmin[idx]
                  if idx == ncolors-2:
                        self.ColorList[idx+1,:] = array([rhigh[idx],ghigh[idx],bhigh[idx]])
                        self.ZValues[idx+1] = dmax[idx]
                  dmin[idx]
                  if idx and dmin[idx] != lastDmax:
                        raise GMTColormapException,'Input color map %s has non-contiguous Z data'
                  lastDmax = dmax[idx]
                  idx += 1
            #get the Z data min/max values
            zmin = self.ZValues.min()
            zmax = self.ZValues.max()
            #what is the _second_ largest value?
            # i = where(self.ZValues == oldzmax)
#             zdata = self.ZValues.copy()
#             zdata[i] = -1
#             zmax = zdata.max()
                        
            for i in range(0,ncolors):
                  if i == 0:
                        thisd = (dmin[i] - zmin)/(zmax - zmin)
                        red = (thisd,rlow[i],rlow[i])
                        green = (thisd,glow[i],glow[i])
                        blue = (thisd,blow[i],blow[i])
                  elif i == ncolors-1:
                        thisd = (dmax[i-1] - zmin)/(zmax - zmin)
                        red =   (thisd,rhigh[i-1],rhigh[i])
                        green = (thisd,ghigh[i-1],ghigh[i])
                        blue =  (thisd,bhigh[i-1],bhigh[i])
                  else:
                        thisd = (dmax[i-1] - zmin)/(zmax - zmin)
                        red =   (thisd,rhigh[i-1],rlow[i])
                        green = (thisd,ghigh[i-1],glow[i])
                        blue =  (thisd,bhigh[i-1],blow[i])

                  self.ColorDict['red'].append(red)
                  self.ColorDict['green'].append(green)
                  self.ColorDict['blue'].append(blue)
            

      def getColorList(self):
            return self.ColorList.copy()
      
      def getColorDict(self):
            return copy.copy(self.ColorDict)

      def getZValues(self):
            return copy.copy(self.ZValues)
      
      def getColor(self,value,hexcolor=False):
            rgb = None
            if value >= self.ZValues.max():
                  rgb = (self.ColorList[-1,0],self.ColorList[-1,1],self.ColorList[-1,2])

            if value <= self.ZValues.min():
                  rgb = (self.ColorList[0,0],self.ColorList[0,1],self.ColorList[0,2])
                  
            zdiff = self.ZValues - value
            imin = abs(zdiff).argmin()
            if zdiff[imin] == 0:
                  rgb = (self.ColorList[imin,0],self.ColorList[imin,1],self.ColorList[imin,2])
            if zdiff[imin] > 0:
                  imin = imin-1
            
            if rgb is None:
                  zmin = self.ZValues[imin]
                  zmax = self.ZValues[imin+1]
                  zfrac = (value-zmin)/(zmax-zmin)
                  rmin = self.ColorList[imin,0]
                  rmax = self.ColorList[imin+1,0]
                  gmin = self.ColorList[imin,1]
                  gmax = self.ColorList[imin+1,1]
                  bmin = self.ColorList[imin,2]
                  bmax = self.ColorList[imin+1,2]
                  rfrac = rmin + (rmax-rmin)*zfrac
                  gfrac = gmin + (gmax-gmin)*zfrac
                  bfrac = bmin + (bmax-bmin)*zfrac
                  rgb = (rfrac,gfrac,bfrac)
            
            if hexcolor:
                  red = hex(int(rgb[0]*255))[2:4]
                  green = hex(int(rgb[1]*255))[2:4]
                  blue = hex(int(rgb[2]*255))[2:4]
                  if len(red) == 1:
                        red = '0' + red
                  if len(green) == 1:
                        green = '0' + green
                  if len(blue) == 1:
                        blue = '0' + blue
                  return '#%s%s%s' % (red,green,blue)
            else:
                  return rgb
            
                  
                  
