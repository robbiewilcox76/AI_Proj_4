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
        # print(weights)
        # for i in range(0,9):
        # while(predictrate<.7):
        import copy
        while(predictrate<.72):
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
                if(iteration%50!=0):
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
                else:
                    for k in range(0,len(mostsuccess[0][0][0])):
                        sum=0

                        for j in range(0,10):
                            weights[j][k]=0
                            for i in range(0,len(mostsuccess)):
                                weights[j][k]+=mostsuccess[i][0][j][k]*mostsuccess[i][1]
                            sum=weights[j][k]
                        for j in range(0,10):
                            if sum!=0:
                                weights[j][k]=weights[j][k]/sum
            testfile=open("classification/data/digitdata/testimages", "r")
            labelfile=open("classification/data/digitdata/testlabels", "r")
            k=""
            imageno=0
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
            print("this predictrate is: ",predictrate)
            print("best predictrate is: ", predictrate1)
            iteration+=1
            if predictrate1>=predictrate:
                weights=weights1
                predictrate=predictrate1
                mostsuccess.append([weights,predictrate])

        iteration+=1
        return weights
def verify(weights):
    testfile=open("classification/data/digitdata/validationimages", "r")
    labelfile=open("classification/data/digitdata/validationlabels", "r")
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
    print(predictrate)
    predictrate=predictrate/imageno
    print("new predictrate is: ",predictrate)
weights=ml.train(1)
verify(weights)