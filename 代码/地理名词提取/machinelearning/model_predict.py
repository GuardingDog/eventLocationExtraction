# Load saved model
import kashgari

loaded_model = kashgari.utils.load_model('REVISED_location_WordEmbedding.h5')

while True:
    text = input('sentence: ')
    t = loaded_model.predict([[char for char in text]])
    target = ""
    place = ""
    verb = ""
    for i in range(len(t[0])):
        if t[0][i] == "B-place":
            place +=" "+text[i]
        if t[0][i] == "I-place":
            place += text[i]
        if t[0][i] == "B-targetplace":
            target +=" "+text[i]
        if t[0][i] == "I-targetplace":
            target += text[i]
        if t[0][i] == "B-verb":
            verb +=" "+text[i]
        if t[0][i] == "I-verb":
            verb += text[i]

    print("targetPlace:"+target)
    print("place:"+place)
    print("verb:"+verb)
