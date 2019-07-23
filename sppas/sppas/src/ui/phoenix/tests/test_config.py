import wx
import sys
from os import path
PROGRAM = path.abspath(__file__)
SPPAS = path.dirname(path.dirname(path.dirname(path.dirname(path.dirname(PROGRAM)))))
sys.path.append(SPPAS)

from sppas.src.ui.phoenix.main_settings import WxAppSettings

app = wx.App()

settings = WxAppSettings()
print('Settings created.')
print(' FG color: ({:d}, {:d}, {:d})'.format(
    settings.fg_color.Red(),
    settings.fg_color.Green(),
    settings.fg_color.Blue()))

print('Fg color change:')
settings.set('fg_color', wx.Colour(0, 0, 128))
print(' New FG color: ({:d}, {:d}, {:d})'.format(
    settings.fg_color.Red(),
    settings.fg_color.Green(),
    settings.fg_color.Blue()))

print('Reset settings:')
settings.reset()
print(' FG color: ({:d}, {:d}, {:d})'.format(
    settings.fg_color.Red(),
    settings.fg_color.Green(),
    settings.fg_color.Blue()))
