import requests
import re
import json
from bs4 import BeautifulSoup
from time import sleep


def getItemQuestsInfo(itemId):
    itemPage = getItemPage(itemId)
    itemElements = itemPage.find_all(
        lambda tag: tag.name == "script" and "objective-of" in tag.text
    )
    itemTitleElement = itemPage.find("meta", {"property": "og:title"})
    itemName = itemTitleElement["content"]

    if len(itemElements) > 1:
        return "it's fucked"

    line = getObjectiveOfDataLine(itemElements)
    rawJson = cleanDataString(line)
    quests = json.loads(rawJson)

    questIds = []
    for quest in quests:
        questPage = getQuestPage(quest["id"])
        questElements = questPage.find_all("tr", {"data-icon-list-quantity": True})
        quantity = getQuantityForItem(itemName, questElements)
        questIds.append(
            {"id": quest["id"], "name": quest["name"], "quantityNeeded": quantity}
        )

    return questIds


def getQuantityForItem(itemName, questElements):
    for questElement in questElements:
        if itemName in questElement.text:
            matches = re.findall(r"\(\d+\)", questElement.text)
            match = matches[-1]
            return match.removeprefix("(").removesuffix(")")


def getItemPage(itemId):
    response = requests.get(f"https://www.wowhead.com/classic/item={item_id}")
    sleep(2)
    return BeautifulSoup(response.content, "html.parser")


def getQuestPage(questId):
    response = requests.get(f"https://www.wowhead.com/classic/quest={questId}")
    sleep(2)
    return BeautifulSoup(response.content, "html.parser")


def getObjectiveOfDataLine(elements):
    for element in elements:
        lines = element.text.split("\n")
        for line in lines:
            if "data:" in line and '"name"' in line and '"xp"' in line:
                return line


def cleanDataString(string):
    return re.sub("\s+data:\s+", "", string).removesuffix(",")


itemIds = [
    159,
    723,
    729,
    730,
    # 731,
    # 732,
    # 769,
    # 814,
    # 929,
    # 1015,
    # 1080,
    # 1081,
    # 1179,
    # 1206,
    # 1251,
    # 1262,
    # 1274,
    # 1468,
    # 1529,
    # 1708,
    # 1939,
    # 1941,
    # 1942,
    # 2070,
    # 2251,
    # 2296,
    # 2309,
    # 2310,
    # 2314,
    # 2318,
    # 2319,
    # 2320,
    # 2321,
    # 2447,
    # 2449,
    # 2454,
    # 2455,
    # 2458,
    # 2589,
    # 2592,
    # 2594,
    # 2604,
    # 2633,
    # 2665,
    # 2686,
    # 2688,
    # 2725,
    # 2728,
    # 2730,
    # 2732,
    # 2734,
    # 2735,
    # 2738,
    # 2740,
    # 2742,
    # 2744,
    # 2745,
    # 2748,
    # 2749,
    # 2750,
    # 2751,
    # 2798,
    # 2799,
    # 2840,
    # 2842,
    # 2845,
    # 2851,
    # 2857,
    # 2868,
    # 2886,
    # 2894,
    # 2924,
    # 2997,
    # 3164,
    # 3172,
    # 3173,
    # 3174,
    # 3240,
    # 3340,
    # 3356,
    # 3357,
    # 3371,
    # 3372,
    # 3383,
    # 3388,
    # 3404,
    # 3421,
    # 3466,
    # 3482,
    # 3483,
    # 3486,
    # 3530,
    # 3575,
    # 3576,
    # 3577,
    # 3703,
    # 3712,
    # 3713,
    # 3719,
    # 3820,
    # 3823,
    # 3825,
    # 3827,
    # 3829,
    # 3835,
    # 3836,
    # 3842,
    # 3851,
    # 3853,
    # 3855,
    # 3857,
    # 3860,
    # 3864,
    # 4234,
    # 4239,
    # 4265,
    # 4278,
    # 4304,
    # 4306,
    # 4338,
    # 4363,
    # 4369,
    # 4371,
    # 4375,
    # 4384,
    # 4389,
    # 4392,
    # 4394,
    # 4395,
    # 4407,
    # 4457,
    # 4470,
    # 4471,
    # 4479,
    # 4480,
    # 4481,
    # 4582,
    # 4589,
    # 4595,
    # 4600,
    # 4611,
    # 4616,
    # 4625,
    # 5051,
    # 5075,
    # 5092,
    # 5093,
    # 5094,
    # 5095,
    # 5117,
    # 5134,
    # 5465,
    # 5469,
    # 5635,
    # 5739,
    # 5768,
    # 5769,
    # 5770,
    # 5996,
    # 5997,
    # 6037,
    # 6040,
    # 6214,
    # 6450,
    # 6451,
    # 6887,
    # 7067,
    # 7068,
    # 7069,
    # 7070,
    # 7075,
    # 7077,
    # 7078,
    # 7079,
    # 7080,
    # 7081,
    # 7228,
    # 7910,
    # 7922,
    # 7926,
    # 7927,
    # 7928,
    # 7930,
    # 7931,
    # 7933,
    # 7935,
    # 7936,
    # 7937,
    # 7941,
    # 7945,
    # 7956,
    # 7957,
    # 7958,
    # 7963,
    # 7966,
    # 7972,
    # 7974,
    # 8150,
    # 8152,
    # 8153,
    # 8165,
    # 8170,
    # 8173,
    # 8175,
    # 8176,
    # 8185,
    # 8187,
    # 8189,
    # 8191,
    # 8193,
    # 8197,
    # 8198,
    # 8203,
    # 8204,
    # 8211,
    # 8214,
    # 8244,
    # 8429,
    # 8430,
    # 8483,
    # 8544,
    # 8545,
    # 8564,
    # 8643,
    # 8644,
    # 8645,
    # 8646,
    # 8683,
    # 8831,
    # 8836,
    # 8846,
    # 8925,
    # 8932,
    # 8956,
    # 9061,
    # 9172,
    # 9224,
    # 9243,
    # 9259,
    # 9264,
    # 9308,
    # 9313,
    # 10450,
    # 10455,
    # 10507,
    # 10559,
    # 10560,
    # 10561,
    # 10562,
    # 10646,
    # 10721,
    # 10725,
    # 11018,
    # 11040,
    # 11109,
    # 11128,
    # 11325,
    # 11370,
    # 11371,
    # 11382,
    # 11404,
    # 11407,
    # 11513,
    # 11514,
    # 11515,
    # 11562,
    # 11563,
    # 11564,
    # 11567,
    # 11590,
    # 11815,
    # 12207,
    # 12209,
    # 12210,
    # 12238,
    # 12359,
    # 12360,
    # 12361,
    # 12363,
    # 12364,
    # 12417,
    # 12422,
    # 12607,
    # 12643,
    # 12644,
    # 12655,
    # 12775,
    # 12792,
    # 12800,
    # 12804,
    # 12810,
    # 12811,
    # 12871,
    # 13422,
    # 13423,
    # 13444,
    # 13446,
    # 13447,
    # 13461,
    # 13506,
    # 13512,
    # 13546,
    # 13724,
    # 13757,
    # 13858,
    # 13864,
    # 13890,
    # 13935,
    # 13965,
    # 14046,
    # 14047,
    # 14048,
    # 14104,
    # 14227,
    # 14256,
    # 14341,
    # 14342,
    # 14529,
    # 14530,
    # 15086,
    # 15088,
    # 15095,
    # 15407,
    # 15408,
    # 15416,
    # 15564,
    # 15992,
    # 15993,
    # 15994,
    # 15997,
    # 16000,
    # 16006,
    # 16666,
    # 16667,
    # 16668,
    # 16669,
    # 16670,
    # 16671,
    # 16672,
    # 16673,
    # 16674,
    # 16675,
    # 16676,
    # 16677,
    # 16678,
    # 16679,
    # 16680,
    # 16681,
    # 16682,
    # 16683,
    # 16684,
    # 16685,
    # 16686,
    # 16687,
    # 16688,
    # 16689,
    # 16690,
    # 16691,
    # 16692,
    # 16693,
    # 16694,
    # 16695,
    # 16696,
    # 16697,
    # 16698,
    # 16699,
    # 16700,
    # 16701,
    # 16702,
    # 16703,
    # 16704,
    # 16705,
    # 16706,
    # 16707,
    # 16708,
    # 16709,
    # 16710,
    # 16711,
    # 16712,
    # 16713,
    # 16714,
    # 16715,
    # 16716,
    # 16717,
    # 16718,
    # 16719,
    # 16720,
    # 16721,
    # 16722,
    # 16723,
    # 16724,
    # 16725,
    # 16726,
    # 16727,
    # 16728,
    # 16729,
    # 16730,
    # 16731,
    # 16732,
    # 16733,
    # 16734,
    # 16735,
    # 16736,
    # 16737,
    # 17010,
    # 17011,
    # 17012,
    # 17058,
    # 17197,
    # 17203,
    # 17422,
    # 17522,
    # 17542,
    # 17771,
    # 18562,
    # 18706,
    # 18944,
    # 18945,
    # 19182,
    # 19228,
    # 19257,
    # 19267,
    # 19277,
    # 19440,
    # 19933,
    # 20407,
    # 20452,
    # 20520,
    # 21377,
    # 21383,
    # 21829,
    # 21833,
    # 21939,
    # 22014,
    # 22682,
]

leftBrace = "{"
rightBrace = "}"

print(leftBrace)
for itemId in itemIds:
    questsInfo = getItemQuestsInfo(itemId)
    print(f"\t[{itemId}] = {leftBrace}")
    for questInfo in questsInfo:
        print(f"\t\t{leftBrace} ")
    # is associated with quests: {questInfo}")
