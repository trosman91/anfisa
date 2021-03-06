from xml.sax.saxutils import escape

from .attr import AttrH
from .view_repr import vcfRepr
from .colgrp import ColGroupsH

#===============================================
class AspectH:
    def __init__(self, name, title, source, field = None,
            attrs = None, ignored = False, col_groups = None,
            research_only = False, mode = "dict"):
        self.mName     = name
        self.mTitle    = title
        self.mSource   = source
        self.mField    = field
        self.mAttrs    = None
        self.mIgnored  = ignored
        self.mResearchOnly = research_only
        self.mColGroups = col_groups
        self.mMode      = mode
        assert self.mSource in ("view", "data")
        if self.mColGroups is not None:
            assert self.mField is None

        if self.mIgnored or self.mMode != "dict":
            self.mAttrs = []
        if attrs is not None:
            self.setAttributes(attrs)

    def setAttributes(self, attrs):
        self.mAttrs = attrs
        for attr_h in self.mAttrs:
            attr_h.setAspect(self)

    def addAttr(self, attr_h):
        attr_h.setAspect(self)
        self.mAttrs.append(attr_h)

    def delAttr(self, attr_h):
        self.mAttrs.remove(attr_h)

    def getName(self):
        return self.mName

    def getSource(self):
        return self.mSource

    def getTitle(self):
        return self.mTitle

    def getAttrs(self):
        return iter(self.mAttrs)

    def getField(self):
        return self.mField

    def getColGroups(self):
        return self.mColGroups

    def isIgnored(self):
        return self.mIgnored

    def getMode(self):
        return self.mMode

    #===============================================
    def dump(self):
        ret = {
            "name": self.mName,
            "title": self.mTitle,
            "source": self.mSource,
            "ignored": self.mIgnored,
            "research": self.mResearchOnly,
            "mode": self.mMode,
            "attrs": [attr_h.dump() for attr_h in self.mAttrs]}
        if self.mField is not None:
            ret["field"] = self.mField
        if self.mColGroups is not None:
            ret["col_groups"] = self.mColGroups.dump()
        return ret

    @classmethod
    def load(cls, data):
        return cls(data["name"], data["title"], data["source"],
            field = data.get("field"),
            attrs = [AttrH.load(it) for it in data["attrs"]],
            ignored = data["ignored"],
            col_groups = ColGroupsH.load(data.get("col_groups")),
            research_only = data["research"],
            mode = data["mode"])

    #===============================================
    def checkResearchBlock(self, research_mode):
        return (not research_mode) and self.mResearchOnly

    def getViewRepr(self, rec_data, research_mode):
        ret = {
            "name": self.mName,
            "title": self.mTitle,
            "kind": {"view": "norm", "data": "tech"}[self.mSource]}
        if self.mName == "input":
            ret["type"] = "pre"
            if "input" in rec_data["data"]:
                ret["content"] = vcfRepr(rec_data["data"]["input"])
            return ret
        ret["type"] = "table"
        objects = [rec_data[self.mSource]]
        if self.mField:
            objects = [objects[0][self.mField]]
        if self.mColGroups:
            objects, prefix_head = self.mColGroups.formColumns(objects)
            if prefix_head:
                ret["colhead"] = [[escape(title), count]
                    for title, count in prefix_head]
        ret["columns"] = len(objects)
        fld_data = dict()
        for attr in self.mAttrs:
            if (attr.getName() is None or
                    attr.checkResearchBlock(research_mode) or
                    attr.hasKind("hidden")):
                continue
            values = [attr.htmlRepr(obj) for obj in objects]
            if any([vv != ('-', "none") for vv in values]):
                fld_data[attr.getName()] = values
        rows = []
        for attr in self.getAttrs():
            a_name = attr.getName()
            if a_name is None:
                rows.append([])
                continue
            if a_name in fld_data:
                rows.append([a_name, escape(attr.getTitle()),
                [[val, class_name]
                    for val, class_name in fld_data[a_name]]])
        ret["rows"] = rows
        return ret
