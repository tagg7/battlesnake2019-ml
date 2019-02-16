import requests
import json
import sys
from time import sleep

def createGame():	
	url = "http://localhost:3005/games"
	headers = {'Content-type': 'text/plain', 'Accept': 'text/plain'}
	payload = {
		"width":15,
		"height":15,
		"food":1,
		"MaxTurnsToNextFoodSpawn":0,
		"snakes":[{"name":"Test","url":"http://localhost:8080"}]
	}
	payload_txt = json.dumps(payload)

	response = requests.post(url, data=payload_txt, headers=headers)
	response.raise_for_status()

	response_json = json.loads(response.text)
	return response_json["ID"]

def startGame(game_id):
	url = "http://localhost:3005/games/" + game_id + "/start"
	headers = {'Content-type': 'text/plain', 'Accept': 'text/plain'}
	
	response = requests.post(url, headers=headers)
	response.raise_for_status()

def waitForGameEnd(game_id):
	is_done = False

	while not is_done:
		url = "http://localhost:3005/games/" + game_id
		headers = {'Content-type': 'text/plain', 'Accept': 'text/plain'}
		
		response = requests.get(url, headers=headers)
		response.raise_for_status()

		response_json = json.loads(response.text)
		if response_json["Game"]["Status"] == "complete":
			is_done = True
		else:
			sleep(0.1)

if __name__ == '__main__':
	iterations = 50

	if len(sys.argv) > 1:
		iterations = int(sys.argv[1])
	
	for x in xrange(iterations):
		game_id = createGame()
		startGame(game_id)
		waitForGameEnd(game_id)
		print("Game Ended: %d - %s" % (x + 1, game_id))