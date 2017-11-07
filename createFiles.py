#!/usr/bin/python
# coding=utf-8
import os

class Player:
	name = ""
	playerId = ""

	def __init__(self, name, playerId):
		self.name = name
		self.playerId = playerId

NAMES = [
		Player("David Ospina", "48844"),
		Player("Petr Cech", "11334"),
		Player("Matt Macey", "113534"),
		Player("Dejan Iliev", "153122"),
		Player("Sead Kolasinac", "111457")
	]

	 

def main():
	print("Creating " + str(len(NAMES)) + " folders")
	for player in NAMES:
		os.mkdir(player.name)
		os.chdir(player.name)
		for x in range(0,100):
			with open(player.playerId + "_H_" + str(x).zfill(5) + ".tga", "w") as file:
				print(str(file) + " created")
		os.chdir("..")

if __name__ == '__main__':
	main()