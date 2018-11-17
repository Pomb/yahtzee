from .command import command as cmd
from .command import diceCommand as dcmd
from .dice import d6Set
from .titleVisualizer import TitleVisualizer
import os


class Turn:
    def __init__(self, gameData):
        self.gameData = gameData
        self.header = TitleVisualizer("Rolling")
        self.diceSet = d6Set()
        self.maxRolls = 3

    def hasRolls(self):
        hasRoll = self.diceSet.rollCount < self.maxRolls
        if hasRoll:
            return self.hasDiceToHold()
        return hasRoll

    def hasDiceToHold(self):
        rollable = self.diceSet.getRollableDiceIndices()
        # print("rollable dice {}".format(rollable))
        return len(rollable) > 0

    def play(self):
        os.system("cls")
        print(self.header)
        print(self.diceSet)

        actions = {}
        actions["r"] = dcmd.RollCommand("Roll", self.diceSet)

        # can only hold once the first roll has been made
        if self.diceSet.rollCount > 0:
            actions["h"] = dcmd.HoldAllCommand("Hold all", self.diceSet)
            for i in range(len(self.diceSet.dice)):
                if self.diceSet.hold[i] is False:
                    actions[str(i + 1)] = dcmd.HoldCommand(
                        "Hold ", self.diceSet, i)

        actions["q"] = cmd.EndRoundCommand("Quit Round", self.gameData)

        actionPrompts = "\n"
        for key, value in actions.items():
            actionPrompts += ("\t{} - {}\n".format(key, value.title))

        actionChoice = input(actionPrompts)

        if actionChoice in actions:
            if actions[actionChoice].execute():
                print(self.diceSet)
        else:
            print("\ninvalid prompt, try again")

        if self.hasRolls() is False:
            # print("out of rolls")
            # self.gameData.player.waitForAnyKey()
            dcmd.HoldAllCommand("Finished rolling ", self.diceSet).execute()

    def chooseScore(self):
        os.system("cls")
        print(self.gameData.player.scoreSheet.header)
        print(self.diceSet)

        actions = {}
        for i, (key, value) in enumerate(
                self.gameData.player.scoreSheet.scores.items()):
            if value < 0:
                actions[str(i + 1)] = dcmd.ScoreCommand(
                    key, self.diceSet, self.gameData.player.scoreSheet, key)

        actionPrompts = "\n"
        for key, value in actions.items():
            actionPrompts += ("\t{} - {}\n".format(key, value.title))

        validChoice = False

        while not validChoice:
            scoreChoice = input(actionPrompts)
            if scoreChoice in actions:
                validChoice = actions[scoreChoice].execute()
            else:
                print("Invaild command, please try again")
