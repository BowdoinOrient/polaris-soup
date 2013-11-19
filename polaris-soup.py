from bs4 import BeautifulSoup

def target_tag(tag):
    print tag.contents[0]
    return tag(rowspan = "1")

fname = "./data.html"
with open(fname) as file:
    htmllist = file.readlines()
    html = "".join(htmllist)

soup = BeautifulSoup(html)

tds = soup.find_all(target_tag)

print len(tds)

classes = []

for title, attrs in zip(tds[:-1], tds[1:]):
    cl = (title, attrs)
    classes.append(cl)