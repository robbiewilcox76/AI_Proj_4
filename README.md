Machine Learning Project

Helpful data:
    Picture dimensions:
        Face:
            height: 68
            width: 60 (excluding newline character)
        Digit:
            height: 20
            width: 28 (excluding newline character)

    This + 1 should be the dimnsions of the feature arrays 
        The last entry of each array will be the number of true or false images seen, respectively.  This is so that everything that
        is needed for calculations is in that array.  This element should never be changed with dealing with features, only when updating
        this number itself.

    Plan for naive bayes:
        Arrays can be serialized using Data class into the specified file path that is already set up, don't mess with the filepaths 
        or the pickle files, this will mess everything up.  Naive Bayes is as follows (for binary data, idk how to do it for digits):
            L(x) = ( P(x | y = true) * P(y = true) )/ ( P(x | y = false) * P(y = false) )

        to calculate p(y = true) and p(y = false) you can simply calculate it as:
            p(y = true) = # of faces that have show up so far / # of images that have shown up so far

        to calculate conditional probabilities you must calculate it using features for each pixel.  The features array will represent occurences, not probabilities, which can just be divided by the number of images so that it's easier to recalculate them when you need to add 1.

Naive Bayes Serialized data (faces):
    Table storing occurrences of black pixel and the image being a face -> TrueAndBlackPixel.pickle
    Table storing occurrences of black pixel and the image not being a face -> FalseAndBlackPixel.pickle
