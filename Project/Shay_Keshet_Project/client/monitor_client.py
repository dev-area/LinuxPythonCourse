import urllib.request
import time

while True:
    response = urllib.request.urlopen(
        "http://192.168.0.2:5001/monitor/alive"
    )

    print(response.read().decode())

    time.sleep(5)