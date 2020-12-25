str = ""
with open("data/location.train", "r") as f:  # 打开文件
    data = f.read()  #读取文件
    cop = data.split("\n")
    pre = ""
    for data in cop:
        if data=="":
            str = str+"\n"
            pre = ""
            continue
        cur = data.split(" ")
        if cur[1]=="P" or cur[1] == "T" or cur[1] == "V":
            if cur[1] == "P":
                cur[1] = "place"
            if cur[1] == "T":
                cur[1] = "targetplace"
            if cur[1] == "V":
                cur[1] = "verb"
            if pre == cur[1]:
                tag = "I-"+cur[1]
                str += cur[0]+" "+tag
            if pre != cur[1]:
                pre = cur[1]
                tag = "B-"+cur[1]
                str += cur[0] + " " + tag
            str += "\n"
        else:
            pre = cur[1]
            str += data+"\n"

with open("data/Revisedlocation.train","w") as f:
    f.write(str)