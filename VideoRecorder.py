from moviepy import *
import random
import webbrowser
import pandas
import numpy as np
import os
import cv2
import matplotlib.pyplot as plt
from upload_manager import *

random = random.randint(1,4)
path = os.getcwd() + "/videos/{}.mp4".format(random)

clip = VideoFileClip(path)
duration = clip.duration

timeElapsed = 0.0
images = dict()

cam = cv2.VideoCapture(0)
cam.set(3,640)
cam.set(4,480)

start = time.time()
for i in range(0,30):
	_, __ = cam.read()

fps = int(30/(time.time() - start))

_, test = cam.read()
size = test.shape[0:2]

html_str = """

<html>
<body>
<video id ='video' autoplay=true width="1400" height="600" controls>
  <source src="{}" type="video/mp4">
</body>
</html>
""".format(path)

Html_file= open("index.html","w")
Html_file.write(html_str)
Html_file.close()

webbrowser.open("file://"+os.getcwd()+"/index.html")

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4',fourcc, fps, size)

while timeElapsed < duration:

	delta = 1.0/fps

	ret, frame = cam.read()

	if ret:
		frame = cv2.resize(frame, size)
		out.write(frame)

	timeElapsed += delta

out.release()
cam.release()

vm = UploadManager()

vm.send_video(os.getcwd()+"/output.mp4")
data = vm.get_data()

while data is None:
	 time.sleep(5)
	 data = vm.get_data()

os.remove(os.getcwd()+"/output.mp4")

array = np.empty((len(data), 9))

row = 0
for k in data.keys():
	array[row][0] = k
	array[row][1] = data[k]["happiness"]
	array[row][2] = data[k]["contempt"]
	array[row][3] = data[k]["anger"]
	array[row][4] = data[k]["disgust"]
	array[row][5] = data[k]["fear"]
	array[row][6] = data[k]["neutral"]
	array[row][7] = data[k]["sadness"]
	array[row][8] = data[k]["surprise"]

	row += 1

df = pandas.DataFrame(array, columns=["Time", "Happiness", "Contempt", "Anger", "Disgust", "Fear", "Neutral", "Sadness", "Surprise"])

plt.plot(df["Time"], df["Happiness"])
plt.plot(df["Time"], df["Contempt"])
plt.plot(df["Time"], df["Anger"])
plt.plot(df["Time"], df["Disgust"])
plt.plot(df["Time"], df["Fear"])
plt.plot(df["Time"], df["Neutral"])
plt.plot(df["Time"], df["Sadness"])
plt.plot(df["Time"], df["Surprise"])

plt.legend(["Happiness", "Contempt", "Anger", "Disgust", "Fear", "Neutral", "Sadness", "Surprise"], loc="upper left")
plt.ylabel("Percent")
plt.xlabel("Time")

plt.show()