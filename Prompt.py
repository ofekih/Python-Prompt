from os.path import isfile
from sys import exit

class Prompt(object):
	""" 
	This serves as python's much-needed console input system. 
	Methods in this class have two basic parameters 
	(Note: either one of these is is optional, the methods have default values for both):

		outputText (string) The text to display while asking for an input
		parameters (dictionary) The parameters to customize and control user input

	List of available keys in the parameters dictionary:

		User input control:
		alphabetical (boolean) True if the string has to be made solely of alphabetical chars, False if it cannot have a single one
		even (boolean) True if input value must be even, False if must be odd
		exists (boolean) When getting a filename, checks if file exists or not (False means file cannot already exist)
		exiton (string or string list) When getting multiple inputs, user exits by typing one of these strings
		extension (string) When getting a filename, checks if input's extension matches requested extension
		max (matches 'type') The maximum value for an input
		min (matches 'type') The minimum value for an input
		mult (matches 'type', can be list) User input must be a multiple of all 'mult' values
		factor (matches 'type', can be list) User input must be a factor of all 'factor' values
		mode (string) When getting a file, mode to open with
		numInputs (integer) When getting multiple inputs, program will stop asking after these many inputs
		ranges (2d array matches 'type') Each 1d array is composed of [min, max]
		repeat (boolean) True if it should ask again when user enters incorrect input

		Output control (Note: Error messages don't output except when explicity defined):
		alphabeticalError (string) The text to display when input fails 'alphabetical' check
		errorMessage (string) The generic error message to display
		evenError (string) The text to display when input fails 'even' check
		existsError (string) The text to display when input fails 'exists' check
		extensionError (string) The text to display when input fails 'extension' check
		factorError (string) The text to display when input value is not a factor of all 'factor' values
		maxError (string) The text to display when input value is larger than 'max'
		minError (string) The text to display when input value is smaller than 'min'
		multError (string) The text to display when input value is not a multiple of all 'mult' values
		outputText (string) The text to display while asking for an input
		rangesError (string) The text to display while input value fails one or more 'ranges' checks
		typeError (string) The text to display when input does not match data type

		Behind-the-scenes:
		call (method) The method to call when repeating
		type (data type) The data type of user input
		uniquechecks (method) Any uniquechecks that this data-type should make

	"""
	@staticmethod
	def getString(outputText = "Enter a string:\t", **parameters):
		parameters["outputText"] = outputText
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
	def getStrings(outputText = None, **parameters):
		parameters["exiton"] = Prompt.dealWithList("exiton", "close", **parameters)
		parameters["outputText"] = "Enter a string, " + str(list(parameters["exiton"])) + " to exit:\t"
		if outputText:
			parameters["outputText"] = outputText
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
	def getInput(outputText = "Enter an input:\t", **parameters):
		Prompt.checkParameters(**parameters)
		if "outputText" in parameters:
			return input(parameters["outputText"])
		else:
			return input(outputText)

	@staticmethod
	def dealWithError(customError = None, **parameters):
		if customError in parameters:
			print(parameters[customError])
		elif "errorMessage" in parameters:
			print(parameters["errorMessage"])
		if "repeat" in parameters and not parameters["repeat"]:
			return None
		else:
			return parameters["call"](**parameters)

	@staticmethod
	def dealWithList(listkey, default, **parameters):
		if listkey == "exiton" and "numInputs" in parameters:
			default = None
		if listkey in parameters:
			if not isinstance(parameters[listkey], list):
				parameters[listkey] = [parameters[listkey]]
		else:
			parameters[listkey] = [default]

		return parameters[listkey]

	@staticmethod
	def getFileName(outputText = "Enter a filename:\t", **parameters):
		Prompt.checkParameters(**parameters)
		parameters["outputText"] = outputText
		parameters["call"] = Prompt.getFileName
		name = Prompt.getInput(**parameters)
		if "extension" in parameters:
			try:
				if name[name.index(".")+1:] != parameters["extension"] and name[name.index("."):] != parameters["extension"]:
					return Prompt.dealWithError("extensionError", **parameters)
			except ValueError:
				return Prompt.dealWithError("extensionError", **parameters)

		if "exists" in parameters and (parameters["exists"] != isfile(name)):
			return Prompt.dealWithError("existsError", **parameters)
		return name

	@staticmethod
	def getFile(outputText = "Enter a filename:\t", **parameters):
		Prompt.checkParameters(**parameters)
		name = Prompt.getFileName(outputText, **parameters)
		if "mode" in parameters:
			return open(name, parameters["mode"])
		else:
			return open(name)

	@staticmethod
	def getInt(outputText = "Enter an integer:\t", **parameters):
		parameters["outputText"] = outputText
		parameters["type"] = int
		return Prompt.getComparator(**parameters)

	@staticmethod
	def getInts(outputText = None, **parameters):
		parameters["exiton"] = Prompt.dealWithList("exiton", "close", **parameters)
		if not outputText:
			outputText = "Enter an integer, " + str(list(parameters["exiton"])) + " to exit:\t"
		parameters["type"] = int
		return Prompt.getComparators(outputText, **parameters)

	@staticmethod
	def getFloat(outputText = "Enter a floating-point number:\t", **parameters):
		parameters["outputText"] = outputText
		parameters["type"] = float
		return Prompt.getComparator(**parameters)

	@staticmethod
	def getFloats(outputText = None, **parameters):
		parameters["exiton"] = Prompt.dealWithList("exiton", "close", **parameters)
		if not outputText:
			outputText = "Enter a floating-point number, " + str(list(parameters["exiton"])) + " to exit:\t"
		parameters["type"] = float
		
		return Prompt.getComparators(outputText, **parameters)

	@staticmethod
	def getHex(outputText = "Enter a hexadecimal number:\t", **parameters):
		parameters["outputText"] = outputText
		parameters["type"] = hex
		return Prompt.getComparator(**parameters)
	
	@staticmethod
	def getHexs(outputText = None, **parameters):
		parameters.exiton = Prompt.dealWithList("exiton", "close", **parameters)
		if not outputText:
			outputText = "Enter a hexadecimal number, " + str(list(parameters["exiton"])) + " to exit:\t"
		parameters["type"] = hex
		
		return Prompt.getComparators(outputText, **parameters)

	@staticmethod
	def getNumber(outputText = "Enter a number:\t", **parameters):
		parameters["outputText"] = outputText
		parameters["type"] = float
		return Prompt.getComparator(**parameters)

	@staticmethod
	def getNumbers(outputText = None, **parameters):
		parameters["exiton"] = Prompt.dealWithList("exiton", "close", **parameters)
		if not outputText:
			outputText = "Enter a number, " + str(list(parameters["exiton"])) + " to exit:\t"
		parameters["type"] = float
		
		return Prompt.getComparators(outputText, **parameters)

	@staticmethod
	def getComparator(outputText = "Enter a comparator:\t", **parameters):
		Prompt.checkParameters(**parameters)
		if not "call" in parameters:
			parameters["call"] = Prompt.getComparator
		
		if not "type" in parameters:
			parameters["type"] = float

		if not "outputText" in parameters:
			parameters["outputText"] = outputText

		if "mult" in parameters:
			parameters["mult"] = Prompt.dealWithList("mult", None, **parameters)

		if "factor" in parameters:
			parameters["factor"] = Prompt.dealWithList("factor", None, **parameters)

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

		if "mult" in parameters:
			for mult in parameters["mult"]:
				if name % mult != 0:
					return Prompt.dealWithError("multError", **parameters)

		if "factor" in parameters and parameters["factor"] % name != 0:
			for factor in parameters["factor"]:
				if factor % name != 0:
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
	def getComparators(outputText = None, **parameters):
		parameters["exiton"] = Prompt.dealWithList("exiton", "close", **parameters)

		if outputText:
			parameters["outputText"] = outputText
		else:
			outputText = "Enter a comparator, " + str(list(parameters["exiton"])) + " to exit:\t"

		if not "call" in parameters:
			parameters["call"] = Prompt.getComparator
		
		if "numInputs" in parameters:
			try:
				parameters["outputText"] = parameters["outputText"][:parameters["outputText"].index("[None]")] + str(parameters["numInputs"]) + " left:\t"
			except ValueError:
				pass

		names = []

		while True:
			if "numInputs" in parameters:
				try:
					parameters["outputText"] = parameters["outputText"][:parameters["outputText"].index("left:")-2] + str(parameters["numInputs"]) + " left:\t"
				except ValueError: pass
			name = parameters["call"](**parameters)
			if not name:
				break
			names.append(name)
			if "numInputs" in parameters:
				parameters["numInputs"] -= 1
				if parameters["numInputs"] == 0:
					break

		return names

	@staticmethod
	def getBoolean(outputText = "Enter a boolean value:\t", **parameters):
		Prompt.checkParameters(**parameters)
		if not "outputText" in parameters:
			parameters["outputText"] = outputText
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
	def getBooleans(outputText = None, **parameters):
		Prompt.checkParameters(**parameters)
		parameters["exiton"] = Prompt.dealWithList("exiton", "close", **parameters)
		parameters["outputText"] = "Enter a boolean value, " + str(list(parameters["exiton"])) + " to exit:\t"
		if outputText:
			parameters["outputText"] = outputText
		parameters["type"] = float
		parameters["call"] = Prompt.getBoolean
		
		name = Prompt.getBoolean(**parameters)
		names = []

		while name != None:
			names.append(name)
			name = Prompt.getBoolean(**parameters)

		return names

	@staticmethod
	def checkParameters(**parameters):
		Prompt.checkParamBoolean("alphabetical", **parameters)
		Prompt.checkParamBoolean("even", **parameters)
		Prompt.checkParamBoolean("exists", **parameters)
		Prompt.checkParamBoolean("repeat", **parameters)
		Prompt.checkParamInteger("numInputs", **parameters)

		# checks that mode is a legitimate open file mode
		if "mode" in parameters:
			try:
				open("Prompt.py", parameters["mode"])
			except ValueError:
				Prompt.formatError("mode must be a legitimate open file mode")


		# checks if ranges is formatted correctly
		if "ranges" in parameters:
			try:
				for singleRange in parameters["ranges"]:
					singleRange[0]
					singleRange[1]
			except TypeError:
				Prompt.formatError("ranges must be a 2d array")
			except IndexError:
				Prompt.formatError("ranges must contain arrays in the format [min, max]")

	@staticmethod
	def checkParamBoolean(listkey, **parameters):
		if listkey in parameters:
			if parameters[listkey] != True and parameters[listkey] != False:
				Prompt.formatError(listkey + " must be a boolean value")

	@staticmethod
	def checkParamInteger(listkey, **parameters):
		if listkey in parameters:
			try:
				int(str(parameters[listkey]))
			except ValueError:
				Prompt.formatError(listkey + " must be an integer value")

	@staticmethod
	def formatError(errorMessage):
		print("FORMAT ERROR: " + errorMessage + "\n")
		exit(1)
