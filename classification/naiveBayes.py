# naiveBayes.py
# -------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import util
import classificationMethod
import math
import collections

class NaiveBayesClassifier(classificationMethod.ClassificationMethod):
  """
  See the project description for the specifications of the Naive Bayes classifier.
  
  Note that the variable 'datum' in this code refers to a counter of features
  (not to a raw samples.Datum).
  """
  def __init__(self, legalLabels):
    self.legalLabels = legalLabels
    self.type = "naivebayes"
    self.k = 1 # this is the smoothing parameter, ** use it in your train method **
    self.automaticTuning = False # Look at this flag to decide whether to choose k automatically ** use this in your train method **
    self.probs = None # Stores conditional probabilities, constructed in TrainAndTune
    self.trainingLabelCounter = None # Stores P(Y = y) for each label
    
  def setSmoothing(self, k):
    """
    This is used by the main method to change the smoothing parameter before training.
    Do not modify this method.
    """
    self.k = k

  def train(self, trainingData, trainingLabels, validationData, validationLabels):
    """
    Outside shell to call your method. Do not modify this method.
    """  
      
    # might be useful in your code later...
    # this is a list of all features in the training set.
    self.features = list(set([ f for datum in trainingData for f in datum.keys() ]));
    
    if (self.automaticTuning):
        kgrid = [0.001, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 20, 50]
    else:
        kgrid = [self.k]
        
    self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, kgrid)
      
  def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, kgrid):
    """
    Trains the classifier by collecting counts over the training data, and
    stores the Laplace smoothed estimates so that they can be used to classify.
    Evaluate each value of k in kgrid to choose the smoothing parameter 
    that gives the best accuracy on the held-out validationData.
    
    trainingData and validationData are lists of feature Counters.  The corresponding
    label lists contain the correct label for each datum.
    
    To get the list of all possible features or labels, use self.features and 
    self.legalLabels.
    """

    "*** YOUR CODE HERE ***"

    self.trainingLabelCounter = util.Counter()
    for i in trainingLabels:
      self.trainingLabelCounter[i] += 1
    self.trainingLabelCounter.normalize()

    self.probs = {}
    for lbl in self.legalLabels:
      self.probs[lbl] = {}
      for i in trainingData[0]:
        self.probs[lbl][i] = util.Counter()
        self.probs[lbl][i][0] += self.k
        self.probs[lbl][i][1] += self.k
    for i, data in enumerate(trainingData):
      #print("{} {}".format(i, data))
      curLabel = trainingLabels[i]
      for tuple in data:
        #print("{} {}".format(tuple, data[tuple]))
        if data[tuple] == 1:
         self.probs[curLabel][tuple][1] += 1
        else:
          self.probs[curLabel][tuple][0] += 1
      #print(probs)
    for i in self.probs:
      for j in self.probs[0]:
        self.probs[i][j].normalize()
    #print(probs)

    #util.raiseNotDefined()
        
  def classify(self, testData):
    """
    Classify the data based on the posterior distribution over labels.
    
    You shouldn't modify this method.
    """
    guesses = []
    self.posteriors = [] # Log posteriors are stored for later data analysis (autograder).
    for datum in testData:
      posterior = self.calculateLogJointProbabilities(datum)
      guesses.append(posterior.argMax())
      self.posteriors.append(posterior)
    return guesses
      
  def calculateLogJointProbabilities(self, datum):
    """
    Returns the log-joint distribution over legal labels and the datum.
    Each log-probability should be stored in the log-joint counter, e.g.    
    logJoint[3] = <Estimate of log( P(Label = 3, datum) )>
    
    To get the list of all possible features or labels, use self.features and 
    self.legalLabels.
    """

    # print(self.trainingLabelCounter)
    logJoint = util.Counter()
    for lbl in self.legalLabels:
      sum = 0
      for tuple in datum:
        sum += math.log(self.probs[lbl][tuple][datum[tuple]])
      # print("label is: ", lbl, self.trainingLabelCounter[lbl])
      if (self.trainingLabelCounter[lbl] == 0):
        sum += math.log(0.001)
      else:
        sum += math.log(self.trainingLabelCounter[lbl])
      logJoint[lbl] = sum
    
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    
    return logJoint
  
  def findHighOddsFeatures(self, label1, label2):
    """
    Returns the 100 best features for the odds ratio:
            P(feature=1 | label1)/P(feature=1 | label2) 
    
    Note: you may find 'self.features' a useful way to loop through all possible features
    """
    featuresOdds = []
       
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

    return featuresOdds
    

    
      
