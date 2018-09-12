import os, codecs

from .acmg59 import evalRec as acmg59_evalRec
from .quality_check import evalRec as quality_check_evalRec
from .af_check import evalRec as af_check_evalRec
from .rare_check import evalRec as rare_check_evalRec
from .common_check import evalRec as common_check_evalRec
from .polyphen_check import evalRec as polyphen_check_evalRec

#===============================================
class RuleFuncH:
    def __init__(self, name, filename, function, expert_mode = False):
        self.mName      = name
        self.mFileName  = filename
        self.mFunc      = function
        self.mIsExpert  = expert_mode

    def getFileName(self):
        return self.mFileName

    def getName(self):
        return self.mName

    def getFunc(self):
        return self.mFunc

    def isExpert(self):
        return self.mIsExpert

#===============================================
class RuleParamH:
    def __init__(self, name, value, expert_mode = False):
        self.mName      = name
        self.mValue     = value
        self.mIsExpert  = expert_mode

    def getName(self):
        return self.mName

    def getValue(self):
        return self.mValue

    def setValue(self, value):
        self.mValue = value

    def isExpert(self):
        return self.mIsExpert

#===============================================
class HOT_SETUP:
    sPath = os.path.dirname(os.path.abspath(__file__))

    FUNCTIONS = [
        RuleFuncH("ACMG59",
            "acmg59", acmg59_evalRec),
        RuleFuncH("Quality-Check",
            "quality_check", quality_check_evalRec),
        RuleFuncH("Candidates-Rare",
            "rare_check", rare_check_evalRec),
        RuleFuncH("Candidates",
            "common_check", common_check_evalRec),
        RuleFuncH("gnomAD_Frequency_Threshold",
            "af_check", af_check_evalRec),
        RuleFuncH("Has_Damaging_Predictions",
            "polyphen_check", polyphen_check_evalRec)
    ]

    PARAMETERS = [
        RuleParamH("af", 0.01),
        RuleParamH("af_in_db", 0.05),
        RuleParamH("severity", 1),
        RuleParamH("gq", 20),
        RuleParamH("fs", 30),
        RuleParamH("qd", 4)]

    @classmethod
    def getSrcContent(cls, key):
        with codecs.open(cls.sPath + "/" + key + ".py",
                "r", encoding = "utf-8") as inp:
            return inp.read()
