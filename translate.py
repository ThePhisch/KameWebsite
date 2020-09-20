import csv

def test():
	return "translate!!"

class Translator():
	def __init__(self, csvLocation = 'static/translations.csv', currentLang=0):
		self.langs = []
		self.dic = {}
		self.currentLang = currentLang

		with open(csvLocation) as file:
			reader = list(csv.reader(file))
			for i in range(len(reader[0][1:])): # skip first entry
				self.langs.append({})
				self.dic[reader[0][i+1]] = i
			for row in reader[1:]: # skip first line
				for i in range(len(self.langs)):
					self.langs[i][str(row[0])] = str(row[i+1])

	def test(self):
		print(self.langs[0]['LANGUAGE'])

	def getString(self, ID):
		try:
			return self.langs[self.currentLang][str(ID)]
		except KeyError:
			return str(ID)

	def g(self, ID):
		return self.getString(ID)

	def setLang(self, ID):
		try:
			self.currentLang = self.dic[str(ID)]
		except KeyError:
			pass

