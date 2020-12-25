from stanfordcorenlp import StanfordCoreNLP
import logging
from gensim import models
import csv

nlp = StanfordCoreNLP(r'stanford-corenlp-full-2018-10-05', lang='zh')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
model = models.Word2Vec.load('word2vec.model')

def init():
    with open('countrycode.csv', 'r') as csvFile:
        countries = list(csv.reader(csvFile))
    return countries

def judge(word1, word2):
    try:
        res = model.similarity(word1,word2)
        print(word1+" "+word2+" "+str(res))
    except:
        res = 0
    return res

def judgeLocation(sen,position):

    # parse = nlp.parse(sen)


    ner = nlp.ner(sen)
    tokenize = nlp.word_tokenize(sen)
    depend = nlp.dependency_parse(sen)
    tag = nlp.pos_tag(sen)

    rootPosition = 0
    dic = []
    for i in range(len(tokenize)):
        t = []
        t.append(i+position)
        t.append(tokenize[i])
        t.append(tag[i][1])
        t.append(ner[i][1])
        for j in range(len(depend)):
            if (depend[j][2] == i + 1):
                t.append(depend[j][1] - 1)
                break
        dic.append(t)
    print(dic)

    for i in range(len(dic)):
        if dic[i][4]==-1:
            if (dic[i][3] == "COUNTRY" or dic[i][3] == "CITY" or dic[i][3] == "STATE_OR_PROVINCE" or dic[i][3] == "LOCATION"): #or dic[i][3] == "GPE"
                locationValue = []
                dic[i].append(1)
                dic[i].append(1.0)
                locationValue.append(dic[i])
                return locationValue
            rootPosition = i
    rootPosition = rootPosition+position

    for i in range(len(dic)):
        if (dic[i][3] == "COUNTRY" or dic[i][3] == "CITY" or dic[i][3] == "STATE_OR_PROVINCE"  or dic[i][3] == "LOCATION"): #or dic[i][3] == "GPE"
            t = dic[i][4]
            while 1:
                if (dic[t][2] == "VV" or dic[t][4]==-1):
                    break
                else:
                    t = dic[t][4]
            dic[i][4] = t

    num = 0
    v = 0
    sen = ""
    for j in range(len(dic)):
        if dic[j][2]=="VV" and dic[j][1]!="报道":
            v = v+1
        if dic[j][1]=="报道" and dic[j][2]!="VV":
            dic[j][1] = "新闻"
        if dic[j][1]=="驻" and dic[j][2]=="VV":
            dic[j][2]="LB"

        sen += dic[j][1]

    print(sen+"!!"+str(v))

    for i in range(len(dic)):
        dic[i].append(0)
        dic[i].append(0.0)
        if dic[i][4] == -1:
            num = i
            dic[i][5] = 1
            dic[i][6] = 1.0
            if dic[i][1]=="报道" and dic[i][2]=="VV" and v >= 1:
                print("!!+!!!!!")
                sen2 = sen.split("报道")
                print(sen2)
                sen = sen2[len(sen2) - 1]
                pos = 0
                for k in range(len(dic)):
                    if dic[k][1]=="报道" and dic[k][2]=="VV":
                        pos = dic[k][0]
                print("!!+!!!!!" + sen)
                return judgeLocation(sen,pos+1)

    flag = 1
    t = []
    t.append(num)
    while flag:
        temp = []

        for i in range(len(dic)):
            if dic[i][4] in t:
                temp.append(i)

        for i in range(len(temp)):
            if dic[temp[i]][5] == 0:
                dic[temp[i]][5] = 1
                dic[temp[i]][6] = dic[dic[temp[i]][4]][6] / 2
            if dic[temp[i]][2] == "VV" and judge(dic[temp[i]][1], "报道") >= 0.4:
                dic[temp[i]][6] = dic[temp[i]][6] / 32

        flag = 0
        t = temp

        for i in range(len(dic)):
            if (dic[i][3] == "COUNTRY" or dic[i][3] == "CITY" or dic[i][3] == "STATE_OR_PROVINCE" or dic[i][3] == "LOCATION" ):#or dic[i][3] == "GPE"
                if (dic[i][5] == 0):
                    flag = 1
                    break

    for i in range(len(dic)):
        print(dic[i])

    locationValue = []

    for i in range(len(dic)):
        if (dic[i][3] == "COUNTRY" or dic[i][3] == "CITY" or dic[i][3] == "STATE_OR_PROVINCE" or dic[i][3] == "LOCATION" ):#or dic[i][3] == "GPE"
            locationValue.append(dic[i])

    return locationValue , rootPosition

def eliminateDuplicated(locations,rootPosition ,countries):
    countryValue = []
    print(rootPosition)
    for i in range(len(locations)):
        for j in range(len(countries)):
            if locations[i][1] in countries[j]:
                locations[i][1] = countries[j][1]
        print(locations)
        flag = 0

        for j in range(len(countryValue)):
            if locations[i][1] in countryValue[j]:
                countryValue[j][1] = countryValue[j][1] + locations[i][6]
                if locations[i][6]>countryValue[j][3] or \
                        (locations[i][6]==countryValue[j][3] and countryValue[j][2]>abs(locations[i][0]-rootPosition)):
                    countryValue[j][2] = min(countryValue[j][2], abs(locations[i][0]-rootPosition))
                    countryValue[j][3] = locations[i][6]
                    countryValue[j][4] = locations[i][0]
                flag = 1
                break

        if flag == 0:
            countryValue.append([locations[i][1], locations[i][6] , abs(locations[i][0]-rootPosition), locations[i][6], locations[i][0]])

    print(countryValue)
    return countryValue

def main():
    countries = init()
    # with open('outputJudgeLocation2000.csv', 'w') as csvFile:
    #         writer = csv.writer(csvFile)
    #         writer.writerow(["content", "position", "geo_info","value"])
    #         for i in range(339764, 341764):  # 339764 402848      349764
    #             filePlace = "../output/filterfile/" + str(i) + ".txt"
    #             # filePlace = "raw.txt"
    #             try:
    #                 with open(filePlace, mode='r', encoding="utf-8") as f:
    #                     for line in f.readlines():
    #                         try:
    #                             line = line.strip()
    #                             line = line.replace("电", "报道").replace("讯", "报道") \
    #                                 .replace("消息", "报道").replace("快讯", "报道")
    #                             print(line)
    #                             curPlaces, rootPosition = judgeLocation(line, 0)
    #                             places = eliminateDuplicated(curPlaces, rootPosition, countries)
    #                             print(places)
    #                             num = 0.0
    #                             place = ""
    #                             position = 0
    #                             loc = 0
    #                             value = 0.0
    #                             if places != None:
    #                                 for j in range(len(places)):
    #                                     if places[j][1] > num or (places[j][1] == num and places[j][2] < position):
    #                                         num = places[j][1]
    #                                         place = places[j][0]
    #                                         position = places[j][2]
    #                                         loc = places[j][4]
    #                                         value = places[j][3]
    #
    #                             writer.writerow([line, loc, place, value])
    #                         except Exception as e:
    #                             print('except:', e)
    #             except Exception as e:
    #                 print('except:', e)
    #                 # continue

    sen = "中国日报网环球在线报道：据法国媒体8月26日报道，俄罗斯武装部队总参谋长尼古拉·马卡罗夫当天表示，俄罗斯已经在俄罗斯靠近同朝鲜的边境附近部署了S-400“凯旋”防空导弹系统。"
    sen = sen.replace("电", "报道").replace("讯", "报道") \
                                    .replace("消息","报道").replace("快讯","报道")
    print(judgeLocation(sen,0))
    position = 0
    place = ""
    location,rootPosition = judgeLocation(sen,0)

    places = eliminateDuplicated(location,rootPosition,countries)
    num = 0
    if places != None:
        for j in range(len(places)):
            if places[j][1] > num:
                num = places[j][1]
                place = places[j][0]
                position = places[j][2]

            if places[j][1] == num and places[j][2] < position:
                num = places[j][1]
                place = places[j][0]
                position = places[j][2]
    print(place)


if __name__=='__main__':
    main()















# tree=Tree.fromstring(nlp.parse(sen))
#
# tree.draw()

