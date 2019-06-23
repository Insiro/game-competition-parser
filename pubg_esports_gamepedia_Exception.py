import requests
from bs4 import BeautifulSoup
import Month_to_NUM as con
import checkStatus as CS

keyord = {'Organizer', 'Number of Teams', 'Links', 'Region',
          'Type', 'Tier', 'Stream(s)'}
tag = '#infoboxTournament > tbody > tr > td'


def parsetest():
    print(parse('https://pubg-esports.gamepedia.com/PUBG_Master_League/2019_Season/Phase_1/Finals'))


def parse(link):
    status = CS.check(link)
    if status != 0:
        return None
    req = requests.get(link)
    html = req.text
    texts = None
    soup = BeautifulSoup(html, 'html.parser')
    temp = 'Nan'
    data = {'Organizer': None, 'Number of Teams': None, 'Links': None,
            'Region': None, 'Type': None, 'Tier': None, 'Streams': None}
    for block in soup.select(tag):
        texts = block.text
        if temp != 'Nan':
            if temp == 'Links':
                data[temp] = {'name': block.text, 'link': block.a['href']}
            elif temp == 'Organizer':
                data[temp] = list()
                for org in block.select('td > a'):
                    data['Organizer'] .append(
                        {'name': org.text, 'link': org['href']})

            elif temp == 'Stream(s)':
                data['Streams'] = [
                    {'name': block.a.text, 'link': block.a['href']}]
                if block.p != None:
                    for a in block.p.select('a'):
                        data['Streams'].append(
                            {'name': a.text, 'link': a['href']})
            else:
                data[temp] = block.text.split(
                    '\xa0')[1] if temp == 'Region' else block.text
            temp = 'Nan'
        elif len(keyord & {texts}) != 0:
            temp = texts
    return data


parsetest()
