from xml.sax.saxutils import escape

from .mirror_dir import MirrorUiDirectory
#===============================================
def startHtmlPage(output, title = None, html_base = None,
        css_files = None, js_files = None):
    print >> output, '''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">'''
    if title:
        print >> output, '    <title>%s</title>' % escape(title)
    if html_base:
        print >> output, '    <base href="%s" />' % html_base
    if css_files:
        for name in css_files:
            print >> output, ('    <link rel="stylesheet" '
                'href="ui/%s" type="text/css" media="all"/>' %
                MirrorUiDirectory.transform(name))
    if js_files:
        for name in js_files:
            print >> output, ('    <script type="text/javascript" '
                'src="ui/%s"></script>' %
                MirrorUiDirectory.transform(name))
    print >> output, '  </head>'

#===============================================
def formTopPage(output, title, html_base, workspace):
    startHtmlPage(output, title, html_base,
        css_files = ["base.css",
            "anf.css", "filters.css", "zones.css", "rules.css"],
        js_files = ["anf.js", "monitor.js", "filters.js",
            "conditions.js", "zones.js", "rules.js"])

    print >> output, ('  <body onload="initWin(\'%s\', \'\');">' %
        (workspace.getName()))
    _formMainDiv(output, workspace.getName())
    _formFiltersDiv(output)
    _formZonesDiv(output, workspace.iterZones())
    _formNoteDiv(output)
    _formRulesDiv(output)

    print >> output, ' </body>'
    print >> output, '</html>'

#===============================================
def _formMainDiv(output, workspace_name):
    print >> output, '''
    <div id="all">
      <div id="top">
        <div id="top-ws">
          <div id="ws-ctrl">
            <div id="ws-info">
              Ws:
              <span id="ws-name"></span><br/>
            </div>
            <div id="list-info">
              <span id="ws-control-wrap" title="Control Menu..." class="drop">
                <span id="ws-control-open" class="drop"
                    onclick="openControlMenu()";>&#8285;</span>
                <div id="ws-control-menu" class="drop">
                    <div onclick="goHome();"
                        class="drop ctrl-menu">Home Directory</div>
                    <div onclick="openNote();"
                        class="drop ctrl-menu">Workspace Note</div>
                    <div onclick="switchResMode();" class="drop ctrl-menu">
                        <span id="res-mode-check">&#10003;</span>Research mode</div>
                    <div onclick="showExport();"
                        class="drop ctrl-menu" >Export...</div>
                </div>
                <div id="ws-export-result" class="drop"></div>
              </span>&emsp;
              <span id="list-report"></span>
              <input id="list-rand-portion" type="number" min="1" max="5"
                onchange="listRandPortion();"/>
            </div>
          </div>
        </div>
        <div  id="top-filters">
          Filters:
          <div id="flt-ctrl">
            <div id="flt-named">
              <input id="flt-check-named" type="checkbox"
                onchange="checkCurFilters(0);"/>
              <select id="flt-named-select" onchange="pickNamedFilter();">
                <option value=""></option>
              </select>
            </div>
            <div id="flt-cur">
              <input id="flt-check-current" type="checkbox"
                onchange="checkCurFilters(1);"/>
              <span id="flt-current-state" title="Setup filter"
                 onclick="filterModOn();">
              </span>
            </div>
          </div>
        </div>
        <div id="top-zones">
          <div id="zone-ctrl">
            Zone:
              <span id="zone-cur-title"></span>
              <select style="visibility:hidden;">
                <option value=""></option>
              </select>
          </div>
          <div id="zone-cur">
            <input id="zone-check" type="checkbox"
                onchange="checkCurZone();"/>
            <span id="zone-descr" onclick="zoneModOn();"></span>
          </div>
         </div>
         <div id="top-tags">
            <div id="tags-ctrl">
              Tags:
              <select id="cur-tag" onchange="pickTag();">
                <option value=""></option>
              </select>
              <span id="cur-tag-count"></span>
            </div>
            <div id="cur-tag-nav">
              <span id="cur-tag-nav-first" class="tags-nav"
                onclick="tagNav(0);">|&#9664;</span>
              <span id="cur-tag-count-prev" class="tags-count"></span>
              <span id="cur-tag-nav-prev" class="tags-nav"
                onclick="tagNav(1);">&#9664;</span>
              <span id="cur-tag-here">&#11044;</span>
              <span id="cur-tag-nav-next" class="tags-nav"
                onclick="tagNav(3);">&#9654;</span>
              <span id="cur-tag-count-next" class="tags-count"></span>
              <span id="cur-tag-nav-last" class="tags-nav"
                onclick="tagNav(4);">&#9654;|</span>
            </div>
         </div>
      </div>
      <div id="bottom">
        <div id="bottom-left">
          <div id="wrap-rec-list">
            <div id="rec-list">
            </div>
          </div>
        </div>
        <div id="bottom-right">
            <iframe id="rec-frame2" name="rec-frame2" src="norecords">
            </iframe>
            <iframe id="rec-frame1" name="rec-frame1" src="norecords">
            </iframe>
        </div>
      </div>
    </div>''' % {"ws": workspace_name}

#===============================================
def _formFiltersDiv(output):
    print >> output, '''
    <div id="filter-back">
      <div id="filter-mod">
        <div id="filter-stat">
          <div id="stat-list">
          </div>
        </div>
        <div id="filter-conditions">
          <div id="filter-ctrl">
            <span id="cond-title"></span>
            <button id="filter-add-cond" onclick="filterAddCond();">
              Add
            </button>
            <button id="filter-update-cond" onclick="filterUpdateCond();">
              Update
            </button>
            <button id="filter-delete-cond"
                onclick="filterDeleteCond();">
              Delete
            </button>
            <button id="filter-undo-cond" title="Undo"
                onclick="filterUndoCond();">
              &#8630;
            </button>
            <button id="filter-redo-cond" title="Redo"
                onclick="filterRedoCond();">
              &#8631;
            </button>
            <span id="close-filter" onclick="filterModOff();">&times;</span>
          </div>
          <div id="filter-cur-cond-text">
            <span id="cond-text"></span>
            <span id="cond-message"></span>
          </div>
          <div id="filter-cur-cond">
            <div id="cur-cond-numeric">
              <span id="cond-min" class="num-set"></span>
              <input id="cond-min-inp" class="num-inp"
                type="text" onchange="checkOpNum();"/>
              <span id="cond-sign"></span>
              <input id="cond-max-inp" class="num-inp"
                type="text" onchange="checkOpNum();"/>
              <span id="cond-max" class="num-set"></span>
              <span id="num-count" class="num-count"></span>
              <input id="cond-undef-check"
                type="checkbox"  onchange="checkOpNum();"/>
              <span id="cond-undef-count" class="num-count"
                class="num-count"></span>
            </div>
            <div id="cur-cond-enum">
              <div id="wrap-cond-enum">
                <div id="wrap-cond-enum-list">
                  <div id="cur-cond-enum-list">
                     <div id="op-enum-list">
                     </div>
                  </div>
                </div>
                <div id="cur-cond-enum-ctrl">
                  <div id="cur-cond-enum-zeros">
                    Show zeros&nbsp;<input id="cur-enum-zeros" type="checkbox"
                        onchange="sOpEnumH.careEnumZeros();"/>
                  </div>
                  <div id="cur-cond-enum-mode">
                    <span id="cond-mode-and-span">
                      <input id="cond-mode-and" type="checkbox"
                        onchange="sOpEnumH.checkControls(1);"/>&nbsp;AND
                    </span><br/>
                    <span id="cond-mode-only-span">
                      <input id="cond-mode-only" type="checkbox"
                        onchange="sOpEnumH.checkControls(2);"/>&nbsp;ONLY
                    </span><br/>
                    <span id="cond-mode-not-span">
                      <input id="cond-mode-not" type="checkbox"
                        onchange="sOpEnumH.checkControls(3);"/>&nbsp;NOT
                    </span><br/>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div id="filters-ctrl">
            <button class="op-button"
                onclick="filterModOff();">
                Done
            </button>
            <button id="filter-clear-all" class="op-button"
                onclick="filterClearAll();">
                Clear
            </button>
            <div class="dropdown">
              <button id="filter-filters-operations" class="op-button drop"
                    onclick="filtersOpMenu();">
                Filters...
              </button>
              <div id="filters-op-list" class="dropdown-content drop">
                <a class="drop" id="filters-op-load"
                    onclick="filterOpStartLoad();">Load</a>
                <a class="drop" id="filters-op-create"
                    onclick="filterOpStartCreate();">Create</a>
                <a class="drop"  id="filters-op-modify"
                    onclick="filterOpStartModify();">Modify</a>
                <a class="drop"  id="filters-op-delete"
                    onclick="filterOpDelete();">Delete</a>
              </div>
            </div>
            <div id="filter-name-combo" class="combobox">
              <select id="filter-name-filter-list"
                  onchange="fltFilterListSel();">
                <option value=""></option>
              <input id="filter-name-filter" type="text" />
              </select>
            </div>
            <button id="filter-flt-op" class="op-button"
                onclick="filterFiltersOperation();">
              ...
            </button>
          </div>
          <div id="filter-wrap-list-conditions">
            <div id="filter-list-conditions">
              <div id="cond-list">
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>'''

#===============================================
def _formZonesDiv(output, zones):
    rep_check_zones, rep_div_zones = [], []
    for zone in zones:
        rep_check_zones.append(('<span id="zn--%s">'
            '<input id="zn-check--%s" class="zone-checkbox" type="checkbox" '
            'onchange="checkWorkZone(\'%s\');"/>%s</span>') %
            (zone.getName(), zone.getName(), zone.getName(),
            escape(zone.getTitle())))
        rep_div_zones.append('<div class="work-zone-list" '
            'id="zn-div--%s"></div>' % zone.getName())
    params = {
        "check_zones": "\n".join(rep_check_zones),
        "div_zones": "\n".join(rep_div_zones)}

    print >> output, '''
    <div id="zone-back">
      <div id="zone-mod">
        <div id="zone-top">
            <p id="zone-title">Zone setup
              <span id="close-zone" onclick="zoneModOff();">&times;</span>
            </p>
        </div>
        <div id="work-zone-area">
          <div id="work-zone-left">
            <div id="work-zone-kind">
               %(check_zones)s
            </div>
            <div id="work-zone-wrap-list">
                %(div_zones)s
            </div>
          </div>
          <div id="zone-right">
            <div id="work-zone-def">
            </div>
            <div id="work-zone-ctrl">
              <button class="op-button"
                  onclick="zoneModOff();">
                Done
              </button>
              <button id="work-zone-clear" class="op-button"
                  onclick="zoneClearSelect();">
                Clear
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
''' % params

#===============================================
def _formNoteDiv(output):
    print >> output, '''
    <div id="note-back">
      <div id="note-mod">
        <div id="note-top">
            <p id="note-title">Workspace
                <span id="note-ws-name"></span> note
              <span id="close-note" onclick="noteModOff();">&times;</span>
            </p>
        </div>
        <div id="work-note-area">
            <textarea id="note-content"></textarea>
        </div>
        <div id="work-note-ctrl">
              <button class="op-button"
                  onclick="saveNote();">
                Save
              </button>
              <button class="op-button"
                  onclick="noteModOff();">
                Done
              </button>
              <span id="note-time"></span>
            </div>
          </div>
        </div>
      </div>
    </div>
'''

#===============================================
def _formRulesDiv(output):
    print >> output, '''
    <div id="rules-back">
      <div id="rules-mod">
        <div id="rules-top">
            <p id="rules-title">&#9874; Rules evaluation setup
              <span id="close-rules" onclick="rulesModOff();">&times;</span>
            </p>
        </div>
        <div id="rules-main">
          <div id="rules-left">
            <div id="rules-wrap-columns">
              <div id="rules-columns">
              </div>
            </div>
            <div id="rules-wrap-param">
              <div id="hi----param"
                class="rule-item" onclick="ruleItemSel(\'--param\');">
                  Parameters
              </div>
            </div>
          </div>
          <div id="rules-right">
            <div id="rules-wrap-content">
                <textarea id="rule-item-content"
                    oninput="checkRuleContent();"></textarea>
            </div>
            <div id="rule-item-ctrl">
                <button id="rule-item-modify" onclick="ruleItemModify();">
                  Apply changes
                </button>
                <button id="rule-item-reset" onclick="ruleItemReset();">
                  Reset changes
                </button>
            </div>
            <div id="rule-item-errors">
            </div"
          </div>
        </div>
      </div>
    </div>'''

#===============================================
def tagsBlock(output):
    print >> output, '''
<div id="tg-all">
  <div id="tg-wrap-filters">
    <div id="tg-filters">
        <i>Filters:</i> <span id="tg-filters-list"></span>
        <span id="tg-run-rules" title="Rules evaluation setup"
            onclick="window.parent.rulesModOn();">&#9874;</span>
    </div>
  </div>
  <div id="tg-tags">
    <div id="tg-title">
        <i>Tags:</i>
    </div>
    <div id="tg-tags-left">
      <div id="tg-check-tags-list">
      </div>
      <div id="tg-tags-wrap-list">
        <div id="tg-op-tags-list">
        </div>
      </div>
    </div>
    <div id="tg-tags-right">
      <div id="tg-tags-ctrl">
        <div class="combobox">
          <select id="tg-tags-tag-list" onchange="tagEnvTagSel();">
            <option value=""></option>
          </select>
          <input id="tg-tag-name" type="text" />
        </div>
        <button id="tg-tag-new" class="op-button" onclick="tagEnvNew();">
          Add
        </button>
        <button id="tg-tag-save" class="op-button" onclick="tagEnvSave();">
          Save
        </button>
        <button id="tg-tag-cancel" class="op-button" onclick="tagEnvCancel();">
          Cancel
        </button>
        <button id="tg-tag-delete"
            title="Delete tag" class="op-button" onclick="tagEnvDelete();">
          Delete
        </button>
      </div>
      <div id="tg-tag-wrap-value">
        <div id="tg-tag-value">
        </div>
        <div id="tg-tag-edit">
          <textarea id="tg-tag-value-content" />
          </textarea>
        </div>
      </div>
      <div id="tg-tags-ctrl-tags">
        <button id="tg-tag-clear-all" class="op-button"
            onclick="tagEnvClearAll();">
          Clear
        </button>
        <button id="tg-tag-undo" class="op-button" title="Undo"
            onclick="tagEnvUndo();">
          &#8630;
        </button>
        <button id="tg-tag-redo" class="op-button"  title="Redo"
            onclick="tagEnvRedo();">
          &#8631;
        </button>
        <span id="tags-time">
        </span>
      </div>
    </div>
  </div>
</div>'''

#===============================================
def noRecords(output):
    startHtmlPage(output, css_files = ["anf.css"])
    print >> output, '''
  <body>
    <h3>No records available</h3>
    <p>Try to drop <button onclick='parent.window.updateCurZone(false);'
            >zone</button>
        or
        <button onclick='parent.window.updateCurFilter("");'
            >filter</button>.</p>
  </body>
</html>'''

#===============================================
def dirPage(output, title, html_base):
    startHtmlPage(output, title, html_base,
        css_files = ["dir.css"], js_files = ["dir.js"])
    print >> output, '''
  <body onload="setup();">
    <h2>%s home directory</h2>
    <p id="p-version">System version: <span id="span-version"></span></p>
    <div id="div-main">
    </div>
  </body>
</html>''' % title

#===============================================
def notFound(output, title, html_base):
    startHtmlPage(output, title + ": Page not found", html_base,
        css_files = ["dir.css"])
    print >> output, '''
  <body>
    <h2>Page not found</h2>
    <p><a href="dir" target="%s">Anfisa home</a></p>
  </body>
</html>''' % (title + "/dir")

