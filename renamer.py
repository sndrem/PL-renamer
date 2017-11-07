from xml.dom import minidom
import os, zipfile, traceback, sys
from unidecode import unidecode
import json

PLAYER_FILE = "players.json"
FAILED = []

class Player(object):
		id = 0
		firstName = ""
		lastName = ""

		def __init__(self, id, firstName, lastName):
			self.id = id
			self.firstName = firstName
			self.lastName = lastName


def readFiles(src, fileEnding):
	listOfFiles = []
	for file in os.listdir(src):
		if file.endswith(fileEnding):
			
			listOfFiles.append(os.path.abspath(file))
			print(os.path.abspath(file))
	return listOfFiles

def readXML(xmlFile):
	players = []
	xmldoc = minidom.parse(xmlFile)
	itemlist = xmldoc.getElementsByTagName('Player')

	for s in itemlist:
	    
	    if(s.getElementsByTagName('Name').length > 0):
	    	playerID = s.attributes['uID'].value
	    	name = s.getElementsByTagName('Name')[0].firstChild.nodeValue
	    	firstName = s.getElementsByTagName('Stat')[0].firstChild.nodeValue
	    	lastName = s.getElementsByTagName('Stat')[1].firstChild.nodeValue
	    	players.append(Player(playerID, firstName, lastName))

	return players

def readJson(jsonFile):
	players = []
	with open(jsonFile, 'r') as file:
		jsonData = json.load(file)

		for team in jsonData['teams']:
			# print("\n\n" + team['teamName'] + "\n")
			for player in team['players']:
				# print(player['playerName'] + " - ID: " + player['playerId'])
				nameParts = player['playerName'].split(" ")

				firstName = nameParts[0]
				lastName = " ".join(nameParts[1:len(nameParts) + 1])
				
				players.append(Player(firstName, lastName, player['playerId']))


	return players

def getPlayerIdFromFileName(filename):
	try:
		startIndex = int(filename.index("-"))
		endIndex = int(filename.index(".zip"))
		playerId = filename[startIndex + 1:endIndex]
	except ValueError as e:
		print("Could not find player id from filename: " + filename)
		playerId = ""
	return playerId

def renameFile(oldFile, playerFile):
	
	print("Renaming: " + oldFile + " to " + playerFile)
	try:
		os.rename(oldFile, unidecode(playerFile))
		return True
	except FileExistsError as e:
		print("Could not rename file. The file " + playerFile + " already exists")
		return False
	except FileNotFoundError as e:
		print("Could not find file " + oldFile)
		return False

def createPlayerFileName(player, postfix, fileEnding):
	return player.lastName.replace(" ", "") + "_" + postfix + "." + fileEnding

def unzipFile(file, player, postfix):
	print("Unzipping " + file)
	ref = zipfile.ZipFile(file, "r")
	playerDir = player.lastName.replace(" ", "")
	ref.extractall(playerDir)
	ref.close()
	print(player.firstName + " " + player.lastName + " unzipped")


def runConversion(files, players, home):
	for file in files:
			playerId = getPlayerIdFromFileName(file)
			for player in players:
				try:
					if player.id in playerId:
						print(player.firstName + " " + player.lastName + " matches with file: " + file)
						if home:	
							playerFile = createPlayerFileName(player, "H", "zip")
						else:
							playerFile = createPlayerFileName(player, "A", "zip")
						if renameFile(file, playerFile):
							print("Renaming went okay")
							if home:
								unzipFile(playerFile, player, "H")
							else:
								unzipFile(playerFile, player, "A")
							print("")
							print("")
				except Exception as e:
					print("Something went wrong for file " + file)
					FAILED.append(file)
					traceback.print_tb(e)

def renamePlayerFolders(src, home):
	listOfFiles = []
	for file in os.listdir(src):
		if(os.path.isdir(file) and not file.startswith(".")):
			playerName = unidecode(file)
			os.chdir(os.path.abspath(file))
			for childFile in os.listdir("."):
				print(childFile)
				try:
					underscoreIndex = childFile.index("_")
					newNameStart = childFile[:underscoreIndex]
				except:
					print(childFile + " without underscore")
					FAILED.append(childFile)
				if home:
					newName = childFile.replace(newNameStart, playerName + "_H")
				else:
					newName = childFile.replace(newNameStart, playerName + "_A")
				os.rename(childFile, newName)
			os.chdir("..")

def main(x):
	print("Reading from {}".format(PLAYER_FILE))
	players = readJson(PLAYER_FILE)
	print("\n{} players found in {}".format(len(players), PLAYER_FILE))
	
	print("Reading .zip files")
	files = readFiles('.', '.zip')
	print("\n{} .zip files found".format(len(files)))

	print("\nConverting...")
	runConversion(files, players, x)
	# renamePlayerFolders(".", home)
	# for failed in FAILED:
	# 	print("Failed: " + failed)

def addPostFixToFileName(filename, postfix):
	index = filename.find("_")
	print("Index is: " + str(index))
	newFilename = filename[:index + 1] + postfix + filename[index:]
	print(newFilename)
	return newFilename

if __name__ == '__main__':
	if(len(sys.argv) == 1):
		print("Please provide an argument after the script name: Use either --h for home team or --a for away team")
	else:
		x = sys.argv[1]
		if(x == "--h"):
			main(True)
		elif(x == "--a"):
			main(False)
		else:
			print("Please provide a valid argument (--h for home or --a for away)")
