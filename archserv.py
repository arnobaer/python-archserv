# -*- coding: utf-8 -*-
#
# archserv  parser for ArchServ surveilance data
# Copyright (C) 2014-2018  Bernhard Arnold <bernhard.arnold@burgried.at>
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
"""Regular expression for point codes."""

RegExPoint = re.compile(r'^(\w+)\s+(\-?\d+\.\d+)\s+(\-?\d+\.\d+)\s+(\-?\d+\.\d+)(?:\s+(\w+))?$')
"""Regular expression for measured points. Both stations and measurements are
supported.

Station format: '<station> <x> <y> <z>'

Point format: '<key> <x> <y> <z> <code>'
"""

class Codes:
    Nail = 0
    Height = 1
    Point = 11
    PolylineOpen = 2
    PolylineClosed = 3
    SplineOpen = 4
    SplineClosed = 5
    Circle = 6
    Find = 71
    ControlPoint = 81
    FixedPoint = 91
    BoundaryOpen = 92
    BoundaryClosed = 93

PointTypes = (
    Codes.Nail,
    Codes.Height,
    Codes.Point,
    Codes.Circle,
    Codes.Find,
    Codes.ControlPoint,
    Codes.FixedPoint,
)

LineTypes = (
    Codes.PolylineOpen,
    Codes.SplineOpen,
    Codes.BoundaryOpen,
)

PolygonTypes = (
    Codes.PolylineClosed,
    Codes.SplineClosed,
    Codes.BoundaryClosed,
)

class Key(object):
    """Encoded point key."""

    def __init__(self, context, group, code, index):
        self.context = int(context)
        self.group = group.upper()
        self.code = int(code)
        self.index = int(index)

    def tuple(self):
        """Returns a sortable tuple."""
        return self.context, self.group, self.code, self.index

    def __lt__(self, other):
        """Sortable by attributes."""
        return self.tuple() < other.tuple()

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return "{context:04d}{group}{code:02d}{index:03d}".format(**self.__dict__)

class Point(object):

    def __init__(self):
        self.key = ""
        self.x = 0.
        self.y = 0.
        self.z = 0.
        self.code = ""
        self.is_station = False

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
        self.is_station = True
        # Convert key to object if encoded
        result = RegExCode.match(self.key)
        if result:
            self.key = Key(*result.groups())
            self.is_station = False

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
            # Clean input line from newlines
            line = line.strip()
            # Skip empty lines
            if not line:
                continue
            point = Point()
            point.parse(line)
            if point.is_station:
                self.stations.append(point)
            else:
                self.points.append(point)

    def features(self):
        features = {}
        for point in sorted(self.points):
            key = point.key.context, point.key.code
            group = point.key.group
            if key not in features:
                features[key] = {}
            if group not in features[key]:
                features[key][group] = []
            features[key][group].append(point)
        return features

def load(fp, crs=None):
    """Load data from iteratable and returns a GeoJSON FeatureCollection object."""
    pass

def loads(s, crs=None):
    """Load data from string and returns a GeoJSON FeatureCollection object."""
    pass
