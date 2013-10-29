import urllib, signal, os
import simplejson # install with pip
try:
	import config
except:
	print ("You must configure config.py.template and rename\n"
		" it to config.py to use this tool.")
	exit()

flikrApiUrl = "http://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=2a5a2148ffc21588facb65536aa91b7d&extras=dims_o%2Curl_o%2Cviews&per_page=500&media=photos&format=json&nojsoncallback=1"
for search in config.searches:
	page = 1
	while True:
		print "Grabbing new page from Flikr API"
		recentPhotos = simplejson.loads(urllib.urlopen("%s&text=%s&page=%s"%(flikrApiUrl, search, page)).read())
		for photo in recentPhotos['photos']['photo']:
			if 'url_o' in photo and 'id' in photo and config.matchesCriteria(photo):
				filename = config.downloadAs(photo)
				if os.path.exists(filename):
					print "Photo '%s' has already been downloaded. Ignoring."%filename
				else:
					try:
						print "Downloading %s"%filename
						image = urllib.urlopen(photo['url_o']).read()
						with open(filename, 'w+') as f:
							f.write(image)
						print "Done."
					except KeyboardInterrupt:
						raise
					except:
						print "Failed to download %s"%filename
		page += 1
		if page > recentPhotos['photos']['pages']:
			break
print "Downloaded all new photos from the recent photo feed that match your criteria."
