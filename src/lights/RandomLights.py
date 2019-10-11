from random import randint
from Sand import *
from dialog import *
from time import time
from ledstuff import *

class RandomLights( Ledable ):
    def __init__( self, cols, rows ):
        self.editor = [
                DialogFloat( "minutes",      "Light Pattern Change Frequency",   units = "minutes", default = 1.0, min = 0.25, max = 10.0 ),
        ]
        self.patterns = filter( lambda c: c not in ['Random','Off'], ledPatterns )

    def generator( self, leds, cols, rows, params ):
        while True:
            pattern = self.patterns[ randint(0,len(self.patterns)-1) ]
            pat = ledPatternFactory( pattern )

            iParams = Params(pat.editor)
            iParams.randomize(pat.editor)
            gen = pat.generator( leds, cols, rows, iParams )
            endTime = time() + params.minutes * 60.0
            try:
                while time() < endTime:
                    yield gen.next()
            except StopIteration:
                pass

