#how this works:
#1. reads the training data, calculates the probability of a pixel being present for each type of image, and stores this probability in a nxm array where n is the number of different types of images(10 digits, face or no face, etc.) and m is the number of pixels in the picture.
#2. tests the data against the test set
#3. if the program is less than 72% accurate, the array randomly multiplies values in the array by .92 with smaller entries in the arrays being more likely to be multiplied. 
#4. the new array is then tested against the testing data, and step 3 is repeated while keeping the array with the largest accuracy.
#5. once the array has an accuracy above 72%, the validation data is used to test the training data. 
class ml:
    def readnextimage(file):
        n=file.readline()
        len=0
        while(n.startswith("                            \n")):
            n=file.readline()
            len+=1
        # print(len)

        k=""
        l=0
        while(not n.startswith("                            \n") or l<20):
            if n=="":
                return k
            k+=n
            n=file.readline()
            # if(n.startswith("                            ")):
            #     m=file.readline()
            #     if(not n.startswith("                            ")):
                    # k+=n
                    # n=m
            l+=1
        return k
    def readnexttag(file):
        k=file.readline()
        return k
    def train(seed):
        import random
        random.seed(seed)
        predictrate=0
        iteration=0
        testfile=open("classification/data/digitdata/trainingimages", "r")
        k=""
        labelfile=open("classification/data/digitdata/traininglabels", "r")
        imageno=1
        k=ml.readnextimage(testfile)
        tag=int(ml.readnexttag(labelfile))
        # print(len(k))
        weights=[[0]*(len(k)+1) for i in range(10)]
        mostsuccess=[]
        storeval=[]
        # print(weights)
        # for i in range(0,9):
        # while(predictrate<.7):
        import copy
        while(predictrate<.72 and iteration<=2000):
            predictrate1=predictrate
            predictrate=0
            
            weights1=copy.deepcopy(weights)
            print ("starting iteration:", iteration)

            if(iteration==0):

                while k!="": 
                    if imageno!=0:
                        k=ml.readnextimage(testfile)
                        if k!="":
                            tag=int(ml.readnexttag(labelfile))
                    if(k==""):
                        break
                    # print(k)
                    # print (tag)
                    # for j in range(0,9):
                    #     for i in range(0,len(k)):
                            # weights[j][i]+=random.uniform(0.0,1.0)
                            # while weights[j][i]==0:
                            #     weights[j][i]+=random.uniform(0.0,1.0)
                    for i in range(0,10):
                        for j in range(0,len(k)):
                            if i==tag:
                                if k[j]== " ":
                                    weights[i][j]=weights[i][j]
                                else:
                                    weights[i][j]=(weights[i][j]+1)
                            if i!=tag:
                                if k[j]== " ":
                                    weights[i][j]=(weights[i][j]+1)
                                else:
                                    weights[i][j]=weights[i][j]
                    imageno=imageno+1
                    # print("trained image:", imageno)
                for j in range(0,len(k)):
                    sum=0
                    for i in range(0,10):
                        weights[i][j]=weights[i][j]/imageno
                        sum+=weights[i][j]
                    for i in range(0,10):
                        weights[i][j]=weights[i][j]/sum
            else:
                for i in range(0,len(weights[0])):
                    sum=0
                    for j in range(0,10):
                        # print(weights[j][i])
                        if(random.uniform(0.0,1.0)>weights[j][i]):
                            weights[j][i]=weights[j][i]*(.92)
                        sum+=weights[j][i]
                        # print(weights[j][i])
                    for j in range(0,10):
                        if sum!=0:
                            weights[j][i]=weights[j][i]/sum
                        #    print(weights[j][i])
            testfile=open("classification/data/digitdata/validationimages", "r")
            labelfile=open("classification/data/digitdata/validationlabels", "r")
            k=""
            imageno=0
            if(iteration==0):
                while(k!="" or imageno==0 or imageno):
                    k=ml.readnextimage(testfile)
                    imageno+=1
                    if(k==""):
                        break
                    # print(k)
                    tag=int(ml.readnexttag(labelfile))
                    # print(tag)
                    storeimage=[]
                    storeimage.append(k)
                    storeimage.append(tag)
                    storeval.append(storeimage)
                    biggestsum=(0,0)
                    for i in range(0,10):
                        cursum=0
                        for j in range(0,len(k)):
                            if k[j]!=" ":
                                cursum+=(weights[i][j])
                        if(cursum>biggestsum[0]):
                            biggestsum=(cursum,i)
                    if(biggestsum[1]==tag):
                        predictrate+=1
                # print(predictrate)
                predictrate=predictrate/imageno
                # print("this predictrate is: ",predictrate)
                # print("best predictrate is: ", predictrate1)
                iteration+=1
                if predictrate1>=predictrate:
                    weights=weights1
                    predictrate=predictrate1
                    mostsuccess.append([weights,predictrate])
            else:
                while(imageno<len(storeval) or imageno==0):
                    k=storeval[imageno][0]
                    if(k==""):
                        break
                    # print(k)
                    tag=storeval[imageno][1]
                    # print(tag)
                    imageno+=1

                    biggestsum=(0,0)
                    for i in range(0,10):
                        cursum=0
                        for j in range(0,len(k)):
                            if k[j]!=" ":
                                cursum+=(weights[i][j])
                        if(cursum>biggestsum[0]):
                            biggestsum=(cursum,i)
                    if(biggestsum[1]==tag):
                        predictrate+=1
                # print(predictrate)
                predictrate=predictrate/imageno
                # print("this predictrate is: ",predictrate)
                # print("best predictrate is: ", predictrate1)
                iteration+=1
                if predictrate1>=predictrate:
                    weights=weights1
                    predictrate=predictrate1
                    mostsuccess.append([weights,predictrate])
        iteration+=1
        return weights
def test(weights):
    testfile=open("classification/data/digitdata/testimages", "r")
    labelfile=open("classification/data/digitdata/testlabels", "r")
    k=""
    imageno=0
    predictrate=0
    while(k!="" or imageno==0):
        k=ml.readnextimage(testfile)
        imageno+=1
        if(k==""):
            break
        tag=int(ml.readnexttag(labelfile))
        
        biggestsum=(0,0)
        for i in range(0,10):
            cursum=0
            for j in range(0,len(k)):
                if k[j]!=" ":
                    cursum+=(weights[i][j])
            if(cursum>biggestsum[0]):
                biggestsum=(cursum,i)
        if(biggestsum[1]==tag):
            predictrate+=1
    # print(predictrate)
    predictrate=predictrate/imageno
    print("new predictrate for identifying digits is: ",predictrate)
class mlface:
    def readnextimage(file):
        n=file.readline()
        len=0
        # while(n.startswith("                                                            \n")):
        #     n=file.readline()
        #     len+=1
        k=""
        l=0
        while(l<=70):#not n.startswith("                                                            \n")):# or l<68):
            if n=="":
                return k
            k+=n
            n=file.readline()
            # if(n.startswith("                            ")):
            #     m=file.readline()
            #     if(not n.startswith("                            ")):
                    # k+=n
                    # n=m
            l+=1
            # print(l)
        return k
    def readnexttag(file):
        k=file.readline()
        return k
    def trainface(seed):
        import random
        random.seed(seed)
        predictrate=0
        iteration=0
        testfile=open("classification/data/facedata/facedatatrain", "r")
        k=""
        labelfile=open("classification/data/facedata/facedatatrainlabels", "r")
        imageno=1
        # verifile=
        k=mlface.readnextimage(testfile)
        tag=int(mlface.readnexttag(labelfile))
        # print(len(k))
        weights=[[0]*(len(k)+1000) for i in range(2)]
        mostsuccess=[]
        storeval=[]
        # print(weights)
        # for i in range(0,9):
        # while(predictrate<.7):
        import copy
        while(predictrate<.72 and iteration<=2000):
            predictrate1=predictrate
            predictrate=0
            
            weights1=copy.deepcopy(weights)
            print ("starting iteration:", iteration)

            if(iteration==0):

                while k!="": 
                    if imageno!=0:
                        k=mlface.readnextimage(testfile)
                        if k!="":
                            # print(imageno)
                            # print(k)
                            tag=int(mlface.readnexttag(labelfile))
                            # print(tag)
                    if(k==""):
                        break
                    # print(k)
                    # print (tag)
                    # for j in range(0,9):
                    #     for i in range(0,len(k)):
                            # weights[j][i]+=random.uniform(0.0,1.0)
                            # while weights[j][i]==0:
                            #     weights[j][i]+=random.uniform(0.0,1.0)
                    for i in range(0,2):
                        for j in range(0,len(k)):
                            # print(i)
                            # print(j)
                            # print(">"+k+"<")
                            if i==tag:
                                if k[j]== " ":
                                    weights[i][j]=weights[i][j]
                                else:
                                    weights[i][j]=(weights[i][j]+1)
                            if i!=tag:
                                if k[j]== " ":
                                    weights[i][j]=(weights[i][j]+1)
                                else:
                                    weights[i][j]=weights[i][j]
                    imageno=imageno+1
                    # print("trained image:", imageno)
                for j in range(0,len(k)):
                    sum=0
                    for i in range(0,2):
                        weights[i][j]=weights[i][j]/imageno
                        sum+=weights[i][j]
                    for i in range(0,2):
                        weights[i][j]=weights[i][j]/sum
            else:
                for i in range(0,len(weights[0])):
                    sum=0
                    for j in range(0,2):
                        # print(weights[j][i])
                        if(random.uniform(0.0,1.0)>weights[j][i]):
                            weights[j][i]=weights[j][i]*(.92)
                        sum+=weights[j][i]
                        # print(weights[j][i])
                    for j in range(0,2):
                        if sum!=0:
                            weights[j][i]=weights[j][i]/sum
                        #    print(weights[j][i])
        
            testfile=open("classification/data/facedata/facedatavalidation", "r")
            labelfile=open("classification/data/facedata/facedatavalidationlabels", "r")
            k=""
            imageno=0
            if(iteration==0):
                while(k!="" or imageno==0):
                    k=mlface.readnextimage(testfile)
                    imageno+=1
                    if(k==""):
                        break
                    tag=int(mlface.readnexttag(labelfile))
                    storeimage=[]
                    storeimage.append(k)
                    storeimage.append(tag)
                    storeval.append(storeimage)
                    biggestsum=(0,0)
                    for i in range(0,2):
                        cursum=0
                        for j in range(0,len(k)):
                            if k[j]!=" ":
                                cursum+=(weights[i][j])
                        if(cursum>biggestsum[0]):
                            biggestsum=(cursum,i)
                    if(biggestsum[1]==tag):
                        predictrate+=1
                # print(predictrate)
                predictrate=predictrate/imageno
                # print("this predictrate is: ",predictrate)
                # print("best predictrate is: ", predictrate1)
                iteration+=1
                if predictrate1>=predictrate:
                    weights=weights1
                    predictrate=predictrate1
                    mostsuccess.append([weights,predictrate])
            else:
                while(imageno<len(storeval) or imageno==0):
                    k=storeval[imageno][0]
                    if(k==""):
                        break
                    tag=storeval[imageno][1]
                    imageno+=1
                    biggestsum=(0,0)
                    for i in range(0,2):
                        cursum=0
                        for j in range(0,len(k)):
                            if k[j]!=" ":
                                cursum+=(weights[i][j])
                        if(cursum>biggestsum[0]):
                            biggestsum=(cursum,i)
                    if(biggestsum[1]==tag):
                        predictrate+=1
                # print(predictrate)
                predictrate=predictrate/imageno
                # print("this predictrate is: ",predictrate)
                # print("best predictrate is: ", predictrate1)
                iteration+=1
                if predictrate1>=predictrate:
                    weights=weights1
                    predictrate=predictrate1
                    mostsuccess.append([weights,predictrate])
        iteration+=1
        return weights
def testface(weights):
    testfile=open("classification/data/facedata/facedatatest", "r")
    labelfile=open("classification/data/facedata/facedatatestlabels", "r")
    k=""
    imageno=0
    predictrate=0
    while(k!="" or imageno==0):
        k=mlface.readnextimage(testfile)
        imageno+=1
        if(k==""):
            break
        tag=int(mlface.readnexttag(labelfile))
        
        biggestsum=(0,0)
        for i in range(0,2):
            cursum=0
            for j in range(0,len(k)-1):
                # print(i)
                # print(j)
                # print(len(k))
                if k[j]!=" ":
                    cursum+=(weights[i][j])
            if(cursum>biggestsum[0]):
                biggestsum=(cursum,i)
        if(biggestsum[1]==tag):
            predictrate+=1
    # print(predictrate)
    predictrate=predictrate/imageno
    print("new predictrate for identifying faces is: ",predictrate)

weights=mlface.trainface(1)
testface(weights)
weights=ml.train(1)
test(weights)

