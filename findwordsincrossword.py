import sys

CROSSWORD = (
	('d', 's', 't', 'q', 'b',),
	('f', 'r', 'a', 'r', 'f',),
	('n', 'r', 'o', 'w', 'c',),
	('q', 'w', 'a', 'w', 's',),
	('i', 's', 'o', 'f', 'i',),
)

WORDS = (
	"row",
	"rf",
	"i",
	"word",
)

cw_row = len(CROSSWORD)
cw_col = len(CROSSWORD[0])

def print_(text, end = ''):
	print(text, end = end)

def printDash():
	global cw_row, cw_col
	for i in range((cw_col * 4) + 1):
		print_("-");

def printCw(is_exit = False):
	global CROSSWORD, cw_row, cw_col

	print("\n")

	if is_exit:
		print("\nYou can verify it here!\n")

	# Print column numbers (for users! so +1)
	print_(" ");
	for i in range(cw_col):
		print_(f" {i + 1}  ")
		# print_(f" {i}  ")

	print()

	printDash()

	for i in range(cw_row):
		print_("\n|");
		for j in range(cw_col):
			print_(f" {CROSSWORD[i][j]} |")

		# Print row numbers (for users! so +1)
		print(f"  {i + 1}");
		# print(f"  {i}");

		printDash();

	print()

	print("\n")

	if is_exit:
		sys.exit()

def findLocationsOfLetterInCw(letter):
	global CROSSWORD

	locations_list = []

	for i, line in enumerate(CROSSWORD):
		for j, char in enumerate(line):
			if char == letter:
				locations_list.append({"x": i, "y": j})

	return locations_list

def validateSurroundingXAndY(loc_list):
	global cw_row, cw_col

	valid_list = []

	for loc_item in loc_list:
		if loc_item["x"] >= 0 and loc_item["y"] >= 0 and loc_item["x"] < cw_row and loc_item["y"] < cw_col:
			valid_list.append(loc_item)

	return valid_list

def findSurroundingsXAndY(loc_dict):
	loc_list = []
	x = loc_dict["x"]
	y = loc_dict["y"]

	loc_list.append({"x": x + 1, "y": y + 1})
	loc_list.append({"x": x + 1, "y": y - 1})
	loc_list.append({"x": x - 1, "y": y + 1})
	loc_list.append({"x": x - 1, "y": y - 1})
	loc_list.append({"x": x, "y": y - 1})
	loc_list.append({"x": x, "y": y + 1})
	loc_list.append({"x": x + 1, "y": y})
	loc_list.append({"x": x - 1, "y": y})

	return validateSurroundingXAndY(loc_list)

def returnLocation(location):
	# For User +1
	return f'({location["x"] + 1}, {location["y"] + 1})'

def getDirection(loc1, loc2):
	return {"diffx": loc1["x"] - loc2["x"], "diffy": loc1["y"] - loc2["y"], "start": loc2}

def getLettersFromDirection(diff_dict, word):
	global CROSSWORD, cw_row, cw_col

	letters = ""
	locations_list = []

	i = 0
	lenword = len(word)

	x = diff_dict["diffx"]
	y = diff_dict["diffy"]

	sx = diff_dict["start"]["x"]
	sy = diff_dict["start"]["y"]

	# print(f"x = {x} y = {y} sx = {sx} sy = {sy}")

	while True:
		dx = (sx + x)
		dy = (sy + y)

		# print(f"dx = {dx + 1} dy = {dy + 1}")

		if dx >= cw_row or dy >= cw_col or dx < 0 or dy < 0 or i >= lenword:
			# print(f"BREAKING! dx = {dx} dy = {dy}")
			break
		else:
			letter = CROSSWORD[dx][dy]

			# print("Letter:")
			# print(letter)
			# print(f"i={i}")

			if letter != word[i]:
				return (False, [],)
			else:
				i += 1

				letters += letter

				locations_list.append({"x": dx, "y": dy})

				sx = dx
				sy = dy

	return (letters, locations_list,)

def handleWords(word):
	global CROSSWORD, cw_row, cw_col, WORDS
	wordlen = len(word)

	if wordlen != 0:
		locations = findLocationsOfLetterInCw(word[0])

		if len(locations) > 0:
			if wordlen == 1:
				print(f'Character "{word}" found at the following location(s):')

				for location in locations:
					print(returnLocation(location))

				printCw(True)

			else:
				if wordlen == 2:
					for location in locations:
						surroundingsXAndY = findSurroundingsXAndY(location)

						# print("surroundings:", surroundingsXAndY)

						for surroundingXAndY in surroundingsXAndY:
							if CROSSWORD[surroundingXAndY["x"]][surroundingXAndY["y"]] == word[1]:
								print(returnLocation(location), "&", returnLocation(surroundingXAndY))
								return
				else:
					# print("ALL LOCATIONS:")
					# print(locations)

					for location in locations:
						surroundingsXAndY = findSurroundingsXAndY(location)

						# print("ALL surroundingsXAndY")
						# print(surroundingsXAndY)

						for surroundingXAndY in surroundingsXAndY:
							direction = getDirection(location, surroundingXAndY)

							# print("Location:")
							# print(location)

							# print("SurroundingXAndY:")
							# print(surroundingXAndY)

							# print("Direction:")
							# print(direction)

							# print()
							# print()

							letters, locations_list = getLettersFromDirection(direction, word)

							if letters is not False:
								if len(letters) == len(word):
									print(f'Word "{word}" found!')
									print("Following are the co-ordinates:")

									for location_item in locations_list[:-1]:
										print_(returnLocation(location_item))
										print_(" & ")

									print_(returnLocation(locations_list[-1]))

									print()

									return

		else:
			print(f'No matches for "{word}"...')
	else:
		print(f"Word number {i} has length 0... So it is not valid!")

def main():
	for i, word in enumerate(WORDS, start = 1):
		print(f'Working on\t{i}\t==> "{word}"')
		handleWords(word)
		printCw()

if __name__ == "__main__":
	main()

