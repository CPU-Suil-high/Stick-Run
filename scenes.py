from classes import *
from functions import *
from units import *

import sys

class Scene:
    def __init__(self, screen:Surface) -> None:
        self.screen = screen
        self.nextScene = self
    
    def update(self, deltaTime:float):
        pass

    def inputKey(self, deltaTime:float):
        pass

    def render(self):
        pass

    def killUnit(self, units):
        i = 0
        unitCount = len(units)
        while (i < unitCount):
            if (units[i].isKilled):
                unitCount -= 1
                units.pop(i)
            else:
                i += 1

class RunningScene(Scene):
    def __init__(self, screen: Surface) -> None:
        super().__init__(screen)

        self.grounds = []
        self.items = []
        self.obstacles = []

        self.player = Player(self.grounds, gravity=120, jumpForce=65)
        self.player.position = Vecotr(5, (self.screen.height - 8)*2)
        self.speed = 15

        self.healthBar = HealthBar(self.player, width=50, height=1)
        self.healthBar.position = Vecotr(2, 2)

        self.scoreNumber = Number(self.player.score)
        self.scoreNumber.position = Vecotr(self.screen.width - self.scoreNumber.width - 1, 0)

        ground = Ground(self, "[]", 58, 3)
        ground.position = Vecotr(0, (self.screen.height - ground.height//2 - 1) * 2)
        ground.velocity = Vecotr(-20, 0)

        self.grounds.append(ground)

    def update(self, deltaTime: float):
        self.player.update(deltaTime)
        
        for ground in self.grounds:
            ground.update(deltaTime)

            if (ground.position.x + ground.width < 0):
                ground.kill()
        
        for item in self.items:
            item.update(deltaTime)

            if (item.position.x + item.width < 0):
                item.kill()
        
        for obstacle in self.obstacles:
            obstacle.update(deltaTime)

            if (obstacle.position.x + obstacle.width < 0):
                obstacle.kill()

        self.killUnit(self.grounds)
        self.killUnit(self.items)

        self.healthBar.update(deltaTime)
        self.scoreNumber.setNumber(self.player.score)
        self.scoreNumber.position = Vecotr(self.screen.width - self.scoreNumber.width - 1, 0)
    
    def inputKey(self, deltaTime: float):
        if (getPressedKey(VirtualKey.RIGHT)):
            self.player.position.x += deltaTime * self.speed
        if (getPressedKey(VirtualKey.LEFT)):
            self.player.position.x -= deltaTime * self.speed
        if (getPressedKey(VirtualKey.DOWN)):
            self.player.position.y += deltaTime * self.speed
        if (getPressedKey(VirtualKey.UP)):
            self.player.position.y -= deltaTime * self.speed
        self.player.inputKey(deltaTime)
    
    def render(self):
        self.screen.fill(" ")

        for ground in self.grounds:
            ground.draw(self.screen, False)

        for item in self.items:
            item.draw(self.screen, False)
        
        for obstacle in self.obstacles:
            obstacle.draw(self.screen, False)

        self.player.draw(self.screen, False)

        self.healthBar.draw(self.screen, True)

        self.scoreNumber.draw(self.screen, True)

class TestScene(Scene):
    def __init__(self, screen: Surface) -> None:
        super().__init__(screen)
        surface = Surface(16, 4)
        surface.setImage("""\
┏━━━━━━┓
┃Hello, World┃
┃I have a pen┃
┗━━━━━━┛
\
""")
        self.aing = Unit(surface)

        surface = Surface(4, 4)
        surface.setImage("asdf\nasdf\nasdf\nasdf")
        self.sans = Unit(surface)
        self.sans.position = Vecotr(self.screen.width//2, self.screen.height//2)

        self.speed = 10

    def update(self, deltaTime:float):        
        self.sans.surface.setImage(f"{self.sans.position.x}\n{self.sans.position.y}\nasdf\nasdf")
        self.aing.surface.setImage(f"""\
┏━━━━━━┓
┃{self.sans.checkCollision(self.aing)}┃
┃{self.aing.position.x}┃
┗{self.aing.position.y}━━━━━━┛
\
""")

    def inputKey(self, deltaTime: float):
        if (getPressedKey(VirtualKey.RIGHT)):
            self.aing.position.x += deltaTime * self.speed
        if (getPressedKey(VirtualKey.LEFT)):
            self.aing.position.x -= deltaTime * self.speed
        if (getPressedKey(VirtualKey.DOWN)):
            self.aing.position.y += deltaTime * self.speed
        if (getPressedKey(VirtualKey.UP)):
            self.aing.position.y -= deltaTime * self.speed
    
    def render(self):
        self.screen.fill(" ")
        self.aing.draw(self.screen)
        self.sans.draw(self.screen)