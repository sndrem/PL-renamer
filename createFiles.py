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
		Player("Sindre", "198291"), 
		Player("Ørjan", "9876242"),
		Player("Kåre", "12344") 
	]

def main():
	print("Creating " + str(len(NAMES)) + " folders")
	for player in NAMES:
		os.mkdir(player.name)
		os.chdir(player.name)
		for x in range(0,100):
			with open(player.playerId + "_" + str(x).zfill(3) + ".tga", "w") as file:
				print(str(file) + " created")
		os.chdir("..")

if __name__ == '__main__':
	main()