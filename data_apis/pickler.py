import re
import os
import json
import pickle

_DIR = "/home/nevronas/Projects/Personal-Projects/Dhruv/NeuralDialog-CVAE/"

file = open(_DIR + "data/commonsense/json_version/annotations.json", "r")
data = json.load(file)
to_write = {"train" : list(), "valid" : list(), "test" : list()}
count = 0
classes = ["joy", "trust", "fear", "surprise", "sadness", "disgust", "anger", "anticipation"]

def get_labels(charay):
    ann = []
    try :
        ann = [charay["emotion"]["ann0"]["plutchik"]]
    except:
        print("ann0 ignored")
    try :
        ann.append(charay["emotion"]["ann1"]["plutchik"])
    except:
        print("ann1 ignored")
    try :
        ann.append(charay["emotion"]["ann2"]["plutchik"])
    except:
        print("ann2 ignored")
    if(len(ann) == 0):
        return None

    final_dict = dict()
    for classi in classes:
        final_dict[classi] = [1, 1, 1]

    for idx in range(len(ann)):
        for i in ann[idx]:
            if(i[:-2] in final_dict.keys()):
                final_dict[i[:-2]][idx] = int(i[-1])
    majority = []
    for key in final_dict.keys():
        if(int(sum(final_dict[key])/3) >= 2):
            majority.append(key) #[key if(floor(sum(final_dict[key]) / 3) >= 2) for key in final_dict.keys()]
    onehot = [1 if i in majority else 0 for i in classes]
    return onehot

with open(_DIR + "data/commonsense/storyid_partition.txt", "r") as f:
    for line in f:
        idkey =  line.split("\t")[0]
        story = data[idkey]
        tdt = story["partition"].replace("dev", "valid")
        dialog = dict()
        chars = list(story["lines"]["1"]["characters"].keys())
        if(len(chars) < 2):
            continue
        dialog["A"] = chars[0]
        dialog["B"] = chars[1] # TODO : Change
        #dialog["topic"] = story["title"].lower() # NOTE : Removed this
        utterances = list()
        for stline in range(5):
            linei = story["lines"]["{}".format(stline + 1)]
            characters = linei["characters"]

            charA, charB = characters[dialog["A"]], characters[dialog["B"]]
            tr = False
            if(charA["app"] == True):
                onehotm = get_labels(charA)
                if(onehotm != None):
                    uttr = ("A", linei["text"], [onehotm])
                    utterances.append(uttr)
                    count += 1
                    tr = True
            if(charB["app"] == True):
                onehotm = get_labels(charB)
                if(onehotm != None):
                    uttr = ("B", linei["text"], [onehotm])
                    utterances.append(uttr)
                    if(!tr):
                        coutn += 1


        print(utterances)
        dialog["utts"] = utterances
        to_write[tdt].append(dialog)
    dev_len = len(to_write["valid"])
    to_write["train"], to_write["valid"] = to_write["valid"][:int(0.8 * dev_len)], to_write["valid"][int(0.8 * dev_len) + 1:]
    print(count)

with open(_DIR + "data/commonsense/data.pkl", "wb+") as handle:
    pickle.dump(to_write, handle)
