import requests, time, json


class UploadManager:
	key = "e5409d248f2d474a81fb1e68dba318a9"

	def __init__(self):
		self.status_url = ""

	def send_video(self, file_path):
		url = "https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognizeInVideo/"

		headers = {
			'content-type': "application/octet-stream",
			'ocp-apim-subscription-key': self.key,
		}
		with open(file_path, "rb") as file:
			response = requests.post(url, data = file, headers = headers)

			if response.status_code == 202:
				self.status_url = response.headers["Operation-Location"]
			else:
				print("Unable to upload; {}".format(response.status_code))

	def __get_response(self):
		if self.status_url != "":
				headers = {
					'ocp-apim-subscription-key': self.key,
				}
				response = requests.get(self.status_url, headers=headers)

				if response.status_code == 200:
					dict = json.loads(response.text)

					if dict["status"] == "Succeeded":
						return json.loads(dict["processingResult"])
					else:
						return None

				else:
					return None


	def get_data(self):
		response = self.__get_response()

		if response is not None:

			data = {}
			ts = 0
			tps = response["timescale"]

			for fragment in response["fragments"]:

				if "interval" not in fragment:
					continue

				delta = fragment["interval"]

				for event in fragment["events"]:
					ev = event[0]
					data[ts/tps] = ev["windowMeanScores"]
					ts += delta

			return data

		else:
			return None

# vm = VideoManager()
#
# vm.send_video("/Users/gabrielramirez/Downloads/IMG_1122.MOV")
#
# data = vm.get_data()
#
# while data is None:
#     time.sleep(5)
#     data = vm.get_data()