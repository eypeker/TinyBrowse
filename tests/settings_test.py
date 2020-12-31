import unittest
from settings import setting_model as stm
from typing import Tuple


class MyTestCase(unittest.TestCase):
    testlines = [["homeurl:\thttp://google.de", "testsetting:\tanal im kanal\n", "kunst  salat", "6_afraid_of_7:True",
                 "reason: 7 eight 9"],
                 [("homeurl","http://google.de"), ("testsetting","anal im kanal"), (),("6_afraid_of_7","True"),
                  ("reason","7 eight 9")]
                 ]

    testtuples = [[("Testtest  ", "Akademie+++"), ("Lars.", "Ungl.###*+++aublich"), ("", "a_*dfsvbsd\n ##")],
                  [("Kafa", "Leyla"), ("187", "Strassenbande"), ("GNTK", "FCKRP")]
                  ]

    testsettings = [["homeurl", "lafer_lighter_lecker"],
                    [["google.de", "\n.com", "\t", "\tdsaf"],
                     ["Kartoffeln", "Hühnchen mit Reis", "Lammragout", "anabolstatt abitur"]]]



    def test_setfileexists(self):
        sm = stm()
        sm.deletesettingfile()
        self.assertFalse(sm.settingfileexists())

    def test_createsetting(self):
        sm = stm()
        sm.createsettingfile()
        self.assertTrue(sm.settingfileexists())
        self.assertFalse(sm.createsettingfile())

    def test_deletesettings(self):
        sm = stm()
        sm.deletesettingfile()
        self.assertFalse(sm.settingfileexists())
        self.assertFalse(sm.deletesettingfile())

    def test_linefitspattern(self):
        sm = stm()
        self.assertTrue(sm.linefitspattern(self.testlines[0][0]))
        self.assertTrue(sm.linefitspattern(self.testlines[0][1]))
        self.assertFalse(sm.linefitspattern(self.testlines[0][2]))
        self.assertTrue(sm.linefitspattern(self.testlines[0][3]))
        self.assertTrue(sm.linefitspattern(self.testlines[0][4]))

    def test_valuefitspattern(self):
        sm = stm()
        for t in self.testtuples[0]:
            self.assertFalse(sm.valuefitspattern(t[1]))
        for t in self.testtuples[1]:
            self.assertTrue(sm.valuefitspattern(t[1]))

    def test_settingfitspattern(self):
        sm = stm()
        for t in self.testtuples[0]:
            self.assertFalse(sm.settingfitspattern(t[0]))
        for t in self.testtuples[1]:
            self.assertTrue(sm.settingfitspattern(t[0]))

    def test_linetovalues(self):
        sm = stm()
        for i in range(len(self.testlines[0])):
            l = self.testlines[0][i]
            vl = self.testlines[1][i]
            if sm.linefitspattern(l):
                lvl = sm.getvaluesfromline(l)
                self.assertTrue(lvl[0] == vl[0])
                self.assertTrue((lvl[1] == vl[1]))

    def test_changesettings(self):
        sm = stm()
        gs = self.testsettings[0][0]
        gv = self.testsettings[1][0][0]
        sm.changesetting(gs, gv)
        self.assertTrue(sm.didsettingschanged())
        self.assertTrue(sm.getsetting(gs) == gv)
        sm.settingschanged = False
        self.assertFalse(sm.didsettingschanged())
        for v in self.testsettings[1][0][1:]:
            self.assertTrue(sm.getsetting(gs) == gv)
            self.assertFalse(sm.didsettingschanged())

        l = self.testsettings[0][1]
        for v in self.testsettings[1][1]:
            sm.changesetting(l, v)
            self.assertTrue(sm.getsetting(l) == v)

    def test_saveloadsettings(self):
        sm = stm()
        tps = self.testtuples[1]
        for t in tps:
            sm.changesetting(t[0], t[1])
        sm.savesettings()
        self.assertTrue(sm.settingfileexists())
        del sm
        sf = stm()
        print("kartoffel")
        for t in tps:
            self.assertTrue(sf.getsetting(t[0]) == t[1])
        sf.deletesettingfile()

    def test_valuestoline(self):
        sm = stm()
        self.assertTrue(sm.linefitspattern(sm.getlinefromvalues(self.testtuples[1][0][0], self.testtuples[1][0][1])))
        self.assertTrue(sm.linefitspattern(sm.getlinefromvalues(self.testtuples[1][1][0], self.testtuples[1][1][1])))
        self.assertTrue(sm.linefitspattern(sm.getlinefromvalues(self.testtuples[1][2][0], self.testtuples[1][2][1])))


if __name__ == '__main__':
    unittest.main()
