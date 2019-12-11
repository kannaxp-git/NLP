import urllib
import urllib.request
import urllib.parse
data=urllib.parse.urlencode({"text":"survey too long."})
binary_data = data.encode('utf8')
u = urllib.request.urlopen("http://text-processing.com/api/sentiment/", binary_data)
the_page = u.read()
print(the_page)
