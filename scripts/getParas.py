import sys
import json
import os


def main(args):
    # cwd = os.getcwd()
    # f = open(cwd + "/../data/wikiContent/animals/" + args[0] + ".txt")
    for filename in os.listdir('plants'):
        print(filename)
        f = open('plants/' + filename)
        data = f.readlines()
        tags = {}
        currContainer = ""
        currTag = ""
        for line in data:
            words = line.split()
            if len(words) >= 1:
                if(words[0] == '===' or words[0] == '==' or words[0] == '='):
                    if currTag != "":
                        tags[currTag] = currContainer
                    currContainer = ""
                    if words[0] == '===':
                        currTag = line[4:-5]
                    elif words[0] == '==':
                        currTag = line[3:-4]
                    else:
                        currTag = line[2:-3]
                else:
                    currContainer = currContainer + line

        with open('plantsJson/' + filename.split('.', 1)[0] + '.json', 'w') as jsonfile:
            json.dump(tags, jsonfile, indent=4, sort_keys=True,
                      ensure_ascii=False)

if __name__ == '__main__':
    main(sys.argv[1:])
