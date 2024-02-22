# LLM - Detect AI Generated Text

This is the an attempt for a Kaggle's contest focused on developing a model capable of differentiating human written text from AI written text. The url of the competition is this one: https://www.kaggle.com/competitions/llm-detect-ai-generated-text

The ideas proposed used the concepts of bag of words and word tagging. There are some protocols in which one tags each word with a label considering the function of that word in the language context. There are a lot of ways of doing this because there can be a lot of different word classifications. In this case we used the built-in `tag.pos_tag` method from the `ntlk` library (Natural language toolkit). This method already knows how to label each word in some classification.

## prueba.py

In order to know how to use the tokenized words, we needed to know all the tags the `tag.pos_tag` used. This script ran through all the tagged words from all the texts from the training set in order to get the full list of tags used by this method.

## wordProportions.py

The central idea of the model is to use the concept of bag of words but instead of words we use types of words. In order to do this, we plot in this script the vectors of proportions of each type of word for each one of the text in the training set. We identify each tag with an index in the vector and we then calculate the proportions for each text and plot all together the AI written texts in red and the human written texts in blue. The resulting plots are `AI normalized.png` and `persons normalized.png`. We made this to see if we can find some patterns in these plots.

We noted in this plots that the fourth and eight tags behaved comparatively different in each plot. In the AI's the forth tag exhibited a lesser proportion than that of the eight tag, and in the humans plot this is reversed.

## averageProportions.py

In this script we took averages from the vectors created in the last script, one for AI and one for humans. We made this to find exact numbers for taking them as reference for creating a model based on the observation we made in the last script's plots. We also printed the averages of the fourth and eight tag proportions.

## model1.py

This is the first model proposal. The path of importation of the test dataset is the one that was necessary for the Kaggle competition, the same is true for the csv exportation format. With the numbers we got in the last script, we created intervals for the difference between the fourth and eight tag proportions in order to predict if the text was written by a human or by an AI. Since the competition asked for the probability of having been written by AI, we used the position of this tag proportions difference in the intervals we defined as a measure of this probability. We used the midpoint between the differences of average tag proportions in human written texts and AI written texts to set the neutral point where the proability is 0.5. We then set the proability to move up or down at linear speed depending on if it is going upwards or downwards. Since this probability variation is linear, it eventually arrives to 0 or 1, depending on the direction, and it stabilizes there.

## neural.ipynb

In this model proposal we created a neural network with `keras` and used the vectors of tag proportions as the training vectors. After using the network to predict the probability of a text input, we cap up or down the number thrown by the network to be included in the interval [0,1]. This approach turned out to be not very helpful. One possible reason for this is that the training set only has 3 AI written texts. 









