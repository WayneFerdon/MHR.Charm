<!--
 * @Author: wayneferdon wayneferdon@hotmail.com
 * @Date: 2022-07-22 11:32:37
 * @LastEditors: wayneferdon wayneferdon@hotmail.com
 * @LastEditTime: 2022-07-22 12:33:27
 * ----------------------------------------------------------------
 * Copyright (c) 2022 by Wayne Ferdon Studio.
 * See the LICENSE file in the project root for more information.
-->

# 配置文件使用说明 Config Files Usage

## 简体中文

### I. 更改设置

打开并编辑Config.json更改设置，保存后将自动刷新

### II. 更改数据库

编辑Skills.json或Language中的文本文件也将自动刷新

### III. 显示

要正确显示护石在装备箱中的位置

    1. 使用自动导出的json，或保证数据顺序和箱中顺序一致
    2. 保证护石之间没有空格或其他装备，推荐自动排序后导出
    3. 需要确保正确配置了Config.json的Offset项

### IV. Config.json说明

1. Offset : 第一个护石前的格子数，一页为50格
2. ShowGuide : 是否显示使用说明
3. Language : 语言，和Language文件夹中的json文件名一致(不含.json后缀)
4. DisplayDetails : 是否显示替换的详情（否则不显示替换项）
5. CommonOnly : 只显示能被通用护石（S321或S400）仅用插槽即可替换的护石
6. MaxDisplayCount : 单次最大显示的可替换护石数量
7. TargetRaritys : 需要检查的护石稀有度，未开启的将不会作为替换或被替换项
8. TargetRarityNames : 对应的具体稀有度

### V. Skills.json说明

数据结构为:

    "技能CID" : {
        "level" : [1级珠技能等级, 2级珠技能等级, 3级珠技能等级, 4级珠技能等级],
        "limit" : 技能等级上限,
    }
不存在对应珠子的，等级填0

### VI. Language文件说明

1. 0~15 : 界面文本
2. 10000 : Excel文件字段名称文本
3. 20000+技能CID : 技能名称，不存在的技能将标注为 Null_xxx
4. 30000+技能CID : 对应饰品的名称，不存在的饰品将标注为 -1

### VII. CharmData.json说明

数据结构与mod"Charm Editor and Item Cheat"的导出数据一致(N网：<https://www.nexusmods.com/monsterhunterrise/mods/17>)
PS: 需要REFramework(N网：<https://www.nexusmods.com/monsterhunterrise/mods/26>)

具体结构:

    {
        "Rarity":稀有度ID，具体可见Config.json中的标注,
        "SkillLevels":按顺序的技能等级,
        "Skills":按顺序的技能CID,
        "Slots":[孔位等级1,孔位等级2,孔位等级3]
    }
孔位数量少于3的用0补充

### VIII. CharmData.xlsx说明

1. 请勿修改灰色格子/带公式的部分/隐藏的部分
2. 若填写了配装器导出数据，将优先读取此部分数据
3. 配装器数据格式和mh.wiki的一致（网址：<https://mhrise.wiki-db.com/sim/>，中文网页：<https://mhrise.wiki-db.com/sim/?hl=zh-hans>)
4. 具体格式：技能名1,技能等级1,技能名2,技能等级2,孔等级1,孔等级2,孔等级3
5. 推荐可在护石页面添加后进行导出并复制粘贴
6. excel中的插槽等级格式为无逗号的孔位等级，例如：400、040、04、4都代表单个4级孔

### IX. 其他说明

1. 成功读取CharmsData.xlsx或CharmsData.json后将按配装器格式(VIII. 3.)导出数据至CharmsData.txt

## English

### Change Settings

Edit Config.json to Change Settiings, Refresh will be automatically when saved

### II. Change Datas

Edito Skills.json or ./Language/*.json will automatically refresh as well

### III. Display

To correctly display positions in the equipment box

    1. Use json which output directly from game, or ensure the order is the same
    2. Make sure no gap or other equipment exist between 2 charm, recommend to output automatically
    3. Make sure "Offset" in Config.json is set correctly

### IV. Config.json

1. Offset : Grids before the first charm, 50 grids each page
2. ShowGuide : Is display guid or not
3. Language : Display and output language, same as the name of json file in ./Language/ (without .json)
4. DisplayDetails : Display details of replacements or not
5. CommonOnly : Is only display charms that can be replace by common charms (S321 or S400) with and only with the slot
6. MaxDisplayCount : The max count of displaying replaceable charms
7. TargetRaritys : Is checking charms with raritys or not
8. TargetRarityNames : The meaning of the raritys' ID

### V. Skills.json

Data's struct:

    "SkillCID" : {
        "level" : [SkillLevelWith【1】Jewl, SkillLevelWith【2】Jewl, SkillLevelWith【3】Jewl, SkillLevelWith【4】Jewl],
        "limit" : MaxSkillLevel,
    }
SkillLevel = 0 while jewl with the same 【level】 is not exist

### VI. Language

1. 0~15 : UI Strings
2. 10000 : Excel Param Name
3. 20000+技能CID : Skill names, illegal skill is named Null_xxx
4. 30000+技能CID : Jewl names，, illegal jewl is named  -1

### VII. CharmData.json

Data's struct is as same as output from mod "Charm Editor and Item Cheat"(NexusMods : <https://www.nexusmods.com/monsterhunterrise/mods/17>)
PS: Require REFramework(NexusMods : <https://www.nexusmods.com/monsterhunterrise/mods/26>)

struct:

    {
        "Rarity" : Rarity ID (see Config.json -> TargetRarityNames),
        "SkillLevels" : Skill Levels (ordered),
        "Skills": Skill CIDs (ordered),
        "Slots": [Slot1【level】,Slot2【level】,Slot3【level】]
    }

Fill with 0 if slots' count is less than 3

### VIII. CharmData.xlsx

1. DO NOT EDIT Grey Grids or Grids with formula or hidden parts
2. Column "配装器导出数据" will be read primary if it's not empty
3. Struct of "配装器导出数据" is as same as the one in mh.wiki (<https://mhrise.wiki-db.com/sim/>, Eng : <https://mhrise.wiki-db.com/sim/?hl=en>)
4. Struct : SkillName1, SkillLevel1, SkillName2, SkillLevel2, Slot1【level】,Slot2【level】,Slot3【level】
5. Recommend use "Charms" to add charms and output
6. Struct of "插槽等级" in xlsx as slots' 【level】 with nothing seperating, such as 400, 040, 04, 4 are all means S400

### IX. Else

1. When successfully read CharmsData.xlsx or CharmsData.json, data will be output into CharmsData.txt with Struct(VIII. 3.)
