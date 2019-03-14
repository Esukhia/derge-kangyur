#!/usr/bin/env python3

# The MIT License (MIT)
# Copyright (c) 2018 Esukhia
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

import re
import os

PAREN_RE = re.compile(r"\(([^\),]*),([^\),]*)\)")
TOH_RE = re.compile(r"\{T(?P<idx>\d+[ab]?)(?:-(?P<subidx>\d+))?\}")

def parrepl(match, mode, pagelinenum, filelinenum, volnum, shortfilename):
    first = match.group(1)
    sec = match.group(2)
    if (len(first) > 0 and len(sec) > 0 and (
            (first[0]== '་' and sec[0]!= '་') or 
            (sec[0]== '་' and first[0]!= '་') or
            (first[-1]== '་' and sec[-1]!= '་') or
            (sec[-1]== '་' and first[-1]!= '་'))):
        printerror("error on line "+str(filelinenum)+" tsheg not matching in parenthesis")
    return mode == 'first' and first or sec

error_regexps = [
        {"reg": re.compile(r"([^ །\(\)\[,]།[^ །\(\]\)༽,]|(?:[^ངོེིུྃཾ]|ང[^ངོེིུྃཾ]|[^ང][ོེིུྃཾ])་།|(?:[^ཀགཤ།ོེིུྃཾ]|[ཀགཤ][^ཀགཤོེིུྃཾ]|[^ཀགཤ][ོེིུྃཾ]|[ཀགཤ][ོེིུྃཾ]།+)། །།|།།།)"), "msg": "invalid shad sequence", "type": "punctuation"},
        {"reg": re.compile(r"[^ཀ-ྼ][ཱ-྄྆྇ྍ-ྼ]"), "msg": "invalid unicode combination sequence", "type": "invalid"},
        {"reg": re.compile(r"[^ༀ-࿚#-~ \[\]\{\}\.]"), "msg": "invalid unicode characters (non-Tibetan, non-ascii)", "type": "invalid"},
        {"reg": re.compile(r"([ྱུྲཿཾ྄ྃྭིྀ་ ])\1"), "msg": "invalid double diactitic sign (shabkyu, gigu, etc.) or tshek", "type": "invalid"},
        {"reg": re.compile(r"ཿ་"), "msg": "invalid visarga + tshek", "type": "punctuation"},
        {"reg": re.compile(r"([^༄༅]༅|[^࿓࿔]࿔|[࿔༅][^།༅࿔])"), "msg": "invalid yigo", "type": "punctuation"},
        {"reg": re.compile(r"[ༀ-༃༆-༊༎-༟ྰ]"), "msg": "suspicious Tibetan character", "type": "invalid"},
        {"reg": re.compile(r"([ཀགཤ།] །|[^ ཀགཤ།]། |[ཀགཤ།]། |[ཀགཤ།][། ]|[༽ཿ་ \]nl])$"), "msg": "invalid end of line", "type": "punctuation", "neg": True},
        # see https://docs.microsoft.com/en-us/typography/script-development/tibetan#reor
        # https://docs.microsoft.com/en-us/typography/script-development/use#glyph-reordering
        {"reg": re.compile(r"([ཱ-྇][ྍ-ྼ]|[ི-྄]ཱ|[ྃཾཿ][ཱ-ཽྀ])"), "msg": "invalid character order (vowel before subscript or achung after vowel)", "type": "invalid"},
        {"reg": re.compile(r"(ཪ[ླྙྲྱཱ-྇ །་༼-ྌྉྈ\(\)\[\]]|[^ཏ]ྲ[ྐ-ྫྷྮ-ྻ]|རྻ)"), "msg": "possible wrong form of rago used (0F62 vs. 0F65)", "type": "invalid"},
        {"reg": re.compile(r"([ྀིེཻོཽུ]{2,}|ཱ{2,})"), "msg": "༺དབྱངས་ཀྱི་སྐྱོན།༻ invalid vowel duplication (use 0F7D and 0F7B when relevant)", "type": "invalid"},
        {"reg": re.compile(r"[ཀྐཏྟཔྤ][ྒྫྡྦ]"), "msg": "possible invalid Sanskrit sandhi", "type": "sanskrit"},
    ]
    # opposite of last is sort of ([ཀགཤ།]། |[^ ཀགཤ།]།|[༽ཿ་\]nl] )\n

def check_simple_regexp(line, pagelinenum, filelinenum, volnum, options, shortfilename):
    for regex_info in error_regexps:
        if "neg" in regex_info and regex_info["reg"]:
            if not regex_info["reg"].search(line):
                report_error(pagelinenum, filelinenum, volnum, shortfilename, regex_info["type"], regex_info["msg"], "")
            continue
        for match in regex_info["reg"].finditer(line):
            s = match.start()
            e = match.end()
            linewithhighlight = line[:s]+"**"+line[s:e]+"**"+line[e:]
            report_error(pagelinenum, filelinenum, volnum, shortfilename, regex_info["type"], regex_info["msg"], linewithhighlight)

def endofverse(state, volnum, shortfilename):
    nbsyls = state['curnbsyllables']
    #print(str(nbsyls)+" "+str(state['prevnbsyllables']))
    if state["nbshad"] == 2:
        prevnbsyls = state['prevnbsyllables']
        nbsylsdiff = prevnbsyls - nbsyls
        if (prevnbsyls in [7,9,11]) and (nbsylsdiff == 1 or nbsylsdiff == -1):
            bchar = state['curbeginchar']
            line = state['curbeginline']
            highlight = line[:bchar]+"***"+line[bchar:]
            report_error(state['curbeginpagelinenum'], state['curbeginfilelinenum'], volnum, shortfilename, "verses", "verse has "+str(nbsyls)+" syllables while previous one has "+str(prevnbsyls), highlight)
    state['prevnbsyllables'] = nbsyls
    state['nbshad'] = 0
    state['curbeginchar'] = -1

def endofsyllable(state):
    line = state['curbeginsylline']
    syllable = line[state['curbeginsylchar']:state['curendsylchar']]
    if syllable.startswith('བཛྲ') or syllable.startswith('པདྨ') or syllable.startswith('ཀརྨ') or syllable.startswith("ཤཱཀྱ"):
        state['curnbsyllables'] += 1
    #if syllable.endswith('འོ') or syllable.endswith("འམ") or syllable.endswith("འང"):
    #    state['curnbsyllables'] += 1
    state['curnbsyllables'] += 1

def check_verses(line, pagelinenum, filelinenum, state, volnum, options, shortfilename):
    lastistshek = state['lastistshek']
    lastisbreak = False
    for idx in range(0,len(line)):
        c = line[idx]
        if c in "#\{\}[]T01234567890ab.\n":
            continue
        if (c >= 'ཀ' and c <= 'ྃ') or (c >= 'ྐ' and c <= 'ྼ'):
            if lastisbreak:
                endofsyllable(state)
                endofverse(state, volnum, shortfilename)
            if state['curbeginchar'] == -1:
                state['curbeginchar'] = idx
                state['curnbsyllables'] = 0
                state['curbeginpagelinenum'] = pagelinenum
                state['curbeginline'] = line
                state['curbeginfilelinenum'] = filelinenum
            if not lastistshek and not lastisbreak:
                continue
            if lastistshek and not lastisbreak:
                endofsyllable(state)
            lastisbreak = False
            state['curbeginsylchar'] = idx
            state['curbeginsylline'] = line
            lastistshek = False
        elif c == '་' and not lastistshek and not lastisbreak:
            state['curendsylchar'] = idx
            lastistshek = True
        else:
            if not lastisbreak:
                if not lastistshek:
                    state['curendsylchar'] = idx
                lastisbreak = True
            if c == '།':
                state['nbshad'] += 1
    state['lastistshek'] = lastistshek

def tohmatch(tohm, state, pagelinenum, filelinenum, volnum, shortfilename):
    idx = tohm.group('idx')
    letter = ""
    subidx = tohm.group("subidx")
    subidxi = None
    if idx.endswith('a') or idx.endswith('b'):
        letter = idx[-1:]
        idx = idx[:-1]
    try:
        idxi = int(idx)
        if subidx is not None:
            subidxi = int(subidx)
    except ValueError:
        report_error(pagelinenum, filelinenum, volnum, shortfilename, "format", "cannot convert Tohoku index to integer", "")
        return
    tohstr = tohm.group(0)
    lasttohstr = state['lasttohstr']
    lastidx = state['lasttohidx']
    lastsubidx = state['lasttohsubidx']
    lastletter = state['lasttohletter']
    if idxi != lastidx+1:
        if idxi == lastidx:
            if (lastletter == "a" and letter == "b") or (lastletter == "" and letter == "a"):
                pass
            elif subidxi is not None and ((lastsubidx is None and subidxi == 1) or (subidxi == lastsubidx+1)):
                pass
            else:
                report_error(pagelinenum, filelinenum, volnum, shortfilename, "tohoku", "non consecutive Tohoku indexes: "+lasttohstr+" -> "+tohstr, "")
        else:
            report_error(pagelinenum, filelinenum, volnum, shortfilename, "tohoku", "non consecutive Tohoku indexes: "+lasttohstr+" -> "+tohstr, "")
    state['lasttohidx'] = idxi
    state['lasttohletter'] = letter
    state['lasttohsubidx'] = subidxi
    state['lasttohstr'] = tohstr

def parse_one_line(line, filelinenum, state, volnum, options, shortfilename):
    if filelinenum == 1:
        state['pageseqnum']= 1
        state['pagenum']= 1
        state['pageside']= 'a'
        return
    pagelinenum = ''
    endpnumi = line.find(']')
    if endpnumi == -1:
        report_error("", filelinenum, volnum, shortfilename, "format", "cannot find \"]\"", "")
        return
    pagelinenum = line[1:endpnumi]
    pagenum = -1
    pageside = -1
    linenum = 0
    isBis = False
    doti = pagelinenum.find('.')
    if doti == -1:
        pageside = pagelinenum[-1]
        if pageside not in ['a', 'b']:
            report_error(pagelinenum, filelinenum, volnum, shortfilename, "format", "cannot understand page side", "")
            return
        pagenumstr = pagelinenum[:-1]
        if pagelinenum[-2]== 'x':
            isBis = True
            pagenumstr = pagelinenum[:-2]
        try:
            pagenum = int(pagenumstr)
        except ValueError:
            report_error(pagelinenum, filelinenum, volnum, shortfilename, "format", "cannot understand page side", "")
            return
    else:
        linenumstr = pagelinenum[doti+1:]
        pageside = pagelinenum[doti-1]
        if pageside not in ['a', 'b']:
            report_error(pagelinenum, filelinenum, volnum, shortfilename, "format", "cannot understand page side", "")
            return
        pagenumstr = pagelinenum[0:doti-1]
        if pagelinenum[doti-2]== 'x':
            isBis = True
            pagenumstr = pagelinenum[0:doti-2]
        try: 
            pagenum = int(pagenumstr)
            linenum = int(linenumstr)
        except ValueError:
            report_error(pagelinenum, filelinenum, volnum, shortfilename, "format", "cannot convert page to integer", "")
            return
    newpage = False
    if 'pagenum' in state and 'pageside' in state:
        oldpagenum = state['pagenum']
        oldpageside = state['pageside']
        if oldpagenum != pagenum and oldpagenum != pagenum-1:
            printerror("error on line "+str(filelinenum)+" leap in page numbers from "+str(oldpagenum)+" to "+str(pagenum))
        if oldpagenum == pagenum and oldpageside == 'b' and pageside == 'a':
            printerror("error on line "+str(filelinenum)+" going backward in page sides")
        if oldpagenum == pagenum-1 and (pageside == 'b' or oldpageside == 'a'):
            printerror("error on line "+str(filelinenum)+" leap in page sides")
        if oldpagenum != pagenum or oldpageside != pageside:
            newpage = True
    if newpage:
        state['pageseqnum']+= 1
    state['pagenum']= pagenum
    state['pageside']= pageside
    if 'linenum' in state and linenum != 0:
        oldlinenum = state['linenum']
        if oldlinenum != linenum and oldlinenum != linenum-1:
            report_error("", filelinenum, volnum, shortfilename, "pagenumbering", "leap in page numbers from "+str(oldpagenum)+" to "+str(pagenum), "")
    state['linenum']= linenum
    check_simple_regexp(line, pagelinenum, filelinenum, volnum, options, shortfilename)
    text = ''
    if len(line) > endpnumi+1:
        text = line[endpnumi+1:]
        if '{T' in text:
            if not '}' in text:
                report_error(pagelinenum, filelinenum, volnum, shortfilename, "format", "missing closing \"}\"", "")

            closeidx = text.find('}')
            if not '-' in text and not text.startswith('༄༅༅། །', closeidx+1):
                rightcontext = text[closeidx+1:closeidx+5]
                report_error(pagelinenum, filelinenum, volnum, shortfilename, "punctuation", "possible wrong beginning of text: \""+rightcontext+"\" should be \"༄༅༅། །\"", "")
            locstr = str(pagenum)+pageside+str(linenum)+" ("+str(volnum)+")"
        for tohm in TOH_RE.finditer(text):
            tohmatch(tohm, state, pagelinenum, filelinenum, volnum, shortfilename)
        if 'keep_errors_indications' not in options or not options['keep_errors_indications']:
            text = text.replace('[', '').replace(']', '')
        if 'fix_errors' not in options or not options['fix_errors']:
            text = PAREN_RE.sub(lambda m: parrepl(m, 'first', pagelinenum, filelinenum, volnum, shortfilename), text)
        else:
            text = PAREN_RE.sub(lambda m: parrepl(m, 'second', pagelinenum, filelinenum, volnum, shortfilename), text)
        check_verses(text, pagelinenum, filelinenum, state, volnum, options, shortfilename)
        if text.find('(') != -1 or text.find(')') != -1:
            report_error(pagelinenum, filelinenum, volnum, shortfilename, "format", "spurious parenthesis", "")

def parse_one_file(infilename, state, volnum, options, shortfilename):
    with open(infilename, 'r', encoding="utf-8") as inf:
        state["curnbsyllables"] = 0
        state["prevnbsyllables"] = 0
        state["curbeginpagelinenum"] = ""
        state["curbeginline"] = ""
        state["curbeginchar"] = -1
        state["curbeginsylchar"] = -1
        state["curbeginfilelinenum"] = 0
        state["curendsylchar"] = -1
        state["curbeginsylline"] = ""
        state["nbshad"] = 0
        state["lastistshek"] = False
        linenum = 1
        for line in inf:
            if linenum == 1:
                line = line[1:]# remove BOM
            # [:-1]to remove final line break
            parse_one_line(line[:-1], linenum, state, volnum, options, shortfilename)
            linenum += 1

errfile = open("errors.txt","w", encoding="utf-8")

def printerror(err):
    errfile.write(err+"\n")

def report_error(linestr, filelinenum, volnum, shortfilename, errortype, errorstr, linewithhighlight):
    printerror(shortfilename+", l. "+str(filelinenum)+" ("+linestr+"): "+errortype+": "+errorstr)
    if len(linewithhighlight) > 1:
        printerror("  -> "+linewithhighlight)

if __name__ == '__main__':
    """ Example use """
    options = {
        "fix_errors": False,
        "keep_errors_indications": False
    }
    state = {
        "lasttohidx": 0,
        "lasttohsubidx": 0,
        "lasttohletter": "",
        "lasttohstr": ""
    }
    # regexp tests:
    # check_simple_regexp("༄༅། །འདུལ་བ་ཀ་བཞུགས་སོ། བ།ཀ བཀྲ་ཤིས་བདེ་ལེགས།", 1, 1, options)
    # check_simple_regexp("༄༅། །འདུལ་བ་ཀ་བཞུགས་སོ། །ྫ བཀྲ་ཤིས་བདེ་ལེགས།", 2, 1, options)
    # check_simple_regexp("༄༅། །འདུལ་བ་ཀ་བཞུགས་སོ། · བཀྲ་ཤིས་བདེ་ལེགས།", 3, 1, options)
    # check_simple_regexp("༄༅། །འདུལ་བ་ཀ་བཞུགས་སོ། ཀུུ བཀྲ་ཤིས་བདེ་ལེགས།", 4, 1, options)
    # check_simple_regexp("༄༅། །འདུལ་བ་ཀ་བཞུགས་སོ། འོ། །དེ བཀྲ་ཤིས་བདེ་ལེགསval། ", 4, 1, options)
    # check_simple_regexp("༄༅། །འདུལ་བ་ཀ་བཞུགས་སོ། ཀ། །།དེ བཀྲ་ཤིས་བདེ་ལེགསval། ", 4, 1, options)
    # check_simple_regexp("༄༅། །འདུལ་བ་ཀ་བཞུགས་སོ། ཀོ། །།དེ བཀྲ་ཤིས་བདེ་ལེགསval། ", 4, 1, options)
    # check_simple_regexp("༄༅། །འདུལ་བ་ཀ་བཞུགས་སོ། ཀོ།། །།དེ བཀྲ་ཤིས་བདེ་ལེགསinv། ", 4, 1, options)
    # check_simple_regexp("༄༅། །འདུལ་བ་ཀ་བཞུགས་སོ། ཀ།། །།དེ བཀྲ་ཤིས་བདེ་ལེགསinv། ", 4, 1, options)
    # check_simple_regexp("༄༅། །འདུལ་བ་ཀ་བཞུགས་སོ། འོ། །།དེ བཀྲ་ཤིས་བདེ་ལེགསinv། ", 4, 1, options)
    # check_simple_regexp("༄༅། །འདུལ་བ་ཀ་བཞུགས་སོ། ངེ་། བཀྲ་ཤིས་བདེ་ལེགསval། ", 4, 1, options)
    # check_simple_regexp("༄༅། །འདུལ་བ་ཀ་བཞུགས་སོ། ང་། བཀྲ་ཤིས་བདེ་ལེགསval། ", 4, 1, options)
    # check_simple_regexp("༄༅། །འདུལ་བ་ཀ་བཞུགས་སོ། ངང་། བཀྲ་ཤིས་བདེ་ལེགསval། ", 4, 1, options)
    # check_simple_regexp("༄༅། །འདུལ་བ་ཀ་བཞུགས་སོ། ངས་། བཀྲ་ཤིས་བདེ་ལེགསinv། ", 4, 1, options)
    # check_simple_regexp("༄༅། །འདུལ་བ་ཀ་བཞུགས་སོ། ངསི་། བཀྲ་ཤིས་བདེ་ལེགསinv། ", 4, 1, options)
    for volnum in range(1, 103):
        volnumstr = '{0:03d}'.format(volnum)
        infilename = '../derge-kangyur-tags/'+volnumstr+'-tagged.txt'
        #print("checking "+infilename)
        parse_one_file(infilename, state, volnum, options, volnumstr+'-tagged')

errfile.close()