from functions import Color
class Surface:
    def __init__(self, width:int, height:int) -> None:
        self.width = width
        self.height = height

        self.image = [[Char(b" ", False, False) for j in range(width)] for i in range(height)]
    
    def fill(self, char:str, x:int=0, y:int=0, width:int=-1, height:int=-1):
        if (len(char) != 1):
            raise "char's len must be 1"
        
        if (width < 0):
            width = self.width
        if (height < 0):
            height = self.height

        for i in range(y, self.height):
            if (i >= y + height):
                break
            for j in range(x, self.width):
                if (j >= x + width):
                    break
                self.image[i][j].byte = char.encode("cp949")
                self.image[i][j].start = False
                self.image[i][j].end = False
    
    def fillColor(self, textColor:Color, backgroundColor:Color, x:int=0, y:int=0, width:int=-1, height:int=-1):
        if (width < 0):
            width = self.width
        if (height < 0):
            height = self.height

        for i in range(y, self.height):
            if (i >= y + height):
                break
            for j in range(x, self.width):
                if (j >= x + width):
                    break
                self.image[i][j].textColor = textColor
                self.image[i][j].backgroundColor = backgroundColor

    def blit(self, surface, x:int, y:int, space:bool=True):
        for i in range(surface.height):
            if (y + i < 0):
                continue
            elif (y + i >= self.height):
                break

            for j in range(surface.width):
                if (x + j < 0 or (not space and surface.image[i][j].byte == b" ")):
                    continue
                elif (x + j >= self.width):
                    break
                
                self.image[y + i][x + j] = surface.image[i][j].clone()
    
    def setImage(self, string:str):
        image = []
        lst = string.split("\n")
        for i in range(len(lst)):
            image.append([])
            for j in range(len(lst[i])):
                byte = lst[i][j].encode("cp949")
                if (len(byte) == 1):
                    image[i].append(Char(byte, False, False))
                else:
                    image[i].append(Char(bytes([byte[0]]), True, False))
                    image[i].append(Char(bytes([byte[1]]), False, True))

        for i in range(self.height):
            if (len(image) <= i):
                break
            for j in range(self.width):
                if (len(image[i]) <= j):
                    break
                image[i][j].textColor = self.image[i][j].textColor
                image[i][j].backgroundColor = self.image[i][j].backgroundColor
                self.image[i][j] = image[i][j]
    
    def clone(self):
        surface = Surface(self.width, self.height)

        for i in range(self.height):
            for j in range(self.width):
                surface.image[i][j] = self.image[i][j].clone()
        
        return surface

class Char:
    def __init__(self, byte:bytes, start:bool = False, end:bool = False, textColor: Color=Color.DEFAULT_TEXT_COLOR, backgroundColor: Color=Color.DEFAULT_BACKGROUND_COLOR) -> None:
        if (len(byte) != 1):
            raise "byte'len must be 1"

        self.byte = byte
        self.start = start
        self.end = end

        self.textColor = textColor
        self.backgroundColor = backgroundColor
    
    def clone(self):
        return Char(self.byte, self.start, self.end, self.textColor, self.backgroundColor)
    
    def __eq__(self, other) -> bool:
        if (self.byte == other.byte and self.start == other.start and self.end == other.end and self.textColor == other.textColor and self.backgroundColor == other.backgroundColor):
            return True
        else:
            return False

class Vecotr:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vecotr(x, y)
    
    def __sub__(self, other):
        return self + -other
    
    def __mul__(self, n):
        x = self.x*n
        y = self.y*n
        return Vecotr(x, y)
    
    def __rmul__(self, n):
        x = self.x*n
        y = self.y*n
        return Vecotr(x, y)
    
    def __truediv__(self, n):
        x = self.x / n
        y = self.y / n
        return Vecotr(x, y)
    
    def __neg__(self):
        x = - self.x
        y = - self.y
        return Vecotr(x, y)
    
    def __getitem__(self, index):
        if (index == 0):
            return self.x
        elif (index == 1):
            return self.y
        else:
            raise StopIteration
        
    def __setitem__(self, index, value):
        if (index == 0):
            self.x = value
        elif (index == 1):
            self.y = value
        else:
            raise Exception
    
    def distance(self):
        return (self.x**2 + self.y**2)**0.5

    def normalize(self):
        return self / self.distance()