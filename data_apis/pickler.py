import re
import os
import json
import pickle

_DIR = "/home/nevronas/Projects/Personal-Projects/Dhruv/NeuralDialog-CVAE/"

file = open(_DIR + "data/commonsense/json_version/annotations.json", "r")
data = json.load(file)
to_write = {"train" : list(), "valid" : list(), "test" : list()}

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
        dialog["topic"] = story["title"]
        utterances = list()
        for stline in range(5):
            linei = story["lines"]["{}".format(stline + 1)]
            characters = linei["characters"]

            charA, charB = characters[dialog["A"]], characters[dialog["B"]]
            print(charA, charB)
            _ = input()
            if(charA["app"] == True):
                try :
                    mystring = str(charA["emotion"]["ann0"]["text"])
                    re.sub('[^A-Za-z]+', '', mystring)
                    uttr = ("A", linei["text"], [mystring])
                    utterances.append(uttr)
                except KeyError:
                    pass
            if(charB["app"] == True):
                try :
                    mystring = str(charB["emotion"]["ann0"]["text"])
                    re.sub('[^A-Za-z]+', '', mystring)
                    uttr = ("B", linei["text"], [mystring])
                    utterances.append(uttr)
                except KeyError:
                    pass
        print(utterances)
        dialog["utts"] = utterances
        to_write[tdt].append(dialog)

with open(_DIR + "data/commonsense/data.pkl", "wb+") as handle:
    pickle.dump(to_write, handle)
