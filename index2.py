import urllib.request
import csv

# the crawler will just crawl the complete category tree
# and apply the func(args) to each uri crawled
# the different tools have to be send on the func(args) through the controller
class Crawler:

	def __init__(self, func):

		self.func = func
		self.output = 'output.csv'
		
		self.waitingList = []
		self.model = {
		'/ersatzteile-verschleissteile':  {'anchor': 'Ersatzteile | Verschleißteile', 'crawled': False},
		'/reifen-felgen-komplettraeder':  {'anchor': 'Reifen | Felgen | Kompletträder', 'crawled': False},
		'/batterien-ladegeraete-wandler': {'anchor': 'Batterien | Ladegeräte | Wandler', 'crawled': False},
		'/additive-oele-schmierung':      {'anchor': 'Additive | Öle | Schmierung', 'crawled': False},
		'/pflegemittel-wartungsmittel':   {'anchor': 'Pflegemittel | Wartungsmittel', 'crawled': False},
		'/zubehoer-pannenhilfe':          {'anchor': 'Zubehör | Pannenhilfe', 'crawled': False},
		'/saisonartikel-frostschutz':     {'anchor': 'Saisonartikel | Frostschutz', 'crawled': False},
		'/gluehlampen-leuchtmittel':      {'anchor': 'Glühlampen | Leuchtmittel', 'crawled': False},
		'/dachboxen-und-traegersysteme':  {'anchor': 'Dachboxen, Trägersysteme, Anhängerkupplungen', 'crawled': False},
		'/tuning-und-styling':            {'anchor': 'Tuning & Styling', 'crawled': False},
		'/werkzeug-werkstatt':            {'anchor': 'Werkzeug | Werkstatt', 'crawled': False},
		}

	def fetchHTML(self, uri):
		response = urllib.request.urlopen('https://www.kfzteile24.de' + uri)
		if response.getcode() != 200:
			print ('error ' + response.getcode() + ' on ' + uri)
			return 'error'

		else:
			data = response.read()
			self.model[uri]['crawled'] = True
			# print (uri + ' crawled')

			# apply the func
			func(uri)
			self.appendLine([uri, self.model[uri]['anchor'], self.model[uri]['crawled']])
			return(data.decode('latin-1'))

	def test(self, uri):

		# print the model + a uri you gave as argument

		print('')
		print('')
		print('')
		print('in this uri: ' + uri)
		html = self.fetchHTML(uri)
		self.passLinkstoModel(html)
		
		for key in self.model:
			print(self.model[key]['anchor'] + '     ->' + key)


	def appendLine(self, lineArr):
		with open(self.output, 'a', encoding='utf8', newline='') as csvfile:
			csvwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			csvwriter.writerow(lineArr)

	def passLinkstoModel(self, html):


		# for special pages with boxes instead of list of links
		if '<div class="productGroupBanner marginBottomMedium">' in html:

			html = html.split('class="standard "')
			for piece in html[1:]:
				uri = piece.split('href="')[1].split('"')[0]
				anchor = piece.split('style="width: 99%; margin-top: -10px;">')[1].split('</div></a>')[0].strip()
				self.model[uri] = {'anchor': anchor, 'crawled': False}


		# for the normal pages
		else:	
		
			html = html.split('<div class="borderBox width100">')
			for piece in html[1:]:
				if 'style="width: 100%; margin-top: 0px; display: inline-block;">' in piece:
					
					# extract links

					# to extract the first link it has to be different
					uri = piece.split('<a href="')
					if (len(uri) > 1):
						uri = uri[-1].split('"')[0]
					else:
						uri = piece.split('<a href="')[1].split('"')[0]
					anchor = piece.split('style="width: 100%; margin-top: 0px; display: inline-block;">')[1].split('</div>')[0].strip()
					self.model[uri] = {'anchor': anchor, 'crawled': False}


	def spider(self):
		# it crawls all the category uri's

		self.updateWaitingList()

		while self.updateWaitingList != []:
			self.updateWaitingList()
			for uri in self.waitingList:
				html = self.fetchHTML(uri)
				self.passLinkstoModel(html)
				# self.waitingList.remove(uri)

		print('done')


	
	def updateWaitingList(self):
		# it pass to self.waitingList the uri's that has 'crawled' as False

		# reset
		self.waitingList = []
		
		for uri in self.model:
			if self.model[uri]['crawled'] == False:
				self.waitingList.append(uri)
	

def func(uri):
	print (uri + '  wo')

crawler = Crawler(func)
crawler.spider()
