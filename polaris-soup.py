from bs4 import BeautifulSoup
import re
import sqlite3

class Cl:
    def __init__(self, title, detail):
        self.detailsoup = detail
        self.titlesoup = title

        self.parse()

    def parse(self):
        for tag in self.titlesoup.find('h5', {"class":"cf-course-title"}):
            self.name = re.sub("'", "''", tag)

        for tag in self.detailsoup.find_all('h4'):
            if tag.contents[0] == u'Course Description':
                self.description = tag.next.next.contents[0]
                try:
                    self.description = re.sub("'", "''", self.description)
                except:
                    self.description = ""

        for tag in self.titlesoup.find('div', {"class":"cf-course-code"}):
            code = re.split(" ", tag)
            self.dept = code[0]
            self.number = code[1]

        seats = self.detailsoup.find('table', {"class":"seats-cf"})
        data = seats.find_all('tr')[1]
        self.cap = int(data.contents[0].string)
        self.registered = int(data.contents[1].string)
        self.vacancies = int(data.contents[2].string)
        self.pending = int(data.contents[3].string)

        tds = self.titlesoup.find_all('td', {"rowspan":"1"}) + self.titlesoup.find_all('td', {"rowspan":"2"})
        self.prof = re.sub("'", "''", tds[4].contents[0].strip())
        self.distros = []
        for line in re.findall(r">(a|b|c|VPA|ESD|INS)<", str(tds[3].contents)):
            self.distros.append(line)

    def isFull(self):
        if self.registered >= self.cap:
            return True
        return False

    def vacancies(self):
        return self.cap - self.registered


fname = "./data.html"
with open(fname) as file:
    htmllist = file.readlines()
    html = "".join(htmllist)

soup = BeautifulSoup(html)

rts = soup.find_all("tr", {"class":"rowtop"})
pds = soup.find_all("tr", {"class":"popdown"})

derp = zip(rts, pds)

classes = []

conn = sqlite3.connect('registration.db')
c = conn.cursor()
c.execute('''DROP TABLE IF EXISTS registration''')
c.execute('''CREATE TABLE registration
             (name text, dept text, prof text, num int, cap int, registered int, vacancies int, distros text, description text)''')
conn.commit()

for (pd, rt) in derp:
    cl = Cl(pd, rt)
    classes.append(cl)

    insert = "INSERT INTO registration VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(cl.name.encode("punycode"), cl.dept, cl.prof, cl.number, str(cl.cap), str(cl.registered), str(cl.vacancies), ", ".join(cl.distros), cl.description.encode('punycode'))
    c.execute(insert)

conn.commit()
conn.close()



