import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class FitChangeProjectedFighterAmountCommand(wx.Command):

    def __init__(self, fitID, position, amount):
        wx.Command.__init__(self, True, 'Change Projected Fighter Amount')
        self.fitID = fitID
        self.position = position
        self.amount = amount
        self.savedAmount = None

    def Do(self):
        pyfalog.debug('Doing change of projected fighter amount to {} at position {} on fit {}'.format(self.amount, self.position, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        fighter = fit.projectedFighters[self.position]
        if self.amount == fighter.amount or self.amount == fighter.amountActive:
            return False
        self.savedAmount = fighter.amount
        if self.amount == -1:
            fighter.amount = self.amount
            eos.db.commit()
            return True
        else:
            fighter.amount = max(min(self.amount, fighter.fighterSquadronMaxSize), 0)
            eos.db.commit()
            return True

    def Undo(self):
        pyfalog.debug('Undoing change of projected fighter amount to {} at position {} on fit {}'.format(self.amount, self.position, self.fitID))
        cmd = FitChangeProjectedFighterAmountCommand(fitID=self.fitID, position=self.position, amount=self.savedAmount)
        return cmd.Do()
