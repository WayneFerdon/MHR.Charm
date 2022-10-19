# ----------------------------------------------------------------
# Author: wayneferdon wayneferdon@hotmail.com
# Date: 2022-01-21 03:18:12
# LastEditors: wayneferdon wayneferdon@hotmail.com
# LastEditTime: 2022-10-12 05:22:24
# FilePath: \undefinedh:\Wayne Custaf Laqinoa Ferdon\Game\MHR\`Charms.py
# ----------------------------------------------------------------
# Copyright (c) 2022 by Wayne Ferdon Studio. All rights reserved.
# Licensed to the .NET Foundation under one or more agreements.
# The .NET Foundation licenses this file to you under the MIT license.
# See the LICENSE file in the project root for more information.
# ----------------------------------------------------------------

'''
Author: wayneferdon wayneferdon@hotmail.com
Date: 2022-01-21 03:18:12
LastEditors: wayneferdon wayneferdon@hotmail.com
LastEditTime: 2022-08-10 21:14:07
FilePath: \MHR\`Charms.py
----------------------------------------------------------------
Copyright (c) 2022 by Wayne Ferdon Studio. All rights reserved.
Licensed to the .NET Foundation under one or more agreements.
The .NET Foundation licenses this file to you under the MIT license.
See the LICENSE file in the project root for more information.
'''
# @Author: wayneferdon wayneferdon@hotmail.com
# @Date: 2022-07-22 11:32:37
# @LastEditors: wayneferdon wayneferdon@hotmail.com
# @LastEditTime: 2022-07-22 12:33:27
# ----------------------------------------------------------------
# Copyright (c) 2022 by Wayne Ferdon Studio.
# See the LICENSE file in the project root for more information.

# region imports
from enum import Enum
import json, xlrd
import os, time, ctypes, traceback
import win32com.client as Client
# endregion imports

# region Global and Constants
class FileType(Enum):
    Excel = 0,
    Json = 1

EXCEL_FILE_PATH = './CharmsData.xlsx'
JSON_FILE_PATH = './CharmsData.json'
TXT_FILE_PATH = './CharmsData.txt'
SKILL_PATH = './Skills.json'
CONFIG_PATH = './Config.json'
LANGUAGE_PATH = './Language/{}.json'
LINE_LENGTH = 70

FILE_PATHS = {
    FileType.Excel:EXCEL_FILE_PATH,
    FileType.Json:JSON_FILE_PATH
}

g_SkillData = dict()
g_Items = dict()
g_LastFile = EXCEL_FILE_PATH
g_Config = {}
g_Strings = {}
g_Exclusion = {}
g_LastRefreshTime = 0
g_LastConfigTime = 0

MAX_SKILL_COUNT = 2
MAX_SLOT_LEVEL = 4
MAX_SLOT_COUNT = 3
COMMON_SLOT_ITEMS = [
    {
        'slot':[3,-1,-1]
    },
    {
        'slot':[2,1,0]
    },
]

# region print color
STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12
# text colors
FOREGROUND_GREY = 0x08  # grey.
FOREGROUND_BLUE = 0x09  # blue.
FOREGROUND_GREEN = 0x0a  # green.
FOREGROUND_RED = 0x0c  # red.
FOREGROUND_YELLOW = 0x0e  # yellow.
# background colors
BACKGROUND_BLUE = 0x90  # yellow.
BACKGROUND_GREEN = 0xa0  # yellow.
BACKGROUND_RED = 0xc0  # yellow.
BACKGROUND_YELLOW = 0xe0  # yellow.
# get handle
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
shell = Client.Dispatch('WScript.Shell')
# endregion print color
# endregion Global and Constants

# region Methods
def SetCMDDisplay(type):
    ctypes.windll.kernel32.SetConsoleTextAttribute(std_out_handle, type)

def ResetCMDDisplay():
    SetCMDDisplay(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)

def GetRowInfo(row):
    page = int((row+1+GetConfig(Config.Offset))/50)
    pageMod = (row+1+GetConfig(Config.Offset))%50
    if pageMod != 0:
        page += 1
        pageRow = int(pageMod/10)
    else:
        pageRow = 5
    pageCol = pageMod%10
    if pageCol != 0:
        pageRow += 1
    else:
        pageCol = 10
    if g_LastFile == JSON_FILE_PATH:
        return GetString(7).format(page,pageRow,pageCol,GetItemInfo(g_Items[row]))
    return GetString(8).format(row+1,GetItemInfo(g_Items[row]))

def GetItemData(item):
    skillDatas = list()
    slotDatas = list()
    for skill in item:
        if skill == 'slot':
            for each in item['slot']:
                slotDatas.append(str(each + 1))
            continue
        skillDatas.append(GetString(int(skill) + 20000))
        skillDatas.append(str(item[skill]))
    skillDatas += ['','0'] * (2 * MAX_SKILL_COUNT - len(skillDatas))
    return ','.join(skillDatas + slotDatas)

def GetItemInfo(item, isCommonSlotItem=False):
    skillInfos = list()
    slotInfo = list()
    for skill in item:
        if skill == 'slot':
            for slotLevel in item['slot']:
                if slotLevel == -1:
                    slotInfo.append(' ー  ')
                else:
                    slotInfo.append('【{}】'.format(slotLevel + 1))
            continue

        level = item[skill]
        limit = g_SkillData[skill]['limit']
        slotImage = '■' * level + '□' * (limit - level)
        slotImage += '\tLv  {}'.format(level)
        skillInfos.append(GetString(int(skill) + 20000))
        skillInfos.append(slotImage)

    info = ''.join(slotInfo)
    if isCommonSlotItem:
        return info
    info = '\t' + GetString(9) + '\t' + info
    info += '\n\t' + GetString(10) + '\t' + '\n\t\t'.join(skillInfos)
    return info

def LoadJson(lines):
    row = -1
    txtOutput = list()
    for itemData in json.loads(''.join(lines)):
        row += 1
        item, text = LoadLineData(itemData)
        txtOutput.append(text)
        if item != None:
            g_Items[row] = item
    WriteTxt(txtOutput)

def LoadLineData(itemData):
    text = None
    item = dict()
    skillLevels = itemData['SkillLevels']
    global g_SkillData
    for i in range(MAX_SKILL_COUNT):
        for skillCID in g_SkillData:
            if int(skillCID) == itemData['Skills'][i]:
                if skillCID != '0' and skillLevels[i] != 0:
                    item[skillCID] = skillLevels[i]
                break
    item['slot'] = [0] * 3
    for i in range(MAX_SLOT_COUNT):
        item['slot'][i] = int(itemData['Slots'][i]) - 1
    item['slot'].sort(reverse=True)
    text = GetItemData(item)
    if 'Rarity' in itemData.keys():
        rarity = itemData['Rarity']
        text = '{},{}'.format(text,rarity)
        if str(rarity) not in GetConfig(Config.TargetRaritys):
            return None, text + '\n'
        if not GetConfig(Config.TargetRaritys)[str(rarity)]:
            return None, text + '\n'
    return item, text + '\n'

def LoadSheet(sheet):
    nrows = sheet.nrows  # 行数
    ncols = sheet.ncols  # 列数
    if ncols == 0 or nrows == 0:
        return
    LoadExcelSkillDatas(sheet, nrows, ncols)
    if g_LastFile == EXCEL_FILE_PATH:
        LoadExcelItemDatas(sheet, nrows, GetColDef(sheet, ncols, 10000))

def LoadExcelSkillDatas(sheet, nrows, ncols):
    cidCol = GetColDef(sheet, ncols, 11001)
    limitCol = GetColDef(sheet, ncols, 11002)
    jewlCol = GetColDef(sheet, ncols, 11003)
    if None in [cidCol, limitCol, jewlCol]:
        return
    skills = dict()
    for row in range(nrows):
        if row == 0:
            continue
        cidCell = sheet.cell(row, cidCol)
        limitCell = sheet.cell(row, limitCol)
        jewlCell = sheet.cell(row, jewlCol)
        if '' in [cidCell.value, limitCell.value, jewlCell.value]:
            continue
        cid = str(int(cidCell.value))
        skills[cid] = {
            "level":[int(x) for x in (jewlCell.value).split(',')],
            "limit":int(limitCell.value)
        }
    with open(SKILL_PATH,'w',encoding='utf-8') as f:
        f.write(json.dumps(skills))
    return

def GetColDef(sheet, ncols, nameStringID):
    colName = GetString(nameStringID)
    done = 0
    for col in range(ncols):
        if done == 5:
            break
        paramName = sheet.cell(0,col).value
        if paramName == colName:
            return col
    return None

def IsLegalCell(cell):
    if cell.ctype == xlrd.XL_CELL_ERROR:
        return False
    elif cell.value == '':
        return False
    return True

def LoadExcelItemDatas(sheet, nrows, dataCol):
    if dataCol is None:
        return
    txtOutput = list()
    for row in range(nrows):
        if row == 0:
            continue
        itemCell = sheet.cell(row,dataCol)
        if itemCell.value == '':
            continue
        itemData = json.loads(itemCell.value)
        item, text = LoadLineData(itemData)
        txtOutput.append(text)
        if item != None:
            g_Items[row] = item
    WriteTxt(txtOutput)

def ReadItemData(data):
    item = dict()
    for i in range(MAX_SKILL_COUNT):
        skill = data[2 * i]
        level = (int)(data[2 * i + 1])
        if skill != '' and level != 0:
            item[skill] = level

    item['slot'] = [0] * 3
    for i in range(MAX_SLOT_COUNT):
        item['slot'][i] = int(data[2 * MAX_SKILL_COUNT + i]) - 1
    item['slot'].sort(reverse=True)
    return item

def WriteTxt(txtOutput):
    with open(TXT_FILE_PATH, 'w',encoding='utf-8') as f:
        f.writelines(txtOutput)

def GetRemainCount(slotsA,slotsB):
    # fill slots, fill lower levels first, than higher levels
    remain = list()
    for i in range(MAX_SLOT_COUNT):
        n = -i-1
        if slotsB[n] < slotsA[n]:
            return None
        if slotsA[n] == -1 and slotsB[n] != -1:
            remain.append(slotsB[n])
    return len(remain)

def GetSkillsNeedJewel(itemA, itemB):
    skillsNeedJewel = dict()
    for skill in itemA:
        if skill == 'slot':
            continue
        countsNeedJewel = itemA[skill]
        if skill in itemB.keys():
            countsNeedJewel -= itemB[skill]
        if countsNeedJewel > 0:
            skillsNeedJewel[skill] = countsNeedJewel
    return skillsNeedJewel

def GetUsableJewls(skillsNeedJewel):
    usableJewls = list()
    for skill in skillsNeedJewel:
        for slotLevel in range(MAX_SLOT_LEVEL):
            skillLevel = g_SkillData[skill]['level'][slotLevel]
            if skillLevel <= 0:
                continue
            usableJewls.append([skill,skillLevel,slotLevel])
    return usableJewls

def GetCombs(usableJewls, remain, skillsNeedJewelCount):
    remain = min(remain, skillsNeedJewelCount)
    combs = list()
    for i in range(len(usableJewls)):
        for j in range(len(usableJewls)):
            for k in range(len(usableJewls)):
                combs.append([usableJewls[i],usableJewls[j],usableJewls[k]])
            if remain <= 1:
                break
        if remain < MAX_SLOT_COUNT:
            newCombs = list()
            for comb in combs:
                newCombs.append(comb[MAX_SLOT_COUNT-remain:MAX_SLOT_COUNT])
            combs = newCombs
            break
    return combs

def GetCheckedCombo(comb,slotA,slotB, skillsNeedJewel):
    need = list()
    for jewl in comb:
        slotLevel = jewl[2]
        need.append(slotLevel)
    need += slotA
    while -1 in need and len(need) > MAX_SLOT_COUNT:
        need.remove(-1)
    if len(need) > MAX_SLOT_COUNT:
        return None
    need.sort(reverse=True)
    if GetRemainCount(need, slotB) is None:
        return None
    
    skillLevels = dict()
    for jewl in comb:
        skill = jewl[0]
        skillLevel = jewl[1]
        if skill not in skillLevels.keys():
            skillLevels[skill] = 0
        skillLevels[skill] += skillLevel
    
    for skill in skillsNeedJewel:
        if skill not in skillLevels.keys():
            return None
        if skillsNeedJewel[skill] > skillLevels[skill]:
            return None
    return comb

def GetCheckedCombos(combs,slotA,slotB,skillsNeedJewel):
    checked = list()
    for comb in combs:
        checkedComb = GetCheckedCombo(comb,slotA,slotB, skillsNeedJewel)
        if checkedComb is not None:
            checked.append(comb)
    for each in checked:
        each.sort()
    distincted = list()
    for each in checked:
        if each in distincted:
            continue
        distincted.append(each)
    return distincted

def GetJewlInfo(jewl):
    jewlName = GetString(int(jewl[0]) + 30000)
    if jewl[1] < 3:
        skillLevel = 'I' * jewl[1]
    elif jewl[1] == 3:
        skillLevel = 'IV'
    elif jewl[1] == 4:
        skillLevel = 'V'
    elif jewl[1] == 5:
        skillLevel = 'VI'
    elif jewl[1] == 6:
        skillLevel = 'VII'
    jewlLevel = jewl[2]+1
    return '{}{}【{}】'.format(jewlName, skillLevel, jewlLevel)

def GetReplacements(combos):
    replacements = list()
    for comb in combos:
        replacements.append(list())
        jewls = dict()
        for jewl in comb:
            jewlInfo = GetJewlInfo(jewl)
            if jewlInfo not in jewls.keys():
                jewls[jewlInfo] = 0
            jewls[jewlInfo] += 1
        for jewlInfo in jewls:
            replacements[-1].append('{}× {}'.format(jewlInfo, jewls[jewlInfo]))
    return replacements

def CheckIsSame(itemA, itemB):
    for skill in itemA:
        if skill not in itemB.keys():
            return False
        if skill == 'slot':
            slotsA = itemA['slot'].copy()
            slotsB = itemB['slot'].copy()
            slotsA.sort()
            slotsB.sort()
            for i in range(MAX_SLOT_COUNT):
                if slotsA[i] != slotsB[i]:
                    return False
            continue
        if itemA[skill] != itemB[skill]:
            return False
    return True

def GetOutPut(rowA, rowB, itemB=None):
    if rowB == rowA or (rowA in g_Exclusion.keys() and rowB in g_Exclusion[rowA]):
        return None
    itemA = g_Items[rowA]
    if itemB is None:
        itemB = g_Items[rowB]
    slotA = itemA['slot']
    slotB = itemB['slot']
    remain = GetRemainCount(slotA, slotB)
    if remain is None:
        return None
    skillsNeedJewel = GetSkillsNeedJewel(itemA, itemB)
    if remain == 0 and len(skillsNeedJewel) != 0:
        return None

    usableJewls = GetUsableJewls(skillsNeedJewel)
    skillsNeedJewelCount = 0
    for skill in skillsNeedJewel:
        skillsNeedJewelCount += skillsNeedJewel[skill]

    combs = GetCombs(usableJewls, remain, skillsNeedJewelCount)
    checkedCombs = GetCheckedCombos(combs,slotA,slotB,skillsNeedJewel)
    if len(checkedCombs) == 0 and len(skillsNeedJewel) != 0:
        return None

    isSame = rowB != -1 and CheckIsSame(itemA, itemB) and CheckIsSame(itemB, itemA)
    if isSame:
        if rowB not in g_Exclusion.keys():
            g_Exclusion[rowB] = list()
        if rowA not in g_Exclusion[rowB]:
            g_Exclusion[rowB].append(rowA)

    result = list()
    if rowB == -1:
        result.append([GetString(11).format(GetItemInfo(itemB,True)),FOREGROUND_BLUE])
    else:
        result.append(['-' * LINE_LENGTH,FOREGROUND_BLUE])
        result.append([GetRowInfo(rowB),FOREGROUND_GREEN])
    if isSame:
        result.append(['\t' + GetString(17),FOREGROUND_YELLOW])
    elif len(skillsNeedJewel.keys())==0:
        result.append(['\t' + GetString(12),FOREGROUND_YELLOW])
    n = 0
    for replacement in GetReplacements(checkedCombs):
        n += 1
        output = '\t' + GetString(13).format(n) + '\t'
        for jewl in replacement:
            output += '{}\t'.format(jewl)
        result.append([output,FOREGROUND_YELLOW])
    return result

def DisplayOutput(result):
    output, rowA, replacementCount = result
    SetCMDDisplay(FOREGROUND_BLUE)
    Display(GetRowInfo(rowA))
    if GetConfig(Config.DisplayDetails):
        if replacementCount != 0:
            Display(GetString(14).format(replacementCount))
        for line in output:
            SetCMDDisplay(line[1])
            Display(line[0])
    SetCMDDisplay(FOREGROUND_RED)
    Display('=' * LINE_LENGTH)

def CheckNeedUpdate(lastRefreshTime):
    dataTimes = list()
    dataTimes.append(os.stat(CONFIG_PATH).st_mtime)
    # dataTimes.append(os.stat(SKILL_PATH).st_mtime)
    if 'Language' in g_Config.keys():
        langFile = LANGUAGE_PATH.format(GetConfig(Config.Language))
        if os.path.exists(langFile):
            dataTimes.append(os.stat(langFile).st_mtime)
    configTime = max(dataTimes)
    fileTime = 0
    try:
        pathExist = False
        for fileType in FileType:
            path = FILE_PATHS[fileType]
            if not os.path.exists(path):
                continue
            pathExist = True
            fileTime = os.stat(path).st_mtime
            if fileTime > lastRefreshTime:
                lastRefreshTime = fileTime
                global g_LastFile
                g_LastFile = FILE_PATHS[fileType]
        SetCMDDisplay(FOREGROUND_RED)
        if not pathExist:
            print(GetString(0),end='\r')
            lastRefreshTime = None
    except Exception:
        pass
    return configTime, lastRefreshTime

def RelpadData():
    g_Items.clear()
    with xlrd.open_workbook(EXCEL_FILE_PATH) as book:
        for sheet in book.sheets():
            LoadSheet(sheet)
    if g_LastFile == JSON_FILE_PATH:
        with open(JSON_FILE_PATH, 'r') as f:
            LoadJson(f.readlines())

def GetResults():
    results = list()
    count = 0
    for rowA in g_Items:
        if count == GetConfig(Config.MaxDisplayCount):
            break
        isCommon = False
        replacementCount = 0
        for item in COMMON_SLOT_ITEMS:
            outputs = GetOutPut(rowA,-1,item)
            if outputs is None:
                continue
            isCommon = True
            count += 1
            if count <= GetConfig(Config.MaxDisplayCount):
                results.append([outputs,rowA,replacementCount])
            break
        if isCommon or GetConfig(Config.CommonOnly):
            continue
        outputs = list()
        for rowB in g_Items:
            output = GetOutPut(rowA,rowB)
            if output is None:
                continue
            outputs += output
            replacementCount += 1
            if replacementCount == 1:
                count += 1
        if replacementCount > 0:
            if count <= GetConfig(Config.MaxDisplayCount):
                results.append([outputs,rowA,replacementCount])
    return results, count

def UpdateConfig():
    with open(SKILL_PATH,'r',encoding='utf-8') as f:
        global g_SkillData
        g_SkillData = json.loads(''.join(f.readlines()))
    with open(CONFIG_PATH,'r',encoding='utf-8') as f:
        global g_Config
        g_Config = json.loads(''.join(f.readlines()))
    langPath = LANGUAGE_PATH.format(GetConfig(Config.Language))
    global g_Strings
    if not os.path.exists(langPath):
        g_Strings = {}
        return
    with open(langPath,'r',encoding='utf-8') as f:
        g_Strings = json.loads(''.join(f.readlines()))

class Config(Enum):
    Language = 0,
    DisplayDetails = 1
    CommonOnly = 2
    MaxDisplayCount = 3
    Offset = 4
    TargetRaritys = 5
    ShowGuide = 6

def GetConfig(configType):
    return g_Config[configType.name]

def GetString(id):
    key = str(id)
    if key not in g_Strings.keys():
        return GetConfig(Config.Language) + '_' + key
    return g_Strings[key] 

def Display(data):
    print(data)

def ClearDisplay():
    os.system('cls')

def Main():
    global g_LastRefreshTime
    global g_LastConfigTime
    while True:
        try:
            configTime, lastModifiedtime = CheckNeedUpdate(g_LastRefreshTime)
            if configTime > g_LastConfigTime:
                g_LastConfigTime = configTime
                UpdateConfig()
                if lastModifiedtime is None or lastModifiedtime < configTime:
                    lastModifiedtime = configTime
            if lastModifiedtime == g_LastRefreshTime:
                continue
            g_LastRefreshTime = lastModifiedtime
            SetCMDDisplay(FOREGROUND_RED)
            ClearDisplay()
            Display('=' * LINE_LENGTH)
            Display(GetString(1))
            Display('=' * LINE_LENGTH)
            RelpadData()
            results, count = GetResults()
            ClearDisplay()
            Display('=' * LINE_LENGTH)
            for result in results:
                DisplayOutput(result)
            SetCMDDisplay(FOREGROUND_RED)
            if count >= GetConfig(Config.MaxDisplayCount):
                Display(GetString(2).format(GetConfig(Config.MaxDisplayCount)))
            else:
                Display(GetString(3).format(count))
            if GetConfig(Config.CommonOnly):
                Display(GetString(4))
            Display(GetString(5))
            Display(GetString(6).format(g_LastFile))
            Display('=' * LINE_LENGTH)
            if GetConfig(Config.ShowGuide):
                Display(GetString(15))
            else:
                Display(GetString(16))
            Display('=' * LINE_LENGTH)
        except Exception:
            g_LastRefreshTime = 0
            SetCMDDisplay(FOREGROUND_RED)
            print(traceback.format_exc())
        time.sleep(0.1)
# endregion Methods

if __name__ == '__main__':
    Main()