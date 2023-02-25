import time

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")
now = datetime.now()  # current date and time
ser = Service('chromedriver.exe')
driver = webdriver.Chrome(service=ser, options=options)

all_data = []

def get_teams_details(name,team_id):
    teamdet=[]
    headers = {
        'authority': 'api.sofascore.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'if-none-match': 'W/"3e1f6f6b1b"',
        'origin': 'https://www.sofascore.com',
        'referer': 'https://www.sofascore.com/',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    }

    response = requests.get(f'https://api.sofascore.com/api/v1/team/{team_id}/events/last/0', headers=headers).json()
    events_td = response.get('events')
    for etd in events_td:
        teamdet.append(get_name(etd))
    return teamdet

def get_h2h(custom):
    h2h=[]
    headers = {
        'authority': 'api.sofascore.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'origin': 'https://www.sofascore.com',
        'referer': 'https://www.sofascore.com/',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    }

    response = requests.get(f'https://api.sofascore.com/api/v1/event/{custom}/h2h/events', headers=headers).json()
    eventsh2h = response.get('events')
    for eh2h in eventsh2h:
        h2h.append(get_name(eh2h))
    return h2h
def get_team_streaks(match_id):
    teamdic={}
    headers = {

        'referer': 'https://www.sofascore.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    }

    response = requests.get(f'https://api.sofascore.com/api/v1/event/{match_id}/team-streaks', headers=headers).json()
    general=response.get('general')
    hometeam={}
    awayteam={}
    for g in general:
        if g['team']=='home':
            hometeam[g.get('name')]=g.get('value')
        if g['team']=='away':
            awayteam[g.get('name')]=g.get('value')
    # print(hometeam,awayteam)
    teamdic={'Home Team':hometeam,
             'Away Team':awayteam}
    return teamdic

def get_stats(pagesource):
    team1 = X = team2 =team2_odd=X_odd=team1_odd= match_status=live_time="Null"
    percentage=0
    data_stat={}
    soup = BeautifulSoup(pagesource, 'lxml')
    div_per = soup.find('div', 'sc-64393ae8-4 bPzuQv')
    win={}
    if div_per:
        divs = div_per.findAll('div')

        for d in divs:
            if d.get('value') == '1':
                team1 = d.text.strip()
            if d.get('value') == 'X':
                X = d.text.strip()
            if d.get('value') == '2':
                team2 = d.text.strip()
        win['Team1']=team1
        win['X']=X
        win['Team2']=team2
    data_stat['Who Will Win']=win
    # print(data_stat)
    odd={}
    odds_div = soup.findAll('div', 'sc-cd4cfbdc-0 sc-4a56d48a-0 hDkGff GZvSp')
    if odds_div:
        if len(odds_div) == 2:
            odds_list = odds_div[1].findAll('div', attrs={'class': None})
        if len(odds_div) == 1:
            odds_list = odds_div[0].findAll('div', attrs={'class': None})
        if len(odds_list) == 3:
            team1_odd = odds_list[0].find('span', 'value').text.strip()
            X_odd = odds_list[1].find('span', 'value').text.strip()
            team2_odd = odds_list[2].find('span', 'value').text.strip()
            print(team1_odd, X_odd, team2_odd)
        # if len(odds_list) == 2:      Over Under Remaining
    odd['Team1']=team1_odd
    odd['X']=X_odd
    odd['Team2']=team2_odd
    data_stat['Odds']=odd
    ht={}
    ht_bar = soup.find('div', 'sc-be07cdeb-4 gInuNM')
    if ht_bar:
        bars = ht_bar.findAll('div', 'sc-be07cdeb-1')
        percents = []
        for b in bars:
            b_per = b.get('width').replace('%', '')
            results = int(b_per) / 100 * 50
            percents.append(results)
        percent = percents[0] + percents[1]

    else:
        headers = {
            'authority': 'api.sofascore.com',
            'accept': '/',
            'accept-language': 'en-US,en;q=0.9,ur;q=0.8,mt;q=0.7,fr;q=0.6',
            'cache-control': 'no-cache',
            'origin': 'https://www.sofascore.com',
            'pragma': 'no-cache',
            'referer': 'https://www.sofascore.com/',
            'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        }

        response = requests.get('https://api.sofascore.com/api/v1/event/10075437/graph', headers=headers).json()
        gP=response.get('graphPoints')
        if gP:
            minutes=gP[-1].get('minute')
            percent=minutes/90*100
    percentage=int(percent)
    if percentage < 50:
        match_status = 'Half Time Not Crossed'
    if percentage > 50:
        match_status = 'Half Time Crossed'
    if percentage == 50:
        match_status = 'Half Time'
    if percentage == 100:
        match_status = 'Full Time'
    time_div = soup.find('div', 'sc-be07cdeb-6 gfybCp')
    if time_div:
        live_time = time_div.text.strip()
        # print(live_time)
    else:
        timer=soup.find('text','timer')
        if timer:
            live_time=timer.text.strip()
    ht['Match Completed'] = f'{percentage}%'
    ht['Match Status'] = match_status
    ht['Match Spent Time']=live_time
    data_stat['Match Status']=ht
    ol_stats = soup.find('ol', 'sc-a58bdd5d-0 jgkMWk')
    match_detail=[]
    if ol_stats:
        lis = ol_stats.findAll('li')
        for li in lis:
            # if """sc-a58bdd5d-1 bnOkBc""" in li:

            match_detail.append(li.get_text(',', strip=True))
    data_stat['Match Details']=match_detail
    return data_stat

def get_name(data):
    main_tournament = hometeam = home_score = awayteam = awayscore = dt_obj =description= ''
    tour = data.get('tournament')
    if tour:
        main_tournament = tour.get('name')
    home = data.get('homeTeam')
    if home:
        hometeam = home.get('name')
        h_score = data.get('homeScore')
        if h_score:
            home_score = h_score.get('current')
    away = data.get('awayTeam')
    if away:
        awayteam = away.get('name')
        a_score = data.get('awayScore')
        if a_score:
            awayscore = a_score.get('current')
    status = data.get('status')
    if status:
        description=status.get('description')
    timestamp = data.get('startTimestamp')
    if timestamp:
        dt_obj = datetime.fromtimestamp(timestamp).strftime("%d - %m - %y")
    # if str(status) == '6':
    #
    #         dt_obj = (datetime.fromtimestamp(timestamp).strftime("%d - %m - %y,%H:%M:%S"))-(now.strftime("%d - %m - %y,%H:%M:%S"))
    #
    #         print("date:", dt_obj)

    return {'tournament': main_tournament,
                 'homeTeam': hometeam,
                 'homeScore': home_score,
                 'awayTeam': awayteam,
                 'awayScore': awayscore,
                 'date': dt_obj,
                 "match_live_status":description}


def scrape():
    headers = {
        'authority': 'api.sofascore.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'origin': 'https://www.sofascore.com',
        'referer': 'https://www.sofascore.com/',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    }

    response = requests.get('https://api.sofascore.com/api/v1/sport/football/events/live', headers=headers).json()
    events = response.get('events')
    statslist=[]
    for e in events:
        statsdic={}
        match = get_name(e)

        print(e.get('customId'))
        driver.get(f"https://www.sofascore.com/pyunik-yerevan-fk-crvena-zvezda/{e.get('customId')}")
        new_data=get_stats(driver.page_source)
        team_streaks=get_team_streaks(e.get('id'))


        main_data={**match,**new_data}
        h2hreturn=get_h2h(e.get('customId'))
        statsdic['H2H']=h2hreturn
        home = e.get('homeTeam')
        if home:
            hometeam_name = home.get('name')
            # home_details=get_teams_details(hometeam_name,home.get('id'))
            # print(home_details)

        away = e.get('awayTeam')
        if away:
            awayteam = away.get('name')
            # away_details = get_teams_details(awayteam, away.get('id'))
            # print(away_details)

        # print(main_data)
        # time.sleep(6)
        all_data.append(main_data)
print(all_data)

# get_team_streaks()
scrape()
print(all_data)
# get_h2h('Xcdsbdd')
# get_teams_details('abx','291120')
# print(all_data)
driver.close()
