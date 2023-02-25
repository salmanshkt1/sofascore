# Web Scraper for Sofascore

This Python script scrapes data from the sofascore.com website using the requests and BeautifulSoup libraries. It also uses the selenium library to access dynamic content that cannot be accessed using the requests library alone.

## Dependencies
* requests
* BeautifulSoup
* selenium
* webdriver

## Usage

1. Install the required dependencies using pip install -r requirements.txt.
2. Download the chromedriver executable that matches your version of Google Chrome from here and place it in the same directory as the script.
3. Run the script.

## Functions

### get_teams_details(name,team_id)
This function takes two arguments:

name: The name of the team.
team_id: The ID of the team.
It returns a list of team details.

### get_h2h(custom)
This function takes one argument:

custom: The custom ID of the event.
It returns a list of head-to-head events.

### get_team_streaks(match_id)
This function takes one argument:

match_id: The ID of the match.
It returns a dictionary of team streaks.

### get_stats(pagesource)
This function takes one argument:

pagesource: The HTML source code of the page.
It returns a dictionary of statistics.

Disclaimer
This script is for educational purposes only. Use of this script for any other purpose is at your own risk. The author of this script is not responsible for any damages or losses incurred through the use of this script.
