# -*- coding: utf-8 -*-
#
# archserv  parser for ArchServ surveilance data
# Copyright (C) 2014-2016  Bernhard Arnold <bernhard.arnold@cern.ch>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import re
from collections import namedtuple

__version__ = "0.1.0"
__all__ = ["ArchServ"]

RegExCode = re.compile(r'^(\d{4})([A-Z])(\d{2})(\d{3})$')
RegExPoint = re.compile(r'^([\w]{,10})\s+(\-?\d+\.\d+)\s+(\-?\d+\.\d+)\s+(\-?\d+\.\d+)(?:\s+(\w+))$')

Codes = {
    00: "Nail",
    01: "Height",
    11: "Point",
    02: "PolylineOpen",
    03: "PolylineClosed",
    04: "SplineOpen",
    05: "SplineClosed",
    06: "Circle",
    71: "Find",
    81: "ControlPoint",
    91: "FixedPoint",
    92: "BoundaryOpen",
    93: "BoundaryClosed",
}

class ArchServKey(object):
    """Encoded point key."""

    def __init__(self, stratum, group, code, index):
        self.stratum = int(stratum)
        self.group = group.upper()
        self.code = int(code)
        self.index = int(index)

    def tuple(self):
        return self.stratum, self.group, self.code, self.index

    def __lt__(self, other):
        """Sortable by attributes."""
        return self.tuple() < other.tuple()

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return "{stratum:04d}{group}{code:02d}{index:03d}".format(**self.__dict__)

class ArchServPoint(object):

    def __init__(self):
        self.key = ""
        self.x = 0.
        self.y = 0.
        self.z = 0.
        self.code = ""

    @property
    def xyz(self):
        """Returns tuple containing XYZ coordinates of point."""
        return self.x, self.y, self.z

    def parse(self, line):
        """Read point from line."""
        result = RegExPoint.match(line.strip())
        if not result:
            raise ValueError(line)
        self.key = result.group(1)
        self.x = float(result.group(2))
        self.y = float(result.group(3))
        self.z = float(result.group(4))
        self.code = result.group(5)
        # Convert key to object if encoded
        result = RegExCode.match(self.key)
        if result:
            self.key = ArchServKey(*result.groups())

    def __lt__(self, other):
        """Make sortable by point key."""
        return self.key < other.key

    def __repr__(self):
        return "{key}\t\t{x}\t{y}\t{z}\t{code}".format(**self.__dict__)

class ArchServ(object):
    """ArchServ format parser."""

    def __init__(self):
        self.points = []
        # Despite the points we collect also the used stations
        self.stations = []

    def read(self, fp):
        """Read from file stream."""
        for line in fp:
            point = ArchServPoint()
            point.parse(line)
            if isinstance(point.key, ArchServKey):
                self.points.append(point)
            else:
                self.stations.append(point)

    def features(self):
        features = {}
        for point in sorted(self.points):
            key = point.key.stratum, point.key.code
            group = point.key.group
            if key not in features:
                features[key] = {}
            if group not in features[key]:
                features[key][group] = []
            features[key][group].append(point)
        return features
