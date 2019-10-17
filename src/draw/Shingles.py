from math import radians, sin
from Sand import *
from dialog import *
    
class Sander( Sandable ):
    """
### Draw a pattern that looks like roofing shingles

#### Hints

This is a pretty boring pattern. Try something more fun.

#### Parameters

* **Shingle Height** - the height of each individual shingle.
* **X and Y Origin** - lower left corner of the drawing. Usually not worth changing.
* **Width** and **Length** - how big the figure should be. Probably not worth changing.
"""

    def __init__( self, width, length ):
        self.editor = [
            DialogFloat( "sHeight",         "Shingle Height",       units = "inches", default = 2.0, min = 0.1, max = length ),
            DialogBreak(),
            DialogFloat( "xOffset",         "X Origin",             units = "inches", default = 0.0 ),
            DialogFloat( "yOffset",         "Y Origin",             units = "inches", default = 0.0 ),
            DialogFloat( "width",           "Width (x)",            units = "inches", default = width ),
            DialogFloat( "length",          "Length (y)",           units = "inches", default = length ),
        ]

    def generate( self, params ):
        pointsPerShingle = 11
        yScale = params.sHeight
        lines = int(params.length / yScale)
        shingles    = params.width / params.sHeight
        pointCount  = int( shingles * pointsPerShingle )
        xScale      = params.width / pointCount
        angleMult   = 90.0 / pointsPerShingle
        
        chain = []
        points = list(range( pointCount))
        for line in range( lines ):
            yOffset = params.yOffset + line * yScale
            offset = (line % 2) * 90.0
            for point in points:
                angle = radians( offset + (point * angleMult) )
                x = params.xOffset + (point * xScale)
                y = yOffset + (abs( sin( angle )) * yScale)
                chain.append( (x, y))
            points.reverse()

        return [chain]
