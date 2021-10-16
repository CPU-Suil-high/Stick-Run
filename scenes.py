from classes import *
from functions import *
from units import *

import sys
import msvcrt

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
    
    def switchScene(self, scene:"Scene"):
        self.nextScene = scene

    def stop(self):
        self.nextScene = None

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

        self.player = Player(self.grounds, self.screen.height*2, gravity=120, jumpForce=65)
        self.player.position = Vecotr(5, (self.screen.height - 8)*2)
        self.speed = 15

        self.healthBar = HealthBar(self.player, width=80, height=4)
        self.healthBar.position = Vecotr(2, 2)

        self.scoreNumber = Number(self.player.score)
        self.scoreNumber.position = Vecotr(self.screen.width - self.scoreNumber.width - 1, 2)

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
        self.scoreNumber.position = Vecotr(self.screen.width - self.scoreNumber.width - 1, 2)

        if (self.player.health <= 0):
            self.switchScene(StartScene(self.screen))
    
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
        self.screen.fillColor(textColor=Color.DEFAULT_TEXT_COLOR, backgroundColor=Color.DEFAULT_BACKGROUND_COLOR)

        for ground in self.grounds:
            ground.draw(self.screen, False)

        for item in self.items:
            item.draw(self.screen, False)
        
        for obstacle in self.obstacles:
            obstacle.draw(self.screen, False)

        self.player.draw(self.screen, False)

        self.healthBar.draw(self.screen, True)

        self.scoreNumber.draw(self.screen, True)

class StartScene(Scene):
    def __init__(self, screen: Surface) -> None:
        super().__init__(screen)

        self.title = Title()
        self.title.position = Vecotr(self.screen.width//2 - self.title.width//2, 4)

        self.buttons = []
        self.selectIndex = 0

        playButton = Button(self.play, width=10, name="Play")
        playButton.position = Vecotr(self.screen.width//2 - playButton.width//2, self.title.position.y + self.title.height + 15)
        self.buttons.append(playButton)

        optionButton = Button(lambda : None, width=10, name="Option")
        optionButton.position = Vecotr(self.screen.width//2 - optionButton.width//2, playButton.position.y + playButton.height + 6)
        self.buttons.append(optionButton)

        exitButton = Button(self.stop, width=10, name="Exit")
        exitButton.position = Vecotr(self.screen.width//2 - exitButton.width//2, optionButton.position.y + optionButton.height + 6)
        self.buttons.append(exitButton)

        self.buttons[0].select(True)
    
    def play(self):
        self.switchScene(RunningScene(self.screen))

    def update(self, deltaTime: float):
        pass

    def inputKey(self, deltaTime: float):
        while (msvcrt.kbhit()):
            key = msvcrt.getch()

            if (key == b"w" or key == b"W"):
                self.buttons[self.selectIndex].select(False)
                self.selectIndex -= 1
            elif (key == b"s" or key == b"S"):
                self.buttons[self.selectIndex].select(False)
                self.selectIndex += 1
            elif (key == b" "):
                self.buttons[self.selectIndex].click()
        
        self.selectIndex %= len(self.buttons)

        self.buttons[self.selectIndex].select(True)

    def render(self):
        self.screen.fill(" ")
        self.screen.fillColor(textColor=Color.DEFAULT_TEXT_COLOR, backgroundColor=Color.DEFAULT_BACKGROUND_COLOR)
        
        self.title.draw(self.screen, False)
        
        for button in self.buttons:
            button.draw(self.screen, False)