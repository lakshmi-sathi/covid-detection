# covid-detection

**detection/classify.py**  <- this code loads the COVID-19 dataset for the purpose of creating and training the decision tree. This code saves (pickles) the trained decision tree in 'saved_tree'.

**detection/predict.py** <- this code is used to run the saved tree and take predictions. It basically runs the tree on the whole dataset and gives the accuracy.

**detection/inference_embed.py**  <- this is the portable version that can be embedded into a mobile app. The inference process has minimal processing overhead and hence is suitable for being processed on a mobile phone or similar platform. It can be noted that it only uses the pickle library which means it'll be easy to incorporate into a mobile application

A next stage planned for this project is to embed it into an android app (possibly using the chaquopy python sdk for android). This will enable easy access to this tool and it can help the average person decide whether he must take the risk to go out into the open and get consulted.
