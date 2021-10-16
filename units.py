import msvcrt
import random
from typing import *
from classes import *
from functions import *

numberImageDict = {
    "-":"""\
   
---
   
""",
    "0":"""\
 _  
/ \\
\\_/
""",
    "1":"""\
   
/| 
 | 
""",
    "2":"""\
__ 
 _)
/__
""",
    "3":"""\
__ 
 _)
__)
""",
    "4":"""\
   
|_|
  |
""",
    "5":"""\
 _ 
|_ 
 _)
""",
    "6":"""\
 _ 
/_ 
\_)
""",
    "7":"""\
___
  /
 / 
""",
    "8":"""\
 _ 
(_)
(_)
""",
    "9":"""\
 _
(_\\
 _/
""",
}

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

class Number(Unit):
    def __init__(self, number:int) -> None:
        surface = Surface(3, 3)
        super().__init__(surface)

        self.setNumber(number)
    
    def setNumber(self, number:int):
        if (type(number) != int):
            return

        numberString = str(number)
        strLen = len(numberString)
        self.surface = Surface(strLen*3, 3)

        self.width = self.surface.width
        self.height = self.surface.height*2

        tempSurface = Surface(3, 3)
        for i in range(strLen):
            image = numberImageDict[numberString[i]]
            tempSurface.setImage(image)
            self.surface.blit(tempSurface, x=i*3, y=0, space=True)

class AnimationUnit(Unit):
    def __init__(self, surface: Surface, surfaces: List[Surface], animationSpeed) -> None:
        super().__init__(surface)
        self.surfaces = surfaces
        self.surfaceIndex = 0
        self.maxSurfaceIndex = len(self.surfaces)
        self.animationSpeed = animationSpeed
    
    def update(self, deltaTime):
        super().update(deltaTime)
        self.animation(deltaTime)
    
    def animation(self, deltaTime):
        self.surfaceIndex += self.animationSpeed * deltaTime

        while (self.surfaceIndex >= self.maxSurfaceIndex):
            self.surfaceIndex -= self.maxSurfaceIndex
        
        self.surface = self.surfaces[int(self.surfaceIndex)].clone()

class Player(AnimationUnit):
    def __init__(self, grounds: "List[Ground]", maxYPos:int, maxHealth: int = 10, gravity: int = 0, maxJumpCount: int = 2, jumpForce : float = 0, maxInvulnerableTime: float = 2, score: int=0) -> None:
        surfaces = [Surface(6, 5) for _ in range(4)]
        surfaces[0].setImage("""\
 _O_\\   
\\ |   
  |    
 / \\
/   \\ 
""")
        surfaces[1].setImage("""\
  O    
 /|\\/   
 \\|    
  |\\     
 /  |   
""")
        surfaces[2].setImage("""\
  O    
  |__   
  |    
  |   
  |  
""")
        surfaces[3].setImage("""\
  O    
 /|\\/   
 \\|   
  |\\  
 /  |   
""")

        surface = Surface(6, 5)

        animationSpeed = 4

        super().__init__(surface, surfaces, animationSpeed)

        self.maxYPos = maxYPos

        self.grounds = grounds

        self.gravity = gravity

        self.jumpForce = jumpForce
        self.jumpCount = 0
        self.maxJumpCount = maxJumpCount

        self.score = score
        self.maxHealth = maxHealth
        self.health = maxHealth
        
        self.isInvulnerable = False
        self.maxInvulnerableTime = maxInvulnerableTime
        self.curInvulnerableTime = 0
    
    def update(self, deltaTime):
        super().update(deltaTime)
        self.velocity.y += self.gravity * deltaTime

        for ground in self.grounds:
            if (self.checkGroundCollision(ground)):
                self.position.y = ground.position.y - self.height
                self.velocity = Vecotr(self.velocity.x, 0)
                self.jumpCount = self.maxJumpCount

        self.updateInvulnerable(deltaTime)

        if (self.position.y >= self.maxYPos):
            self.velocity = Vecotr(0, -1) * self.jumpForce * 1.1
            self.jumpCount = self.maxJumpCount - 1

            self.addDamage(self.maxHealth//5)

    def inputKey(self, deltaTime):
        while (msvcrt.kbhit()):
            key = msvcrt.getch()
            if (key == b" "):
                self.jump()
    
    def updateInvulnerable(self, deltaTime):
        if (self.isInvulnerable):
            self.curInvulnerableTime += deltaTime

            if (self.curInvulnerableTime > self.maxInvulnerableTime):
                self.curInvulnerableTime = 0
                self.isInvulnerable = False
            elif (self.curInvulnerableTime < 0.3):
                self.surface.fillColor(Color.RED, Color.DEFAULT_BACKGROUND_COLOR)
            elif (self.curInvulnerableTime % 0.5 <= 0.25):
                self.surface.fillColor(Color.DARK_GRAY, Color.DEFAULT_BACKGROUND_COLOR)
            else:
                self.surface.fillColor(Color.WHITE, Color.DEFAULT_BACKGROUND_COLOR)

    def checkGroundCollision(self, ground: "Ground"):
        if (self.velocity.y < 0):
            return False

        surface = Surface(self.width, 1)
        playerBottomUnit = Unit(surface)
        playerBottomUnit.position = self.position + Vecotr(0, self.height - 2)

        surface = Surface(ground.width, 1)
        groundTopUnit = Unit(surface)
        groundTopUnit.position = ground.position

        return playerBottomUnit.checkCollision(groundTopUnit)

    def jump(self):
        if (self.jumpCount > 0):
            if (self.jumpCount == self.maxJumpCount):
                self.velocity = Vecotr(0, -1) * self.jumpForce
            else:
                self.velocity = Vecotr(0, -1) * self.jumpForce / 6 * 5
            self.jumpCount -= 1

    def addScore(self, score: int):
        self.score += score

    def addDamage(self, damage: int):
        if (self.isInvulnerable):
            return
        self.health -= damage
        
        if (self.health < 0):
            self.health = 0

        self.isInvulnerable = True

class HealthBar(Unit):
    def __init__(self, player:Player, width:int=10, height:int=4, followingSpeed:float=2, maxFollowingDelay:float=0.5) -> None:
        surface = Surface(width, height)
        super().__init__(surface)

        self.player = player

        self.slash = Unit(Surface(3, 3))
        self.slash.surface.setImage("""\
   
 / 
/  
""")    
        self.slash.position = Vecotr(self.width//2-self.slash.width//2 - 2, 0)

        self.maxHealthNumber = Number(self.player.maxHealth)
        self.maxHealthNumber.position = Vecotr(self.slash.position.x+self.slash.width, 0)

        self.healthNumber = Number(self.player.health)
        
        self.followingHealth = player.health

        self.followingSpeed = followingSpeed

        self.followingDelay = 0
        self.maxFollowingDelay = maxFollowingDelay

    def update(self, deltaTime):
        super().update(deltaTime)
        
        self.updateHealth(deltaTime)
    
    def updateHealth(self, deltaTime):

        if (self.player.health < self.followingHealth):
            if (self.followingDelay < self.maxFollowingDelay):
                self.followingDelay += deltaTime
            else:
                self.followingHealth -= deltaTime * self.followingSpeed
        else:
            self.followingHealth = self.player.health
            self.followingDelay = 0

        if (self.player.health < 0):
            width = 0
            followingWidth = 0
        else:
            width = int((self.player.health/self.player.maxHealth) * self.surface.width)
            followingWidth = int((self.followingHealth/self.player.maxHealth) * self.surface.width)

        self.surface.fill(" ")

        self.updateSurfaceHealth()

        self.surface.fillColor(Color.WHITE, Color.DARK_GRAY)
        self.surface.fillColor(Color.WHITE, Color.RED, x=0, y=0, width=followingWidth)
        self.surface.fillColor(Color.WHITE, Color.DARK_RED, x=0, y=0, width=width)

    def updateSurfaceHealth(self):
        self.healthNumber.setNumber(self.player.health)

        self.healthNumber.position = Vecotr(self.slash.position.x - self.healthNumber.width - 1, 0)

        self.surface.fill(" ")

        self.healthNumber.draw(self.surface)
        self.slash.draw(self.surface)
        self.maxHealthNumber.draw(self.surface)

class Ground(Unit):
    def __init__(self, scene, patten: str="@", width: int=5, height: int=3) -> None:
        surface = Surface(width, height)
        super().__init__(surface)

        self.scene = scene
        self.grounds = scene.grounds

        self.setPatten(patten)

        self.patten = patten

        self.surface.fillColor(Color.DARK_GREEN, Color.DEFAULT_BACKGROUND_COLOR, x=0, y=0, width=width, height=1)
        self.surface.fillColor(Color.DARK_YELLOW, Color.DEFAULT_BACKGROUND_COLOR, x=0, y=1, width=width, height=height-1)

        self.isWaitingToSummon = True
    
    def update(self, deltaTime):
        super().update(deltaTime)

        if (self.isWaitingToSummon and self.position.x < self.scene.screen.width):
            self.summonNextGround()

    def summonNextGround(self):
        ground = Ground(self.scene, self.patten, width=self.width, height=self.height//2)
        ground.position = self.position + Vecotr(self.width + random.randint(0, 1)*15, 0)
        ground.velocity = self.velocity

        self.grounds.append(ground)

        obstacleClass = random.choice((Tree, Stone))

        obstacle = obstacleClass(self.scene.player)

        obstacle.position = ground.position + Vecotr(ground.width/2 - obstacle.width/2, - obstacle.height)
        obstacle.velocity = self.velocity

        self.scene.obstacles.append(obstacle)

        for i in range(1, ground.width, 3):
            coin = Coin(self.scene.player)
            coin.position = ground.position + Vecotr(i, -6)
            
            if (coin.checkCollision(obstacle)):
                continue

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
                self.surface.image[j][i] = temp[i % tempCount].clone()

class Item(Unit):
    def __init__(self, surface: Surface, player: Player, score: int=0) -> None:
        super().__init__(surface)

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

        surface = Surface(1, 1)
        surface.setImage("$")
        surface.fillColor(Color.YELLOW, Color.DEFAULT_BACKGROUND_COLOR)
        
        super().__init__(surface, player, score=score)

class Obstacle(Unit):
    def __init__(self, surface: Surface, player: Player, damage: int = 0) -> None:
        super().__init__(surface)

        self.player = player
        self.damage = damage
    
    def update(self, deltaTime):
        super().update(deltaTime)
        
        if (self.checkCollision(self.player)):
            self.player.addDamage(self.damage)

class Stone(Obstacle):
    def __init__(self, player: Player) -> None:
        damage = 2

        surface = Surface(8, 3)

        surface.setImage("""\
   .-^\\
 _/  \\_\\
/  \\ / /
""")

        surface.fillColor(Color.DARK_GRAY, Color.DEFAULT_BACKGROUND_COLOR)

        super().__init__(surface, player, damage=damage)

class Tree(Obstacle):
    def __init__(self, player: Player) -> None:
        damage = 2

        surface = Surface(8, 8)

        surface.setImage("""\
 (￣￣)
/ ( ^) \\
 (_^ _)
   ||
   ||
   ||
   ||
   ||
""")
        surface.fillColor(Color.GREEN, Color.DEFAULT_BACKGROUND_COLOR, x=0, y=0, width=8, height=3)
        surface.fillColor(Color.DARK_YELLOW, Color.DEFAULT_BACKGROUND_COLOR, x=0, y=3, width=8, height=5)

        super().__init__(surface, player, damage=damage)

class Title(Unit):
    def __init__(self) -> None:
        surface = Surface(48, 6)

        surface.setImage("""\
  _____ _   _      _          _____             
 / ____| | (_)    | |        |  __ \            
| (___ | |_ _  ___| | __     | |__) |   _ _ __  
 \___ \| __| |/ __| |/ /     |  _  / | | | '_ \ 
 ____) | |_| | (__|   <      | | \ \ |_| | | | |
|_____/ \__|_|\___|_|\_\     |_|  \_\__,_|_| |_|
""")
        super().__init__(surface)

class Button(Unit):
    def __init__(self, func:Callable, args:List=[], width:int=10, name:str="button") -> None:
        surface = Surface(width, 1)
        super().__init__(surface)
        
        temp = Surface(len(name.encode("cp949")), 1)
        temp.setImage(name)
        self.surface.blit(temp, self.surface.width//2 - temp.width//2, 0)

        self.func = func
        self.args = args

    def select(self, isSelected:bool):
        if (isSelected):
            self.surface.fill("[", 0, 0, 1, 1)
            self.surface.fill("]", self.surface.width-1, 0, 1, 1)
        else:
            self.surface.fill(" ", 0, 0, 1, 1)
            self.surface.fill(" ", self.surface.width-1, 0, 1, 1)
    
    def click(self):
        self.func(*self.args)