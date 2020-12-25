from stanfordcorenlp import StanfordCoreNLP
import csv

# nlp = StanfordCoreNLP(r'stanford', lang='zh')
# sen = "强台风凤凰可能今晚在福建连江至厦门间登陆"
#
# # print(nlp.ner(sen))
# # print(nlp.parse(sen))
# dic = nlp.ner(sen)
# print(dic)

# #
nlp = StanfordCoreNLP(r'stanford', lang='zh')
def main():

    with open('output2.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(["content", "txt_num", "geo_info"])
        for i in range(339764,402848):  #339764 402848
            filePlace = "../output/filterfile/" + str(i) + ".txt"
            try:
                with open(filePlace, mode='r', encoding="utf-8") as f:
                    for line in f.readlines():
                        places = []
                        place = ""
                        try:
                            line = line.strip()
                            print(line)
                            dic = nlp.ner(line)
                            for j in range(len(dic)):
                                # if (dic[j][1] == "COUNTRY" or dic[j][1] == "CITY" or dic[j][1] == "STATE_OR_PROVINCE"
                                #       or dic[j][1]=="GPE" or dic[j][1]=="LOCATION"):
                                if (dic[j][1] == "COUNTRY" or dic[j][1] == "CITY" or dic[j][1] == "STATE_OR_PROVINCE"
                                     or dic[j][1] == "LOCATION"):
                                    if (dic[j][0] not in places):
                                        place = place + " "+"("+str(j)+","+str(dic[j][0])+")"
                                        places.append(dic[j][0])

                            writer.writerow([line, i , place])
                        except Exception as e:
                            print('except:', e)

            except Exception as e:
                # print('except:', e)
                continue


if __name__ == '__main__':
    main()

