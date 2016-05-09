import urllib.request
import csv


model = {
	# 'url': {'anchor': anchor,
	# 		  'crawled': true/false,
	# },
}

crawlingList = []




def saveCSV(file):
	with open(file, 'w', encoding='utf8', newline='') as csvfile:
		csvwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for url in model:	
			csvwriter.writerow([url, model[url]['anchor'], model[url]['crawled']])


def insertCSV(file):
	with open(file, 'a', encoding='utf8', newline='') as csvfile:
		csvwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for url in model:	
			csvwriter.writerow([url, model[url]['anchor'], model[url]['crawled']])

def appendLine(file, lineArr):
	with open(file, 'a', encoding='utf8', newline='') as csvfile:
		csvwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		csvwriter.writerow(lineArr)

def fromCSVtoModel(file):
	with open(file, 'r', encoding='utf8', newline='') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for row in csvreader:
			model[row[0]] = {'anchor': row[1], 'crawled': row[2]}

def getHTML(url):
	response = urllib.request.urlopen('https://www.kfzteile24.de' + url)
	if response.getcode() != 200:
		print ('error ' + response.getcode() + ' on ' + url)
		return 'error'

	else:
		data = response.read() 
		return(data.decode('latin-1'))


def passLinkstoModel(html):


	# for special pages with boxes instead of list of links
	if '<div class="productGroupBanner marginBottomMedium">' in html:

		html = html.split('class="standard "')
		for piece in html[1:]:
			url = piece.split('href="')[1].split('"')[0]
			anchor = piece.split('style="width: 99%; margin-top: -10px;">')[1].split('</div></a>')[0].strip()
			model[url] = {'anchor': anchor, 'crawled': 'False'}


	# for the normal pages
	else:	
	
		html = html.split('<div class="borderBox width100">')
		for piece in html[1:]:
			if 'style="width: 100%; margin-top: 0px; display: inline-block;">' in piece:
				
				# extract links

				# to extract the first link it has to be different
				url = piece.split('<a href="')
				if (len(url) > 1):
					url = url[-1].split('"')[0]
				else:
					url = piece.split('<a href="')[1].split('"')[0]
				anchor = piece.split('style="width: 100%; margin-top: 0px; display: inline-block;">')[1].split('</div>')[0].strip()
				model[url] = {'anchor': anchor, 'crawled': 'False'}
				# print(url)


def test(uri):
	html = getHTML(uri)
	passLinkstoModel(html)
	print(model)



def listCrawler(urls):

	for url in urls:

		print(url)
		html = getHTML(url)
		passLinkstoModel(html)
		model[url]['crawled'] = 'True'

		
		


def superController(input, output):
	

	# another option is to do a check up of all the keys in the model to see if any of them is
	# still to be crawled

	fromCSVtoModel(input)
	updateCrawlingList()

	while crawlingList != []:
		listCrawler(crawlingList)
		saveCSV(output)
		updateCrawlingList()


	print('superController finished')



def updateCrawlingList():

	# reset 
	crawlingList = []

	for url in model:
		if model[url]['crawled'] == 'False':
			crawlingList.append(url)


# superController('leftNav.csv', 'result.csv')
test('/reifen-felgen-komplettraeder')



# html = getHTML('/ersatzteile-verschleissteile/bremsanlage')
# passLinkstoModel(html)
# print (model)

