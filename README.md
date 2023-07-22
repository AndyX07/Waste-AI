# Waste-AI

## Inspiration
Each year, over **2.1 billion tons** of waste are generated worldwide with a significant portion of which ending up in landfills, causing devastating environmental impacts.

One key challenge in addressing this problem is the ineffective sorting and classification of waste, which often results in missed recycling opportunities, improper disposal of waste, and increased pollution

According to a survey commissioned by Covanta, **62%** of Americans worry that lack of knowledge causes them to recycle incorrectly. I aim to solve this with Waste AI.

## What it does
Waste AI is a system that utilizes machine learning and computer vision algorithms to classify and sort waste items into appropriate categories of electronic, glass, metal, paper, plastic, organic, and textile waste. Its core functionalities are:
- Classify waste
- Provides user with the proper steps to recycle the waste.

## How we built it
The dataset of 7400 images was collected by me using google images and the Download All Images chrome extension.

The machine learning model was built using Python and including Tensorflow, OpenCV, Numpy and Pandas. The model is a Convolutional Neural Network and is built on top of MobileNetV2 using transfer learning.

The web app was built using Flask as the backend with HTML and CSS on the front end
## Challenges we ran into
When training the model, some of the images from chrome was not a very good training images. So, I tried removing all the images that I thought were bad training images.

## Accomplishments that we're proud of
The accomplishment that I am most proud of was training the model to have an accuracy of over 80%. I expected the accuracy to be much lower and I am proud that the model's accuracy was good. 

## What we learned
I learned how to use Flask as a backend. Prior to this, I had not used Flask before so this was my first time using Flask in an application. I also learned how to better plan projects to make execution easier.

## What's next for Waste AI
I hope to expand the capabilities of the AI to detect more types of waste. I also hope to improve the accuracy of the machine learning model to make classification even more accurate.
