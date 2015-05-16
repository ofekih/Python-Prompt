from os.path import isfile

class Prompt(object):
	@staticmethod
	def getString(defaultText = "Enter a string:\t", **parameters):
		parameters["defaultText"] = defaultText
		parameters["type"] = str
		parameters["call"] = Prompt.getString
		parameters["uniquechecks"] = Prompt.checkString
		return Prompt.getComparator(**parameters)

	@staticmethod
	def checkString(name, **parameters):
		if "alphabetical" in parameters and parameters["alphabetical"] != Prompt.alpha(name):
			return Prompt.dealWithError("alphabeticalError", **parameters)
		return name

	@staticmethod
	def getStrings(defaultText = None, **parameters):
		parameters["exiton"] = Prompt.dealWithList("exiton", "close", **parameters)
		parameters["defaultText"] = "Enter a string, " + str(list(parameters["exiton"])) + " to exit:\t"
		if defaultText:
			parameters["defaultText"] = defaultText
		parameters["type"] = str
		parameters["uniquechecks"] = Prompt.checkString
		
		return Prompt.getComparators(**parameters)

	@staticmethod
	def alpha(name):
		newname = ""
		for item in name:
			if item != ' ':
				newname += item
		if newname.isalpha():
			return True
		for item in name:
			if (item >= 'a' and item <= 'z') or (item >= 'A' and item <= 'Z'):
				return None
		return False

	@staticmethod
	def getInput(defaultText = "Enter an input:\t", **parameters):
		if "outputText" in parameters:
			return input(parameters["outputText"])
		elif "defaultText" in parameters:
			return input(parameters["defaultText"])
		else:
			return input(defaultText)

	@staticmethod
	def dealWithError(customError = None, **parameters):
		if customError in parameters:
			print(parameters[customError])
		elif "errorMessage" in parameters:
			print(parameters["errorMessage"])
		if ("repeat" in parameters and not parameters["repeat"]) or ("defaultRepeat" in parameters and not parameters["defaultRepeat"]):
			return None
		else:
			return parameters["call"](**parameters)

	@staticmethod
	def dealWithList(listkey, default, **parameters):
		if listkey in parameters:
			if not isinstance(parameters[listkey], list):
				parameters[listkey] = [parameters[listkey]]
		else:
			parameters[listkey] = [default]

		return parameters[listkey]

	@staticmethod
	def getFileName(defaultText = "Enter a filename:\t", **parameters):
		parameters["defaultText"] = defaultText
		parameters["call"] = Prompt.getFileName
		name = Prompt.getInput(**parameters)
		if "extension" in parameters:
			try:
				if name[name.index(".")+1:] != parameters["extension"] and name[name.index("."):] != parameters["extension"]:
					return Prompt.dealWithError("extensionError", **parameters)
			except ValueError:
				return Prompt.dealWithError("extensionError", **parameters)

		if "exists" in parameters and parameters["exists"]:
			if not isfile(name):
				return Prompt.dealWithError("existsError", **parameters)
		return name

	@staticmethod
	def getFile(defaultText = "Enter a filename:\t", **parameters):
		name = Prompt.getFileName(defaultText, **parameters)
		if "mode" in parameters:
			return open(name, parameters["mode"])
		else:
			return open(name)

	@staticmethod
	def getInt(defaultText = "Enter an integer:\t", **parameters):
		parameters["defaultText"] = defaultText
		parameters["type"] = int
		return Prompt.getComparator(**parameters)

	@staticmethod
	def getInts(defaultText = None, **parameters):
		parameters["exiton"] = Prompt.dealWithList("exiton", "close", **parameters)
		parameters["defaultText"] = "Enter an integer, " + str(list(parameters["exiton"])) + " to exit:\t"
		if defaultText:
			parameters["defaultText"] = defaultText
		parameters["type"] = int
		
		return Prompt.getComparators(**parameters)

	@staticmethod
	def getFloat(defaultText = "Enter a floating-point number:\t", **parameters):
		parameters["defaultText"] = defaultText
		parameters["type"] = float
		return Prompt.getComparator(**parameters)

	@staticmethod
	def getFloats(defaultText = None, **parameters):
		parameters["exiton"] = Prompt.dealWithList("exiton", "close", **parameters)
		parameters["defaultText"] = "Enter a floating-point number, " + str(list(parameters["exiton"])) + " to exit:\t"
		if defaultText:
			parameters["defaultText"] = defaultText
		parameters["type"] = float
		
		return Prompt.getComparators(**parameters)

	@staticmethod
	def getHex(defaultText = "Enter a hexadecimal number:\t", **parameters):
		parameters["defaultText"] = defaultText
		parameters["type"] = hex
		return Prompt.getComparator(**parameters)
	
	@staticmethod
	def getHexs(defaultText = None, **parameters):
		parameters.exiton = Prompt.dealWithList("exiton", "close", **parameters)
		parameters["defaultText"] = "Enter a hexadecimal number, " + str(list(parameters["exiton"])) + " to exit:\t"
		if defaultText:
			parameters["defaultText"] = defaultText
		parameters["type"] = hex
		
		return Prompt.getComparators(**parameters)

	@staticmethod
	def getNumber(defaultText = "Enter a number:\t", **parameters):
		parameters["defaultText"] = defaultText
		parameters["type"] = float
		return Prompt.getComparator(**parameters)

	@staticmethod
	def getNumbers(defaultText = None, **parameters):
		parameters["exiton"] = Prompt.dealWithList("exiton", "close", **parameters)
		parameters["defaultText"] = "Enter a number, " + str(list(parameters["exiton"])) + " to exit:\t"
		if defaultText:
			parameters["defaultText"] = defaultText
		parameters["type"] = float
		
		return Prompt.getComparators(**parameters)

	@staticmethod
	def getComparator(defaultText = "Enter a comparator:\t", **parameters):
		if not "call" in parameters:
			parameters["call"] = Prompt.getComparator
		
		if not "type" in parameters:
			parameters["type"] = float

		if not "defaultText" in parameters:
			parameters["defaultText"] = defaultText

		name = Prompt.getInput(**parameters)

		if "exiton" in parameters:
			for exitcase in parameters["exiton"]:
				if name == exitcase:
					return None

		try:
			name = parameters["type"](name)
		except ValueError:
			return Prompt.dealWithError("typeError", **parameters)

		if "min" in parameters and name < parameters["min"]:
			return Prompt.dealWithError("minError", **parameters)

		if "max" in parameters and name > parameters["max"]:
			return Prompt.dealWithError("maxError", **parameters)

		if "mult" in parameters and name % parameters["mult"] != 0:
			return Prompt.dealWithError("multError", **parameters)

		if "factor" in parameters and parameters["factor"] % name != 0:
			return Prompt.dealWithError("factorError", **parameters)

		if "even" in parameters:
			if (parameters["even"] and name % 2 == 1) or (not parameters["even"] and name % 2 == 0):
				return Prompt.dealWithError("evenError", **parameters)

		if "ranges" in parameters:
			printError = True
			for singleRange in parameters["ranges"]:
				if name >= singleRange[0] and name <= singleRange[1]:
					printError = False
			if printError:
				return Prompt.dealWithError("rangesError", **parameters)

		if "uniquechecks" in parameters:
			name = parameters["uniquechecks"](name, **parameters)

		return name

	@staticmethod
	def getComparators(defaultText = None, **parameters):
		if not "call" in parameters:
			parameters["call"] = Prompt.getComparator
		name = parameters["call"](**parameters)
		names = []

		while name:
			names.append(name)
			name = parameters["call"](**parameters)

		return names

	@staticmethod
	def getBoolean(defaultText = "Enter a boolean value:\t", **parameters):
		if not "defaultText" in parameters:
			parameters["defaultText"] = defaultText
		parameters["call"] = Prompt.getBoolean
		name = Prompt.getInput(**parameters)

		if "exiton" in parameters:
			for exitcase in parameters["exiton"]:
				if name == exitcase:
					return None

		return Prompt.checkBoolean(name, **parameters)

	@staticmethod
	def checkBoolean(name, **parameters):
		if name.lower() == "true":
			return True
		elif name.lower() == "false":
			return False
		else:
			return Prompt.dealWithError(**parameters)

	@staticmethod
	def getBooleans(defaultText = None, **parameters):
		parameters["exiton"] = Prompt.dealWithList("exiton", "close", **parameters)
		parameters["defaultText"] = "Enter a boolean value, " + str(list(parameters["exiton"])) + " to exit:\t"
		if defaultText:
			parameters["defaultText"] = defaultText
		parameters["type"] = float
		parameters["call"] = Prompt.getBoolean
		
		name = Prompt.getBoolean(**parameters)
		names = []

		while name != None:
			names.append(name)
			name = Prompt.getBoolean(**parameters)

		return names
