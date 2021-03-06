from math import pi, sin
import random
from Sand import TABLE_WIDTH, TABLE_LENGTH, LED_PERIOD
from dialog import DialogFloat
from palettes import palettes
from LedsBase import LedsBase
from ledable import Ledable

class Lighter(Ledable):
    """
        Create a light pattern similar to waves washing up on a beach.

        FIX: self.lights should be cleaned up and moved to an LED library
        FIX: lighting techniques should be moved to the LED library
    """

    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.editor = [
            DialogFloat("wpm",         "Wave Frequency",       units="per minute", default=30.0, min=0.1, max=90.0),
            DialogFloat("roughness",   "Water Roughness",      units="percent", default=40.0, min=0.0, max=100.0),
        ]

    def generator(self, leds, params):
        colors = palettes['Ocean'](params).getColors()
        width, length = TABLE_WIDTH, TABLE_LENGTH
        cols, rows = self.cols, self.rows
        self.lights = [
            # Physical light location           Led range                             Reference
            (((0.0, 0.0), (width, 0.0)),         (cols*2+rows-1, cols+rows)),       # Bottom
            (((width, 0.0), (width, length)),    (cols+rows-1, cols)),              # Right
            (((0.0, length), (width, length)),   (0, cols-1)),                      # Top
            (((0.0, 0.0), (0.0, length)),        (cols*2+rows, cols*2+rows*2-1)),   # Left
        ]

        wavesPerPeriod = (params.wpm / 60.0) * LED_PERIOD
        stepsPerWave = int(1.0 / wavesPerPeriod)
        anglePerStep = pi / stepsPerWave

        roughness = params.roughness * 0.01

        def cmp(a, b): return (a > b)-(a < b)
        while True:
            # set the various edges of the waves
            def makeColors(points): return [colors[random.randint(0, len(colors)-1)] for p in range(points)]
            lines = [[r, cmp(r[1], r[0]), makeColors(abs(r[0]-r[1])+1)] for l, r in self.lights]

            for step in range(stepsPerWave):
                leds.clear()
                distance = int(sin(step * anglePerStep) * (rows-1))
                for led in range(distance):
                    leds.set(lines[1][0][0] + lines[1][1] * led, lines[1][2][distance-led])
                    leds.set(lines[3][0][0] + lines[3][1] * led, lines[3][2][distance-led])

                # Bottom (Ocean)
                for led in range(abs(lines[0][0][0] - lines[0][0][1])):
                    leds.set(lines[0][0][0] + lines[0][1] * led, lines[0][2][led])

                # Top (Shore)
                percent = float(distance) / rows
                threshold = 0.75
                if percent > threshold:
                    for led, rgb in enumerate(self._dim(lines[0][2], (percent - threshold) / (1.0 - threshold))):
                        leds.set(lines[2][0][0] + lines[2][1] * led, rgb)

                for line in lines:
                    line[2] = self._scintilate(line[2], roughness)

                yield True

    def _scintilate(self, leds, roughness):
        return [LedsBase.RGBScintilate(rgb, roughness) for rgb in leds]

    def _dim(self, leds, percent):
        return [LedsBase.RGBDim(rgb, percent) for rgb in leds]
