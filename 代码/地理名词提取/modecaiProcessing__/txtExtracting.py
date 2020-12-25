
def main():
    for i in range(339764, 402849):
        filePlace = "rawdata/" + str(i) + ".txt"
        outputfilePlace = "output/rawoutput/" + str(i) + ".txt"
        print(i)
        with open(filePlace, mode='r', encoding="utf-8") as f:
            fo = open(outputfilePlace, "w")
            count = 0
            for line in f.readlines():
                count = count + 1
                fo.write(line.strip())
                if count == 2:
                    break
                fo.write("\n")


if __name__ == '__main__':
    main()


