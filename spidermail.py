import requests as req
import re
import os
import os.path

# these are from https://github.com/Boredsoft/email-spider
email_pattern = re.compile(r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+(?:[A-Z]{2}|com|org|net|edu|gov|mil|biz|info|mobi|name|aero|asia|jobs|museum|mx|com\.mx|xxx|tv|tk)\b")
url_pattern = re.compile(r'href=[\'"]?([^\'" >]+)')

# this is following https://github.com/kennethreitz/requests/issues/557
if os.path.exists('cacert.pem'):
	os.environ['REQUESTS_CA_BUNDLE'] = 'cacert.pem'

max_depth = 1


def load_urls(filename="urls.txt"):
    urls = {}
    with open(filename) as fin:
        for line in fin:
            urls[line.strip()] = 0
    return urls

# urls = load_urls()


def get_base_url(url):
    if url.startswith('http://'):
        i = url[7:].index('/')
        base_url = url[:i+7]
    else:
        i = url.index('/')
        base_url = url[:i]
    return base_url

#base_url = get_base_url(urls.keys()[0])


def get_urls(url, depth):
    base_url = get_base_url(url)
    r = req.get(url)
    if not r.ok:
        print "** Failed getting links from", url
        return
    links = url_pattern.findall(r.content)
    print "%d links from %s" % (len(links), url)
    urls = {}
    for link in links:
        if link.startswith('/'):
            link = base_url + link
        elif not link.startswith(base_url):
            continue
        urls[link] = depth + 1
    return urls


def get_emails(url):
    r = req.get(url)
    if not r.ok:
        print "** Failed getting emails from", url
        return []
    emails = email_pattern.findall(r.content)
    emails = list(set(emails))
    print "%d emails from %s" % (len(emails), url)
    return emails
        
# get_emails(r'/faculty/directory/10010/Alford')


def crawl(urls):
    emails = []
    links = {}
    for url,depth in urls.items():
        emails.extend( get_emails(url) )
        if depth < max_depth:
            links.update( get_urls(url,depth) )
    if links:
        emails.extend( crawl(links) )
    return emails


def write_emails(emails, filename="emails.txt"):
    with open(filename, 'w') as fout:
        for em in emails:
            fout.write(em)
            fout.write('\n')
    print "%d emails written to %s" % (len(emails), filename)


if __name__ == '__main__':
	urls = load_urls()
	emails = crawl(urls)
	write_emails(emails)