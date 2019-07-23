#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# ---------------------------------------------------------------------------
#            ___   __    __    __    ___
#           /     |  \  |  \  |  \  /              Automatic
#           \__   |__/  |__/  |___| \__             Annotation
#              \  |     |     |   |    \             of
#           ___/  |     |     |   | ___/              Speech
#
#
#                           http://www.sppas.org/
#
# ---------------------------------------------------------------------------
#            Laboratoire Parole et Langage, Aix-en-Provence, France
#                   Copyright (C) 2011-2016  Brigitte Bigi
#
#                   This banner notice must not be removed
# ---------------------------------------------------------------------------
# Use of this software is governed by the GNU Public License, version 3.
#
# SPPAS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SPPAS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SPPAS. If not, see <http://www.gnu.org/licenses/>.
#
# ---------------------------------------------------------------------------
# File: imageutils.py
# ----------------------------------------------------------------------------

__docformat__ = """epytext"""
__authors__   = """Brigitte Bigi"""
__copyright__ = """Copyright (C) 2011-2015  Brigitte Bigi"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

import os
import os.path
import sys
import wx
import math
import random

from sppas.src.config import paths
from sppas.src.ui.wxgui.sp_icons import THEME_DEFAULT
from sppas.src.ui.wxgui.sp_icons import CHECKED_ICON, ACTIVATED_ICON, RADIOCHECKED_ICON
from sppas.src.ui.wxgui.sp_icons import UNCHECKED_ICON, DISABLED_ICON, RADIOUNCHECKED_ICON

# ----------------------------------------------------------------------------


def TakeScreenShot(rect, client_x=0, client_y=0):
    """Takes a screenshot of the given pos & size (rect)."""

    # adjust widths for Linux
    if sys.platform == 'linux2':
        border_width = client_x - rect.x
        title_bar_height = client_y - rect.y
        rect.width  += (border_width * 2)
        rect.height += title_bar_height + border_width

    # Create a DC for the whole screen area
    dcScreen = wx.ScreenDC()

    # Create a Bitmap that will hold the screenshot image later on
    bmp = wx.EmptyBitmap(rect.width, rect.height)

    # Create a memory DC that will be used for actually taking the
    # screenshot
    memDC = wx.MemoryDC()

    # Tell the memory DC to use our Bitmap
    # all drawing action on the memory DC will go to the Bitmap now
    memDC.SelectObject(bmp)

    # Blit (in this case copy) the actual screen on the memory DC
    # and thus the Bitmap
    memDC.Blit( 0, #Copy to this X coordinate
                0, #Copy to this Y coordinate
                rect.width, #Copy this width
                rect.height, #Copy this height
                dcScreen, #From where do we copy?
                rect.x, #What's the X offset in the original DC?
                rect.y  #What's the Y offset in the original DC?
                )

    # Select the Bitmap out of the memory DC by selecting a new
    # uninitialized Bitmap
    memDC.SelectObject(wx.NullBitmap)

    return bmp.ConvertToImage()

#-----------------------------------------------------------------------------


def CreateCursorFromXPMData( xpmdata, hotspot ):
    """Return a wx.Cursor from a vectorized image."""

    # get cursor image
    bmp   = wx.BitmapFromXPMData( xpmdata )
    image = wx.ImageFromBitmap( bmp )

    # since this image didn't come from a .cur file,
    # tell it where the hotspot is
    image.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_X, hotspot)
    image.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, hotspot)

    # make the image into a cursor
    return wx.CursorFromImage( image )

# ----------------------------------------------------------------------------


def ScaleBitmap(bitmap, width, height):
    """Scale the bitmap image."""

    image = wx.ImageFromBitmap(bitmap)
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    return wx.BitmapFromImage(image)

# -----------------------------------------------------------------------


def ScaleImage(img, width, height):
    """Scale the image."""

    return img.Scale(width, height, wx.IMAGE_QUALITY_HIGH)

# -----------------------------------------------------------------------


def RotateImage(bmp):
    """Rotates the bitmap."""

    w,h = bmp.GetWidth(), bmp.GetHeight()
    wcenter = int(w/2)
    hcenter = int(h/2)

    return bmp.Rotate(math.pi, (wcenter, hcenter), True)

# -----------------------------------------------------------------------


def GrayOut(anImage):
    """
    Convert the given image (in place) to a grayed-out version,
    appropriate for a 'disabled' appearance.

    """
    factor = 0.7        # 0 < f < 1.  Higher Is Grayer

    if anImage.HasMask():
        maskColor = (anImage.GetMaskRed(), anImage.GetMaskGreen(), anImage.GetMaskBlue())
    else:
        maskColor = None

    data = map(ord, list(anImage.GetData()))

    for i in range(0, len(data), 3):

        pixel = MakeGray(data[i], data[i+1], data[i+2], factor, maskColor)

        for x in range(3):
            data[i+x] = pixel[x]

    anImage.SetData(''.join(map(chr, data)))

    return anImage

# -----------------------------------------------------------------------


def MakeGray(r,g,b, factor, maskColor):
    """
    Make a pixel grayed-out. If the pixel matches the maskcolor, it won't be
    changed.

    """
    if (r,g,b) != maskColor:
        return map(lambda x: int((230 - x) * factor) + x, (r,g,b))
    else:
        return (r, g, b)

# -----------------------------------------------------------------------


def get_img_file(id, theme=None):
    """
    Get the bitmap file name from its identifier.

    @param id is the key of a bitmap (see sp_icons.py)
    @param size (int)
    @param theme (string) is the icons theme name - default is 'Oxygen'

    """
    if theme is not None:
        bmpdir = os.path.join(paths.etc, "icons", theme)
        if not os.path.exists(bmpdir):
            theme = None

    if theme is None:
        bmpdir = os.path.join(paths.etc, "icons", THEME_DEFAULT)

    bmpfile = os.path.join(bmpdir, id)

    # if the icon is missing in the style, use the default style.
    if not os.path.exists(bmpfile):
        bmpfile = os.path.join(paths.etc, "icons", THEME_DEFAULT, id)
        if not os.path.exists(bmpfile):
            return os.path.join(paths.etc, "icons", THEME_DEFAULT, "actions", "missing.png")

    return bmpfile

# ----------------------------------------------------------------------------


def spBitmap(idb, size=None, theme=None):
    """
    Get the bitmap from its identifier.

    @param idb is the identifier of a bitmap (see sp_icons.py)
    @param size (int)
    @param theme (string) is the icons theme name

    @return wx.Bitmap

    """
    img = wx.Image( get_img_file( idb, theme ), wx.BITMAP_TYPE_ANY)

    if size is not None:
        img = ScaleImage(img, size, size)

    return wx.BitmapFromImage( img )

# ----------------------------------------------------------------------------


def GetBitmap(bmppath, pattern, ext):
    """
    Get a random bitmap in a directory.

    @param bmppath (string) Path to get a bitmap.
    @param pattern (string) Pattern included in the file name
    @param ext (string) extension of the file.

    @return filename of the selected bitmap image

    """
    tipsbmp = [f for f in os.listdir(bmppath) if pattern in f and f.endswith(ext)]
    return os.path.join(bmppath,random.choice(tipsbmp))

# ----------------------------------------------------------------------------


def GetCheckedBitmap( CCB_TYPE="check" ):
    """
    Return a bitmap representing "check".

    """
    return wx.BitmapFromImage(GetCheckedImage(CCB_TYPE))


def GetCheckedImage( CCB_TYPE="check" ):
    """
    Return a 16x16 image representing "check".

    """
    if CCB_TYPE == "radiocheck":
        img = wx.Image(get_img_file(RADIOCHECKED_ICON), wx.BITMAP_TYPE_PNG)
        return ScaleImage(img, 16, 16)

    if CCB_TYPE == "activecheck":
        img = wx.Image(get_img_file(ACTIVATED_ICON), wx.BITMAP_TYPE_PNG)
        return ScaleImage(img, 32, 24)

    img = wx.Image(get_img_file(CHECKED_ICON), wx.BITMAP_TYPE_PNG)
    return ScaleImage(img, 16, 16)

#----------------------------------------------------------------------


def GetNotCheckedBitmap( CCB_TYPE="check" ):
    """
    Return a bitmap representing "uncheck".
    """
    return wx.BitmapFromImage(GetNotCheckedImage(CCB_TYPE))


def GetNotCheckedImage( CCB_TYPE="check" ):
    """
    Return an image representing "uncheck".

    """
    if CCB_TYPE == "radiocheck":
        img = wx.Image(get_img_file(RADIOUNCHECKED_ICON), wx.BITMAP_TYPE_PNG)
        return ScaleImage(img, 16, 16)

    if CCB_TYPE == "activecheck":
        img = wx.Image(get_img_file(DISABLED_ICON), wx.BITMAP_TYPE_PNG)
        return ScaleImage(img, 32, 24)

    img = wx.Image(get_img_file(UNCHECKED_ICON), wx.BITMAP_TYPE_PNG)
    return ScaleImage(img, 16, 16)
