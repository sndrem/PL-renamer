from xml.dom import minidom
import os, zipfile, traceback

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
		os.rename(oldFile, playerFile)
		return True
	except FileExistsError as e:
		print("Could not rename file. The file " + playerFile + " already exists")
		return False
	except FileNotFoundError as e:
		print("Could not find file " + oldFile)
		return False

def createPlayerFileName(player, postfix, fileEnding):
	return player.lastName.replace(" ", "") + "_" + postfix + "." + fileEnding

def unzipFile(file, player):
	print("Unzipping " + file)
	ref = zipfile.ZipFile(file, "r")
	playerDir = player.lastName.replace(" ", "")
	ref.extractall(playerDir)
	ref.close()
	# Rename all files inside directory
	print("Trying to list all files from " + os.path.abspath(playerDir))
	for file in os.listdir(playerDir):
		if file.endswith(".tga"):
			try:
				newPlayerSequenceName = file.replace(player.id, player.lastName.replace(" ", ""))
				newPlayerSequenceName = os.path.abspath(os.path.join(playerDir, newPlayerSequenceName))
				file = os.path.abspath(os.path.join(playerDir, file))
				print("Should rename: " + file + " to " + newPlayerSequenceName + " inside " + playerDir)
				os.rename(file, newPlayerSequenceName)
			except Exception as e:
				traceback.print_tb(e)
				print("Old file: " + file + " ----- New file: " + newPlayerSequenceName)


def runConversion(files, players):
	for file in files:
			playerId = getPlayerIdFromFileName(file)
			for player in players:
				try:
					if player.id in playerId:
						print(player.firstName + " " + player.lastName + " matches with file: " + file)
						playerFile = createPlayerFileName(player, "H", "zip")
						if renameFile(file, playerFile):
							print("Renaming went okay")
							unzipFile(playerFile, player)
							print("")
							print("")
				except Exception as e:
					print("Something went wrong for file " + file)
					traceback.print_tb(e)
def main():
	players = readXML('Player_Opta_IDs.xml')
	files = readFiles('.', '.zip')
	runConversion(files, players)
	


if __name__ == '__main__':
	main()