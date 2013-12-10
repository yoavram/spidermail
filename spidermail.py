import requests as req
import re
import os
import os.path

# this is from https://gist.github.com/dideler/5219706
email_pattern = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                    "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                    "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))
# these are from https://github.com/Boredsoft/email-spider
#email_pattern = re.compile(r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+(?:[A-Z]{2}|com|org|net|edu|gov|mil|biz|info|mobi|name|aero|asia|jobs|museum|mx|com\.mx|xxx|tv|tk)\b")
url_pattern = re.compile(r'href=[\'"]?([^\'" >]+)')

# this is following https://github.com/kennethreitz/requests/issues/557
if os.path.exists('cacert.pem'):
	os.environ['REQUESTS_CA_BUNDLE'] = 'cacert.pem'

max_depth = 1


def load_urls(filename="urls.txt"):
    urls = {}
    with open(filename) as fin:
        for line in fin:
            if not line.startswith("#"):
                fields = line.strip().split(' ')
                url = fields[0]
                prefix = url[:-1-url[::-1].index('/')]
                if len(fields) > 1:
                    prefix = fields[1]
                urls[url] = prefix
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


def get_urls(url, prefix=''):
    if prefix == '':
        prefix = url
    urls = {}
    base_url = get_base_url(url)
    try:
        r = req.get(url)
    except req.ConnectionError:
        print "Failed connecting to", url
        return urls
    if not r.ok:
        print "Failed getting links from", url
        return urls
    links = url_pattern.findall(r.content)
    print "%d links in %s" % (len(links), url)
    for link in links:        
        if link.startswith('/'):
            link = base_url + link        
        if link.startswith(prefix):
            urls[link] = prefix
    print "%d urls from %s" % (len(urls), url)
    return urls


def get_emails(url):
    try:
        r = req.get(url)
    except req.ConnectionError:
        print "Failed connecting to", url
        return []
    if not r.ok:
        print "** Failed getting emails from", url
        return []
    emails = [email[0] for email in re.findall(email_pattern, r.content) if not email[0].startswith('//')]
    emails = list(set(emails))
    print "%d emails from %s" % (len(emails), url)
    return emails
        
# get_emails(r'/faculty/directory/10010/Alford')


def crawl(urls, depth=0):
    emails = []
    links = {}
    for url,prefix in urls.items():
        emails.extend( get_emails(url) )
        if depth < max_depth:
            links.update( get_urls(url,prefix) )
    if links:
        emails.extend( crawl(links, depth + 1) )
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