from bs4 import BeautifulSoup

fname = "./data.html"
with open(fname) as file:
    htmllist = file.readlines()
    html = "".join(htmllist)

soup = BeautifulSoup(html)

rts = soup.find_all("tr", {"class":"rowtop"})
pds = soup.find_all("tr", {"class":"popdown"})

derp = zip(rts, pds)

classes = []

for (pd, rt) in derp:
    classes.append({"title":pd, "detail":rt})