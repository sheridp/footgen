#!/usr/bin/python
# footgen.py
# Copyright (C) 2005-2007 Darrell Harmon
# Generates footprints for PCB from text description
# The GPL applies only to the python scripts.
# the output of the program and the footprint definition files
# are public domain
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

class Generator():
    def __init__(self, part): # part name
        self.options = "" # "cir" circle pad (BGA) "round" rounded corners "bottom" on bottom of board
        self.diameter = 1 # used for circular pads, mm
        self.width = 1 # pad x dimension or silk width
        self.height = 1 # pad y dimension
        self.drill = 0 # drill diameter
        self.angle = 0 # rotation - only kicad
        self.clearance = 0.2
        self.silkwidth = 0.15
        self.mask_clearance = 0.075
        self.part = part
        refdesy = 0
        refdesx = 0
        self.fp = "Element[\"\" \"%s\" \"Name\" \"Val\" 1000 1000 %dnm %dnm 0 100 \"\"]\n(\n" % (part, self.mm_to_geda(refdesx), self.mm_to_geda(-1.0 - refdesy))
        return
    def mm_to_geda(self,mm):
        return int(round(mm * 1.0e6))
    def add_pad(self, x, y, name):
        if (self.options.find("round") != -1) | (self.options.find("cir") != -1):
            flags = ""
        else:
            flags = "square"
        if self.drill > 0:
            self.fp += "\tPin[ %dnm %dnm %dnm %dnm %dnm %dnm \"%s\" \"%s\" \"%s\"]\n" % (self.mm_to_geda(x),self.mm_to_geda(y),self.mm_to_geda(self.diameter),\
                                                                                         self.mm_to_geda(self.clearance*2),\
                                                                                         self.mm_to_geda(self.mask_clearance+self.diameter),\
                                                                                         self.mm_to_geda(self.drill),name,name,flags)
            return
        linewidth = min(self.height,self.width)
        linelength = abs(self.height-self.width)
        if self.height>self.width:
        #vertcal pad
            x1 = x
            x2 = x
            y1 = y - linelength/2
            y2 = y + linelength/2
        else:
        #horizontal pad
            x1 = x - linelength/2
            x2 = x + linelength/2
            y1 = y
            y2 = y
        self.fp += "\tPad[%dnm %dnm %dnm %dnm %dnm %dnm %dnm \"%s\" \"%s\" \"%s\"]\n"\
            % (self.mm_to_geda(x1), self.mm_to_geda(y1), self.mm_to_geda(x2), self.mm_to_geda(y2),\
                   self.mm_to_geda(linewidth), self.mm_to_geda(self.clearance*2), self.mm_to_geda(self.mask_clearance+linewidth), name, name, flags)
    # draw silkscreen line
    def silk_line(self, x1, y1, x2, y2):
        self.fp += "\tElementLine [%dnm %dnm %dnm %dnm %dnm]\n" % (self.mm_to_geda(x1), self.mm_to_geda(y1),\
                                                                       self.mm_to_geda(x2), self.mm_to_geda(y2), self.mm_to_geda(self.silkwidth))
    def finish(self):
        self.fp += ")\n"
        return self.fp
