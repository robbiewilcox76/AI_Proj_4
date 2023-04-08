from Data import Data
import math

def ValidateFaces(arr1, arr2, limit: int):
    prob1 = 0
    prob1arr = []
    prob2 = 0
    prob2arr = []
    prob3 = arr1[len(arr1)-1]/(arr1[len(arr1)-1] + arr2[len(arr2)-1])
    prob4 = arr2[len(arr2)-1]/(arr1[len(arr1)-1] + arr2[len(arr2)-1])
    v_images = open("data/facedata/facedatavalidation", 'r')
    v_labels = open("data/facedata/facedatavalidationlabels", 'r')
    line = v_images.readline()
    for i in range(limit):
        label = v_labels.readline()
        while line.isspace():
            line = v_images.readline()
            row = 0
        while not line.isspace():
            #print(line, end = "")
            col = 0
            for c in line:
                if c == '\n': continue
                if c == '#' or c == '+':
                    prob1arr.append(math.log(arr1[row][col]/arr1[len(arr1)-1]))
                    prob2arr.append(math.log(arr2[row][col]/arr2[len(arr2)-1]))
                else:
                    prob1arr.append(math.log(1 - (arr1[row][col]/arr1[len(arr1)-1])))
                    prob2arr.append(math.log(1 - (arr2[row][col]/arr2[len(arr2)-1])))
                col+=1
            line = v_images.readline()
            row+=1
        max_p1 = max(prob1arr)
        max_p2 = max(prob2arr)
        for i in prob1arr:
            prob1 += math.exp(i - max_p1)
        ln_prob1 = math.log(prob1) + max_p1
        for i in prob2arr:
            prob2 += math.exp(i - max_p2)
        ln_prob2 = math.log(prob2) + max_p2
        print((ln_prob1 * prob3)/(ln_prob2 * prob4))

def TrainFaces(dig_or_face: str, limit: int):
    arr1 = Data.load_object("SerializedData_NaiveBayes/TrueAndBlackPixel.pickle")
    arr2 = Data.load_object("SerializedData_NaiveBayes/FalseAndBlackPixel.pickle")
    #arr1 = [[1 for i in range(60)] for j in range(68)]
    #arr1.append(0)
    #arr2 = [[1 for i in range(60)] for j in range(68)]
    #arr2.append(0)
    #Data.save_data(arr2,"SerializedData_NaiveBayes/FalseAndBlackPixel.pickle" )
    #Data.save_data(arr1,"SerializedData_NaiveBayes/TrueAndBlackPixel.pickle" )
    if dig_or_face == "faces":
        t_images = open("data/facedata/facedatatrain", 'r')
        t_labels = open("data/facedata/facedatatrainlabels", 'r')
    else:
        if dig_or_face == "digits":
            t_images = open("data/digitdata/trainingimages", 'r')
            t_labels = open("data/digitdata/traininglabels", 'r')
        else:
            return
    line = t_images.readline()
    for i in range(limit):
        label = t_labels.readline()
        if label == "1\n": arr1[len(arr1)-1] += 1 
        else: arr2[len(arr2)-1]+=1 
        while line.isspace():
            line = t_images.readline()
            row = 0
        while not line.isspace():
            col = 0
            for c in line:
                if c == '#' or c == '+':
                    if label == "1\n":
                        arr1[row][col]+=1
                    else:
                        arr2[row][col]+=1
                col+=1
            line = t_images.readline()
            row+=1
    print(arr1)
    ValidateFaces(arr1, arr2, 2)

TrainFaces("faces", 45)