#Maria Jose Castro Lemus 
#181202
#Graficas por Computadora - 10
#Lab 1: SR1 Point

import struct 
#from vertices import Obj


def char(c):
    return struct.pack('=c', c.encode('ascii'))
def word(c):
    return struct.pack('=h', c)
def dword(c):
    return struct.pack('=l', c)
def color(r, g, b):
    return bytes([b, g, r]) 


class Render(object):
    def __init__(self):
        #self.width = width
        #self.height = height
        self.framebuffer =[]
        #self.clear()
        #self.glCreateWindow()

    def glInit(self):
        pass

    def clear(self, r, g,b):
        self.framebuffer= [
        [color(r,g,b) for x in range(self.width)]
        for y in range(self.height)
        ]

    def  glClear(self):
        self.clear()

    def glClearcolor(self, r, g, b):
        r = round(r*255)
        g = round(g*255)
        b = round(b*255)
        self.clear(r, g, b)

    def glColor(self, r,g,b):
        r = round(r*255)
        g = round(g*255)
        b = round(b*255)
        return color(r, g, b)
        
    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        #r = Render(width,height)

    def glViewport(self, x, y, width, height):
        self.viewPortWidth = width
        self.viewPortHeight = height
        self.xViewPort = x
        self.yViewPort = y

    def glVertex(self, x,y):
        calcX = round((x+1)*(self.viewPortWidth/2)+self.xViewPort)
        calcY = round((y+1)*(self.viewPortHeight/2)+self.yViewPort)
        self.point(calcX, calcY)


    def write(self, filename):
        f = open(filename, 'bw')
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        #image header 
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        #pixel data
        for x in range(self.width):
            for y in range(self.height):
                    f.write(self.framebuffer[y][x])

        f.close()

    #function dot
    def point(self, x, y,color):
        self.framebuffer[x][y] = self.glColor(color[0], color[1], color[2])  

    def rellenito(self, poligono,color):
        lados = len(poligono)
        x_p=[]
        y_p=[]
        for i in range(len(poligono)):
            x_p.append(poligono[i][0])
            y_p.append(poligono[i][1])

        x_min= min(x_p)
        y_min= min(y_p)
        x_max= max(x_p)
        y_max= max(y_p)
        centro_x = round(x_min+(x_max-x_min)/2)
        centro_y = round(y_min+(y_max-y_min)/2)

        for i in range(len(poligono)):
            x0i= poligono[i][0]
            y0i= poligono[i][1]
            x1i= poligono[(i+1)% len(poligono)][0]
            y1i= poligono[(i+1)% len(poligono)][1]

            for valor in range (1, 1000): 
                x0 = round((x0i-centro_x)*(valor/1000))+centro_x
                y0 = round((y0i-centro_y)*(valor/1000))+centro_y
                x1 = round((x1i-centro_x)*(valor/1000))+centro_x
                y1 = round((y1i-centro_y)*(valor/1000))+centro_y

                dy = abs(y1 - y0)
                dx = abs(x1 - x0)

                steep = dy > dx

                if steep:
                  x0, y0 = y0, x0
                  x1, y1 = y1, x1

                if x0 > x1:
                  x0, x1 = x1, x0
                  y0, y1 = y1, y0

                dy = abs(y1 - y0)
                dx = abs(x1 - x0)

                offset = 0 
                threshold =  dx
                y = y0

                for x in range(x0, x1+1):
                  if steep:
                    r.point(y, x,color)

                  else:
                    r.point(x, y,color)

                  offset +=   2 * dy
                  if offset >=threshold:
                    y += 1 if y0 < y1 else -1
                    threshold +=  2 * dx
        
        #Referencia del repositorio ejemplo de dennis
    def glFinish(self, filename='out.bmp'):
        self.write(filename)
        try:
          from wand.image import Image
          from wand.display import display

          with Image(filename=filename) as image:
            display(image)
        except ImportError:
          pass  # do nothing if no wand is installed


r = Render()
r.glCreateWindow(800, 800)
r.glClearcolor(0.75, 0.25, 0.39)
r.rellenito([(165, 380), (185, 360), (180, 330), (207, 345), (233, 330), (230, 360), (250, 380), (220, 385), (205, 410), (193, 383)],[0,0,0])
r.rellenito([(321, 335), (288, 286), (339, 251), (374, 302)],[0,0,0])
r.rellenito([(377, 249), (411, 197), (436, 249)],[0,0,0])
r.rellenito([(413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37), (660, 52),(750, 145), (761, 179), (672, 192), (659, 214), (615, 214), (632, 230), (580, 230),(597, 215), (552, 214), (517, 144), (466, 180)],[0,0,0])
r.rellenito([(682, 175), (708, 120), (735, 148), (739, 170)],[0.75, 0.25, 0.39])
r.glFinish()