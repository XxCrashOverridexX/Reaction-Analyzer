# Reaction Analyzer is a program that gives feedback to companies about the effectiveness of their advertisements. 

# The first feature - Video Recorder - is a facial expression analyzer which tracks the user's facial expressions throughout the video via the camera on their computer. After capturing the data from the user's facial expressions, it produces a graph of different emotions the user went through over time, by using Microsoft Azure's emotion tracker API. 

# The second feature - Text Analysis - is a verbal feedback analyzer, which asks the user to type in a 1 sentence comment describing their thoughts throughout the video. Via the use of Microsoft Azure's Text Analysis API, the program analyzes their grammar usage, vocabulary and overall tone of voice in the comment, and returns a number between 0 and 1 to describe their overall emotion (1 being positive and 0 being negative).
