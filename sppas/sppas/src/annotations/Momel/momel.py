# -*- coding: UTF-8 -*-
"""
    ..
        ---------------------------------------------------------------------
         ___   __    __    __    ___
        /     |  \  |  \  |  \  /              the automatic
        \__   |__/  |__/  |___| \__             annotation and
           \  |     |     |   |    \             analysis
        ___/  |     |     |   | ___/              of speech

        http://www.sppas.org/

        Use of this software is governed by the GNU Public License, version 3.

        SPPAS is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        SPPAS is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with SPPAS. If not, see <http://www.gnu.org/licenses/>.

        This banner notice must not be removed.

        ---------------------------------------------------------------------

    src.annotations.Momel.momel.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    https://en.wikipedia.org/wiki/Momel

    Different versions of the Momel algorithm have been developed
    in the LPL in Aix en Provence over the last twenty years and have been
    used for the phonetic modelling and symbolic coding of the intonation
    patterns of a number of languages (including English, French, Italian,
    Catalan, etc).

    The last implementation is presented as a Praat plugin. The modelling
    and coding algorithms have been implemented as a set of Praat scripts,
    each corresponding to a specific step in the process.

    See:
        | Hirst, Daniel. (2007).
        | A Praat plugin for Momel and INTSINT with improved algorithms
        | for modelling and coding intonation.
        | Proceedings of the 16th International Congress of Phonetic Sciences.


    The quality of the F0 modelling crucially depends on the quality of
    the F0 detected.

    The quadratic spline function used to model the macro-melodic component
    is defined by a sequence of target points, (couples <s, Hz>) each pair
    of which is linked by two monotonic parabolic curves with the spline
    knot occurring (by default) at the midway point between the two targets.
    The first derivative of the curve thus defined is zero at each target
    point and the two parabolas have the same value and same derivative at
    the spline knot. This, in fact, defines the most simple mathematical
    function for which the curves are both continuous and smooth.

"""
import math

from .anchor import Anchor
from .momelutil import quicksortcib

# ----------------------------------------------------------------------------


class Momel(object):
    """Implements Momel.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi

    """

    def __init__(self):
        """Create a new Momel instance."""
        # Constants
        self.SEUILV = 50.
        self.FSIGMA = 1.
        self.HALO_BORNE_TRAME = 4
        self.RAPP_GLITCH = 0.05
        self.ELIM_GLITCH = True

        # Array of pitch values
        self.hzptr = []
        self.nval = 0
        self.delta = 0.01

        # Output of cible:
        self.cib = []
        # Output of reduc:
        self.cibred = []
        # Output of reduc2:
        self.cibred2 = []

        # cible window length (lfen1 est en pointes echantillon,
        # pas milliseconds)
        self.lfen1 = 30
        # f0 threshold
        self.hzinf = 50
        # f0 ceiling (Hirst, Di Cristo et Espesser :
        # hzsup est calcule automatiquement)
        self.hzsup = 600
        # maximum error (Maxec est 1+Delta en Hirst, Di Cristo et Espesser)
        self.maxec = 1.04
        # reduc window length (lfen2 est en pointes echantillon,
        # pas milliseconds)
        self.lfen2 = 20
        # minimal distance (seuildiff_x est en pointes echantillon,
        # pas milliseconds)
        self.seuildiff_x = 5
        # minimal frequency ratio
        self.seuilrapp_y = 0.05

        self.a0 = 0
        self.a1 = 0
        self.a2 = 0

    # -------------------------------------------------------------------

    def initialize(self):
        """Set some variables to their default values."""
        # Array of pitch values
        self.hzptr = []
        self.nval = 0
        self.delta = 0.01

        # Output of cible:
        self.cib = []
        # Output of reduc:
        self.cibred = []
        # Output of reduc2:
        self.cibred2 = []

    # -------------------------------------------------------------------

    def set_pitch_array(self, arrayvals):
        self.hzptr = arrayvals
        self.nval = len(self.hzptr)

    def set_option_elim_glitch(self, activate=True):
        self.ELIM_GLITCH = activate

    def set_option_win1(self, val):
        self.lfen1 = val
        assert(self.lfen1 > 0)

    def set_option_lo(self, val):
        self.hzinf = val

    def set_option_hi(self, val):
        self.hzsup = val

    def set_option_maxerr(self, val):
        self.maxec = val

    def set_option_win2(self, val):
        self.lfen2 = val

    def set_option_mind(self, val):
        self.seuildiff_x = val

    def set_option_minr(self, val):
        self.seuilrapp_y = val

    # ------------------------------------------------------------------

    def elim_glitch(self):
        """Eliminate Glitch of the pitch values array.

        Set a current pith value to 0 if left and right values
        are greater than 5% more than the current value.

        """
        _delta = 1.0 + self.RAPP_GLITCH
        for i in range(1, self.nval-1):
            cur = self.hzptr[i]
            gprec = self.hzptr[i-1] * _delta
            gnext = self.hzptr[i+1] * _delta
            if cur > gprec and cur > gnext:
                self.hzptr[i] = 0.

    # ------------------------------------------------------------------

    def calcrgp(self, pond, dpx, fpx):
        """From inputs, estimates: a0, a1, a2.

        :param pond:
        :param dpx:
        :param fpx:

        """
        pn = 0.
        sx = sx2 = sx3 = sx4 = sy = sxy = sx2y = 0.
        for ix in range(dpx, fpx+1):
            p = pond[ix]
            if p != 0.:
                val_ix = float(ix)
                y = self.hzptr[ix]
                x2 = val_ix * val_ix
                x3 = x2 * val_ix
                x4 = x2 * x2
                xy = val_ix * y
                x2y = x2 * y

                pn = pn + p
                sx += (p * val_ix)
                sx2 += (p * x2)
                sx3 += (p * x3)
                sx4 += (p * x4)
                sy += (p * y)
                sxy += (p * xy)
                sx2y += (p * x2y)

        if pn < 3.:
            raise ValueError('pn < 3')

        spdxy = sxy - (sx * sy) / pn
        spdx2 = sx2 - (sx * sx) / pn
        spdx3 = sx3 - (sx * sx2) / pn
        spdx4 = sx4 - (sx2 * sx2) / pn
        spdx2y = sx2y - (sx2 * sy) / pn

        muet = (spdx2 * spdx4) - (spdx3 * spdx3)
        if spdx2 == 0. or muet == 0.:
            raise ValueError('spdx2 == 0. or muet == 0.')

        self.a2 = (spdx2y * spdx2 - spdxy * spdx3) / muet
        self.a1 = (spdxy - self.a2 * spdx3) / spdx2
        self.a0 = (sy - self.a1 * sx - self.a2 * sx2) / pn

    # ------------------------------------------------------------------

    def cible(self):
        """Find momel target points."""
        if len(self.hzptr) == 0:
            raise IOError('Empty pitch array')
        if self.hzsup < self.hzinf:
            raise ValueError('F0 ceiling > F0 threshold')

        pond = []
        pondloc = []  # local copy of pond
        hzes = []
        for ix in range(self.nval):
            hzes.append(0.)
            if self.hzptr[ix] > self.SEUILV:
                pond.append(1.0)
                pondloc.append(1.0)
            else:
                pond.append(0.0)
                pondloc.append(0.0)

        # Examinate each pitch value
        for ix in range(self.nval):
            # Current interval to analyze: from dpx to fpx
            dpx = ix - int(self.lfen1 / 2)
            fpx = dpx + self.lfen1 + 1

            # BB: do not go out of the range!
            if dpx < 0:
                dpx = 0
            if fpx > self.nval:
                fpx = self.nval

            # copy original pond values for the current interval
            for i in range(dpx, fpx):
                pondloc[i] = pond[i]

            nsup = 0
            nsupr = -1
            xc = yc = 0.0
            ret_rgp = True
            while nsup > nsupr:
                nsupr = nsup
                nsup = 0
                try:
                    # Estimate values of: a0, a1, a2
                    self.calcrgp(pondloc, dpx, fpx-1)
                except Exception:
                    # if calcrgp failed.
                    # print "calcrgp failed: ",e
                    ret_rgp = False
                    break
                else:
                    # Estimate hzes
                    for ix2 in range(dpx, fpx):
                        hzes[ix2] = self.a0 + \
                                    (self.a1 + self.a2 * float(ix2)) * \
                                    float(ix2)
                    for x in range(dpx, fpx):
                        if self.hzptr[x] == 0. or \
                                (hzes[x] / self.hzptr[x]) > self.maxec:
                            nsup += 1
                            pondloc[x] = 0.

            # Now estimate xc and yc for the new 'cible'
            if ret_rgp is True and self.a2 != 0.:
                vxc = (0.0 - self.a1) / (self.a2 + self.a2)
                if (vxc > ix - self.lfen1) and (vxc < ix + self.lfen1):
                    vyc = self.a0 + (self.a1 + self.a2 * vxc) * vxc
                    if vyc > self.hzinf and vyc < self.hzsup:
                        xc = vxc
                        yc = vyc

            c = Anchor()
            c.set(xc, yc)
            self.cib.append(c)

    # ------------------------------------------------------------------

    def reduc(self):
        """First target reduction of too close points."""
        # initialisations
        # ---------------
        xdist = []
        ydist = []
        dist = []
        for i in range(self.nval):
            xdist.append(-1.)
            ydist.append(-1.)
            dist.append(-1.)

        lf = int(self.lfen2 / 2)
        xds = yds = 0.
        np = 0

        # xdist and ydist estimations
        for i in range(self.nval-1):
            # j1 and j2 estimations (interval min and max values)
            j1 = 0
            if i > lf:
                j1 = i - lf
            j2 = self.nval - 1
            if i+lf < self.nval-1:
                j2 = i + lf

            # left (g means left)
            sxg = syg = 0.
            ng = 0
            for j in range(j1, i+1):
                if self.cib[j].y > self.SEUILV:
                    sxg = sxg + self.cib[j].x
                    syg = syg + self.cib[j].y
                    ng += 1

            # right (d means right)
            sxd = syd = 0.
            nd = 0
            for j in range(i+1, j2):
                if self.cib[j].y > self.SEUILV:
                    sxd = sxd + self.cib[j].x
                    syd = syd + self.cib[j].y
                    nd += 1

            # xdist[i] and ydist[i] evaluations
            if nd * ng > 0:
                xdist[i] = math.fabs(sxg / ng - sxd / nd)
                ydist[i] = math.fabs(syg / ng - syd / nd)
                xds = xds + xdist[i]
                yds = yds + ydist[i]
                np += 1
        # end for

        if np == 0 or xds == 0. or yds == 0.:
            raise ValueError('Not enough values more than ' +
                             str(self.SEUILV) + ' hz \n')

        # dist estimation (on pondere par la distance moyenne)
        # ----------------------------------------------------
        px = float(np) / xds
        py = float(np) / yds
        for i in range(self.nval):
            if xdist[i] > 0.:
                dist[i] = (xdist[i] * px + ydist[i] * py) / (px + py)

        # Cherche les maxs des pics de dist > seuil
        # -----------------------------------------
        # Seuil = moy des dist ponderees
        seuil = 2. / (px + py)

        susseuil = False
        # Add the start value (=0)
        xd = list()
        xd.append(0)
        xmax = 0

        for i in range(self.nval):
            if len(xd) > int(self.nval/2):
                raise Exception('Too many partitions (', len(xd), ')\n')
            if susseuil is False:
                if dist[i] > seuil:
                    susseuil = True
                    xmax = i
            else:
                if dist[i] > dist[xmax]:
                    xmax = i
                if dist[i] < seuil and xmax > 0:
                    xd.append(xmax)
                    susseuil = False
        # end for
        # do not forget the last analyzed value!
        if susseuil is True:
            xd.append(xmax)
        # Add the final value (=nval)
        xd.append(self.nval)

        # Partition sur les x
        # -------------------
        for ip in range(len(xd)-1):
            # bornes partition courante
            parinf = xd[ip]
            parsup = xd[ip + 1]

            sx = sx2 = sy = sy2 = 0.
            n = 0

            # moyenne sigma
            for j in range(parinf, parsup):
                # sur la pop d'une partition
                if self.cib[j].y > 0.:
                    sx += self.cib[j].x
                    sx2 += self.cib[j].x * self.cib[j].x
                    sy += self.cib[j].y
                    sy2 += self.cib[j].y * self.cib[j].y
                    n += 1

            # pour la variance
            if n > 1:
                xm = float(sx) / float(n)
                ym = float(sy) / float(n)
                varx = float(sx2) / float(n) - xm * xm
                vary = float(sy2) / float(n) - ym * ym

                # cas ou variance devrait etre == +epsilon
                if varx <= 0.:
                    varx = 0.1
                if vary <= 0.:
                    vary = 0.1

                et2x = self.FSIGMA * math.sqrt(varx)
                et2y = self.FSIGMA * math.sqrt(vary)
                seuilbx = xm - et2x
                seuilhx = xm + et2x
                seuilby = ym - et2y
                seuilhy = ym + et2y

                #  Elimination (set cib to 0)
                for j in range(parinf, parsup):
                    if self.cib[j].y > 0. and \
                            (self.cib[j].x < seuilbx or
                             self.cib[j].x > seuilhx or
                             self.cib[j].y < seuilby or
                             self.cib[j].y > seuilhy):
                        self.cib[j].x = 0.
                        self.cib[j].y = 0.

            # Recalcule moyennes
            # ------------------
            sx = sy = 0.
            n = 0
            for j in range(parinf, parsup):
                if self.cib[j].y > 0.:
                    sx += self.cib[j].x
                    sy += self.cib[j].y
                    n += 1

            # Reduit la liste des cibles
            if n > 0:
                cibred_cour = Anchor()
                cibred_cour.set(sx/n, sy/n, n)
                ncibr = len(self.cibred) - 1

                if ncibr < 0:
                    ncibr = 0
                    self.cibred.append(cibred_cour)
                else:
                    # si les cibred[].x ne sont pas strictement croissants
                    # on ecrase  la cible ayant le poids le moins fort
                    if cibred_cour.x > self.cibred[ncibr].x:
                        # 1 cibred en +  car t croissant
                        ncibr += 1
                        self.cibred.append(cibred_cour)
                    else:
                        # t <= precedent
                        if cibred_cour.p > self.cibred[ncibr].p:
                            # si p courant >, ecrase la precedente
                            self.cibred[ncibr].set(cibred_cour.x,
                                                   cibred_cour.y,
                                                   cibred_cour.p)

    # ------------------------------------------------------------------

    def reduc2(self):
        """reduc2.

        2eme filtrage des cibles trop proches en t [et Hz]

        """
        # classe ordre temporel croissant les cibred
        c = quicksortcib(self.cibred)
        self.cibred = c

        self.cibred2.append(self.cibred[0])
        pnred2 = 0
        assert(self.seuilrapp_y > 0.)
        ncibr_brut = len(self.cibred)
        for i in range(1, ncibr_brut):

            delta_x = self.cibred[i].x - self.cibred2[pnred2].x

            if float(delta_x) < float(self.seuildiff_x):
                if math.fabs(float((self.cibred[i].y - self.cibred2[pnred2].y)) /
                             self.cibred2[pnred2].y) < self.seuilrapp_y:
                    self.cibred2[pnred2].x = (self.cibred2[pnred2].x +
                                              self.cibred[i].x) / 2.
                    self.cibred2[pnred2].y = (self.cibred2[pnred2].y +
                                              self.cibred[i].y) / 2.
                    self.cibred2[pnred2].p = (self.cibred2[pnred2].p +
                                              self.cibred[i].p)
                else:
                    if self.cibred2[pnred2].p < self.cibred[i].p:
                        self.cibred2[pnred2].set(self.cibred[i].x,
                                                 self.cibred[i].y,
                                                 self.cibred[i].p)
            else:
                pnred2 += 1
                self.cibred2.append(self.cibred[i])

    # ------------------------------------------------------------------

    def borne(self):
        """borne.

        Principes:
        calcul borne G (D)  si 1ere (derniere) cible est
        ( > (debut_voisement+halo) )
        ( < (fin_voisement -halo)  )
        ce pt de debut(fin) voisement  == frontiere
        cible extremite == ancre
        regression quadratique sur Hz de  [frontiere ancre]

        """
        halo = self.HALO_BORNE_TRAME
        ancre = Anchor()
        borne = Anchor()

        # Borne gauche
        # ------------

        # Recherche 1er voise
        premier_voise = 0
        while premier_voise < self.nval and \
                self.hzptr[premier_voise] < self.SEUILV:
            premier_voise += 1

        if int(self.cibred2[0].x) > (premier_voise + halo):
            # origine des t : ancre.x, et des y : ancre.y
            ancre = self.cibred2[0]

            sx2y = 0.
            sx4 = 0.

            j = 0
            for i in range(int(ancre.x), 0):
                if self.hzptr[i] > self.SEUILV:
                    x2 = float(j) * float(j)
                    sx2y += (x2 * (self.hzptr[i] - ancre.y))
                    sx4 += (x2 * x2)
                j += 1

            frontiere = float(premier_voise)
            a = 0.
            if sx4 > 0.:
                a = sx2y / sx4

            borne.x = frontiere - (ancre.x - frontiere)
            borne.y = ancre.y + \
                      (2 * a * (ancre.x - frontiere) * (ancre.x - frontiere))

        # recherche dernier voisement
        dernier_voise = self.nval - 1
        while dernier_voise >= 0 and self.hzptr[dernier_voise] < self.SEUILV:
            dernier_voise -= 1

        # ################################################################## #

        # nred2 = len(self.cibred2)
        # if( int(self.cibred2[nred2-1].x) < (dernier_voise - halo)):
            # origine des t : ancre.x, et des y : ancre.y
            # ancre = self.cibred2[nred2-1]

            # sx2y = 0.
            # sx4 = 0.
            # j = 0
            # for i in range( int(ancre.x),self.nval):
                # if self.hzptr[i] > self.SEUILV:
                    # x2 = float(j) * float(j)
                    # sx2y += (x2 * (self.hzptr[i] - ancre.y))
                    # sx4 += (x2*x2)
                # j += 1
            # frontiere = float(dernier_voise)
            # a = 0.
            # if (sx4 > 0.):
            #     a = sx2y / sx4

            # borne.set_x( frontiere + (frontiere - ancre.x) )
            # borne.set_y( ancre.y +
            #      (2. * a * (ancre.x - frontiere) * (ancre.x - frontiere)) )

    # ------------------------------------------------------------------

    def annotate(self, pitch_values):
        """Apply momel from a vector of pitch values, one each 0.01 sec.

        :param pitch_values: (list)
        :returns: list of selected anchors

        """
        # Get pitch values
        self.initialize()
        self.set_pitch_array(pitch_values)

        if self.ELIM_GLITCH is True:
            self.elim_glitch()

        self.cible()
        self.reduc()
        if len(self.cibred) == 0:
            raise Exception("No left point after the first pass of point "
                            "reduction.\n")

        self.reduc2()
        if len(self.cibred2) == 0:
            raise Exception("No left point after the second pass of point "
                            "reduction.\n")

        self.borne()

        return self.cibred2
