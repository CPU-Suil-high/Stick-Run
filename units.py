import random
from typing import *
from classes import *
from functions import *

class Unit:
    def __init__(self, surface: Surface) -> None:
        self.surface = surface

        self.width = surface.width
        self.height = surface.height*2

        self.position = Vecotr()
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

class AnimationUnit(Unit):
    def __init__(self, surface: Surface, images: List[str], animationSpeed) -> None:
        super().__init__(surface)
        self.images = images
        self.imageIndex = 0
        self.maxImageIndex = len(self.images)
        self.animationSpeed = animationSpeed
    
    def update(self, deltaTime):
        super().update(deltaTime)
        self.animation(deltaTime)
    
    def animation(self, deltaTime):
        self.imageIndex += self.animationSpeed * deltaTime

        while (self.imageIndex >= self.maxImageIndex):
            self.imageIndex -= self.maxImageIndex
        
        self.surface.fill(" ")
        self.surface.setImage(self.images[int(self.imageIndex)])

class Player(AnimationUnit):
    def __init__(self, grounds: "List[Ground]", gravity: Vecotr = Vecotr(), jumpForce : float = 0, score: int=0) -> None:
        images = ["""\
 _O_\\   
\\ |   
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

        surface = Surface(6, 5)
        surface.setImage(images[0])

        animationSpeed = 4

        super().__init__(surface, images, animationSpeed)

        self.grounds = grounds

        self.gravity = gravity

        self.jumpForce = jumpForce
        self.jumpCount = 0
        self.maxJumpCount = 2

        self.score = score
    
    def update(self, deltaTime):
        super().update(deltaTime)
        self.velocity += self.gravity * deltaTime

        for ground in self.grounds:
            if (self.checkCollision(ground)):
                self.position.y = ground.position.y - self.height
                self.velocity = Vecotr(self.velocity.x, 0)
                self.jumpCount = self.maxJumpCount
        
        self.surface.setImage(f"{self.score}")
    
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

    def addScore(self, score: int):
        self.score += score
class Ground(Unit):
    def __init__(self, scene, patten: str="@", width: int=5, height: int=3) -> None:
        surface = Surface(width, height)
        super().__init__(surface)

        self.scene = scene
        self.grounds = scene.grounds

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

        self.grounds.append(ground)

        for i in range(1, ground.width, 3):
            coin = Coin(self.scene.player)
            coin.position = ground.position + Vecotr(i, -6)
            coin.velocity = self.velocity
            coin.imageIndex = (ground.width - i)*0.05
            self.scene.items.append(coin)

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

class Item(AnimationUnit):
    def __init__(self, surface: Surface, images: List[str], animationSpeed: int, player: Player, score: int=0) -> None:
        super().__init__(surface, images, animationSpeed)

        self.player = player
        self.score = score
    
    def update(self, deltaTime):
        super().update(deltaTime)

        if (self.checkCollision(self.player)):
            self.player.addScore(self.score)
            self.kill()

class Coin(Item):
    def __init__(self, player: Player) -> None:
        score = 1

        images = ["""\
$
"""]

        surface = Surface(1, 1)
        surface.setImage(images[0])

        animationSpeed = 0
        
        super().__init__(surface, images, animationSpeed, player, score=score)