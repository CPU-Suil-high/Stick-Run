import random
from classes import *
from functions import *

class Unit:
    def __init__(self, scene, surface: Surface, x:int=0, y:int=0) -> None:
        self.scene = scene
        self.surface = surface

        self.width = surface.width
        self.height = surface.height*2

        self.position = Vecotr(x, y)
        self.velocity = Vecotr()

        self.isKilled = False
    
    def update(self, deltaTime):
        self.position += self.velocity * deltaTime

    def inputKey(self, deltaTime):
        pass

    def kill(self):
        self.isKilled = True
    
    def draw(self, screen:Surface, space:bool=True):
        screen.blit(self.surface, round(self.position.x), round(self.position.y/2), space)
    
    def checkCollision(self, unit) -> bool:
        left = self.position.x
        right = self.position.x + self.width
        top = self.position.y
        bottom = self.position.y + self.height

        otherLeft = unit.position.x
        otherRight = unit.position.x + unit.width
        otherTop = unit.position.y
        otherBottom = unit.position.y + unit.height

        if ((left <= otherLeft < right or otherLeft <= left < otherRight) and (top <= otherTop < bottom or otherTop <= top < otherBottom)):
            return True
        else:
            return False

class Player(Unit):
    def __init__(self, scene, x: int = 0, y: int = 0, gravity: Vecotr = Vecotr(), jumpForce : float = 0) -> None:
        surface = Surface(7, 5)
        surface.setImage("""\
   O
  /|/
  \\|
  / \\
 /   \\
""")
        super().__init__(scene, surface, x=x, y=y)

        self.images = ["""\
   O  \\   
\\￣|￣   
   |    
  / \\
 /   \\ 
""", """\
   O    
  /|\\/   
  \\|    
   |\\     
  /  |   
""", """\
   O    
   |__   
   |    
   |   
   |  
""", """\
   O    
  /|\\/   
  \\|   
   |\\  
  /  |   
"""]
        self.imageIndex = 0
        self.maxImageIndex = len(self.images)
        self.animationSpeed = 4

        self.gravity = gravity

        self.jumpForce = jumpForce
        self.jumpCount = 0
        self.maxJumpCount = 2
    
    def update(self, deltaTime):
        super().update(deltaTime)
        self.velocity += self.gravity * deltaTime

        for ground in self.scene.grounds:
            if (self.checkCollision(ground)):
                self.position.y = ground.position.y - self.height
                self.velocity = Vecotr(self.velocity.x, 0)
                self.jumpCount = self.maxJumpCount
        
        self.animation(deltaTime)
        self.surface.setImage(f"{len(self.scene.grounds)}")
    
    def inputKey(self, deltaTime):
        state = getAsyncKeyState(VirtualKey.SPACE)

        if (getAsyncKeyState(VirtualKey.SPACE) & 0x8000 and not self.space):
            self.jump()

        if (state == 0):
            self.space = False
        else:
            self.space = True
    
    def jump(self):
        if (self.jumpCount > 0):
            self.velocity = Vecotr(0, -1) * self.jumpForce
            self.jumpCount -= 1
    
    def animation(self, deltaTime):
        self.imageIndex += self.animationSpeed * deltaTime

        if (self.imageIndex >= self.maxImageIndex):
            self.imageIndex -= self.maxImageIndex
        
        self.surface.setImage(self.images[int(self.imageIndex)])

class Ground(Unit):
    def __init__(self, scene, patten: str="@", width: int=5, height: int=3, x: int = 0, y: int = 0) -> None:
        surface = Surface(width, height)
        super().__init__(scene, surface, x=x, y=y)

        self.setPatten(patten)

        self.patten = patten

        self.isWaitingToSummon = True
    
    def update(self, deltaTime):
        super().update(deltaTime)

        if (self.isWaitingToSummon and self.position.x < self.scene.screen.width):
            self.summonNextGround()

        if (self.position.x + self.width < 0):
            self.kill()

    def summonNextGround(self):
        ground = Ground(self.scene, self.patten, width=self.width, height=self.height//2)
        ground.position = self.position + Vecotr(self.width + random.randint(0, 1)*15, 0)
        ground.velocity = self.velocity

        self.scene.grounds.append(ground)

        self.isWaitingToSummon = False

    def setPatten(self, patten :str):
        temp = []

        for i in range(len(patten)):
            byte = patten[i].encode("cp949")
            if (len(byte) == 1):
                temp.append(Char(byte, False, False))
            else:
                temp.append(Char(bytes([byte[0]]), True, False))
                temp.append(Char(bytes([byte[1]]), False, True))

        tempCount = len(temp)

        for i in range(self.width):
            for j in range(self.height//2):
                self.surface.image[j][i] = temp[i % tempCount]