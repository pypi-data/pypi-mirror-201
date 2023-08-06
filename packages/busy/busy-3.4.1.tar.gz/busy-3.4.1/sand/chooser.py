from busy.ui.ui import UI
from enum import Enum
E = Enum('E', ['YES','NO'])
c1 = UI.Chooser.Choice(keys=['y'], commands=['yes'], action=E.YES)
c2 = UI.Chooser.Choice(keys=['n'], commands=['no'], action=E.NO)
c = UI.Chooser([c1, c2])
