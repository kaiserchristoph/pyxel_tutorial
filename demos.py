import pyxel
import math
import time
import random

WIDTH = 8*8
HEIGHT = 8*8

class Swirl:
    def __init__(self):
        self.timestep = 0
        self.parameter1 = 0
        
    def update(self):
        self.timestep = math.sin(time.time() / 18) * 1500
        self.parameter1 = pyxel.mouse_x / WIDTH

    def draw(self):
        pyxel.cls(0)
        for y in range(HEIGHT):
            for x in range(WIDTH):
                b = self.swirl(x, y, self.timestep) > 0.2
                if b:
                    col = random.randint(5, 6)
                    pyxel.pset(x, y, col)

        #pyxel.text(0, 0, f"p1 {self.parameter1}", 2)

    def swirl(self, x, y, step):
        x -= (WIDTH/2.0)
        y -= (HEIGHT/2.0)

        dist = math.sqrt(pow(x, 2) + pow(y, 2))

        angle = (step / 10.0) + dist / 1.5

        s = math.sin(angle)
        c = math.cos(angle)

        xs = x * c - y * s
        ys = x * s + y * c

        r = abs(xs + ys)

        val =  max(0.0, 0.7 - min(1.0, r/8.0))
        return val

class Plasma:
    def __init__(self):
        self.i = 0
        self.s = 1

    def update(self):
        self.i += 2
        self.s = math.sin(self.i / 100.0) * 2.0 + 6.0

    def draw(self):
        pyxel.cls(0)
        
        for y in range(HEIGHT):
            for x in range(WIDTH):
                b = self.handle_px(x, y)
                if b:
                    pyxel.pset(x, y, 6)

    def handle_px(self, x, y):
        v = 0.3 + (0.3 * math.sin((x * self.s) + self.i / 4.0) *
                   math.cos((y * self.s) + self.i / 4.0))
        return v > 0.3

class RotatingPlasma:
    def __init__(self):
        self.current = time.time()

    def update(self):
        self.current = time.time()

    def draw(self):
        pyxel.cls(0)

        for y in range(HEIGHT):
            for x in range(WIDTH):
                b = self.handle_px(x, y)
                col = int(b * 3)
                if b:
                    pyxel.pset(x, y, col)

    def handle_px(self, x, y):
        v = math.sin(1*(0.5*x*math.sin(self.current/2) +
                        0.5*y*math.cos(self.current/3)) + self.current)
        # -1 < sin() < +1
        # therfore correct the value and bring into range [0, 1]
        v = (v+1.0) / 2.0
        return v 


class PingPong:
    def __init__(self):
        self.vel = [1, 1]
        self.pos = [0, HEIGHT // 2]

    def handle_px(self, x, y):
        if x == self.pos[0] and y == self.pos[1]:
            return True
        else:
            return False

    def update(self):
        if self.pos[0] + self.vel[0] > WIDTH or \
                self.pos[0] + self.vel[0] < 0:
            self.vel[0] = -self.vel[0]

        if self.pos[1] + self.vel[1] > HEIGHT or \
                self.pos[1] + self.vel[1] < 0:
            self.vel[1] = -self.vel[1]

        self.pos = [self.pos[0] + self.vel[0],
                    self.pos[1] + self.vel[1]]

    def draw(self):
        pyxel.cls(0)
        for y in range(HEIGHT):
            for x in range(WIDTH):
                b = self.handle_px(x, y)
                if b:
                    pyxel.pset(x, y, 6)

class PerlinNoise:
    """
    Perlin noise demo.

    Inspired by https://github.com/kitao/pyxel/blob/main/python/pyxel/examples/12_perlin_noise.py
    """
    def __init__(self):
        self.parameter = 0

    def update(self):
        self.parameter = max(0.1, 10 * pyxel.mouse_x / WIDTH)

    def draw(self):
        pyxel.cls(0)
        for y in range(HEIGHT):
            for x in range(WIDTH):
                n = pyxel.noise(
                    x / self.parameter, # 10,
                    y / self.parameter, #10,
                    pyxel.frame_count / 40
                )

                # determine color based on noise value
                if n > 0.4: col = 7
                elif n > 0: col = 6
                elif n > -0.4: col = 12
                else: col = 0

                pyxel.pset(x, y, col)

class Moire:
    """
    Moire pattern demo.

    Inspired by https://seancode.com/demofx/
    """
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self):
        pyxel.cls(0)
        self.moire()

    def moire(self):
        t = time.time()

        # center of two circles
        cx1 = math.sin(t / 2) * WIDTH / 3 + WIDTH / 2
        cy1 = math.sin(t / 4) * HEIGHT / 3 + HEIGHT / 2
        cx2 = math.cos(t / 3) * WIDTH / 3 + WIDTH / 2
        cy2 = math.cos(t) * HEIGHT / 3 + HEIGHT / 2

        for y in range(HEIGHT):
            # calculate distance from center
            dy = (y - cy1) * (y - cy1)
            dy2 = (y - cy2) * (y - cy2)
            for x in range(WIDTH):
                # calculate distance from center
                dx = (x - cx1) * (x - cx1)
                dx2 = (x - cx2) * (x - cx2)

                # calculate distance between two points
                rt1 = int(math.sqrt(dx + dy))
                rt2 = int(math.sqrt(dx2 + dy2))

                # xor the two distances
                xor = rt1 ^ rt2

                shade = ((xor >> 4) & 1) * 3
                pyxel.pset(x, y, shade)

class DemoHandler:
    def __init__(self):
        self.timestep = 0
        self.current_demo = 0
        self.demos = [
            Swirl(), Plasma(), RotatingPlasma(), PingPong(), 
            PerlinNoise(), Moire()
        ]
        self.__txt_vis_counter = 100

        pyxel.init(WIDTH, HEIGHT)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_RIGHT, hold=10):
            self.current_demo += 1
            self.__txt_vis_counter = 100
            if self.current_demo >= len(self.demos):
                self.current_demo = 0

        self.__txt_vis_counter = max(0, self.__txt_vis_counter - 1)

        self.demos[self.current_demo].update()

    def draw(self):
        self.demos[self.current_demo].draw()

        if self.__txt_vis_counter > 0:
            demo = self.demos[self.current_demo]
            demo_name = demo.__class__.__name__
            pyxel.text(1, 1, f"{demo_name}", 3)


DemoHandler()
