#!/usr/bin/env python
# coding: utf-8

# In this case we get data from site HowLongToBeat with time, that was spent by user's walkthrough.
# For every page we create an object of class 'Page', using library BeautifulSoup we are find and get all needed
# information and add it to dataframe. If values are missed, data will be filled as NaN.

import urllib3
import re
from bs4 import BeautifulSoup
import time
import numpy as np
import pandas as pd

http = urllib3.PoolManager()
urllib3.disable_warnings()

# Set interval between requests to site
request_interval = 3

# Check existence of page with game
def is_exist(url):
    request = http.request('GET', url)
    request_data = str(request.data)
    if request.status == 200 and (request_data.find("img/404/pong")) < 0:
        return True
    else:
        return False


class Page:
    def __init__(self, url=''):
        self.url = url
        self.content = self.getPage()
        self.soup = BeautifulSoup(self.content, 'lxml')

        self.title = self.getTitle()
        self.developer = self.getDeveloper()
        self.description = self.getDescription()
        self.publisher = self.getPublisher()
        self.genres = self.getGenres()
        self.playable = self.getPlayable()

        self.na_release = self.getNaRelease()
        self.eu_release = self.getEuRelease()
        self.jp_release = self.getJpRelease()

        self.getMainStory()
        self.getMainExtras()
        self.getCompletionists()
        self.getAllPlaystyles()
        self.getAnySpeedrun()
        self.getFullSpeedrun()
        self.getCoop()
        self.getCompetitive()

    def getPage(self):
        page = http.request('GET', self.url)
        return page.data

    def getDescription(self):
        div = self.soup.find_all("div", "in back_primary shadow_box")[2]
        if div.find("p") is not None:
            div = div.find("p")
            description = div.get_text().strip()
            return description
        else:
            return None

    def getTitle(self):
        div = self.soup.find("div", class_="profile_header shadow_text")
        if div is not None:
            title = div.get_text().strip()
            return title
        else:
            return None

    def getDeveloper(self):
        div = self.soup.find("strong", text=re.compile("Developer"))
        if div is not None:
            developer = div.next_sibling.strip()
            return developer
        else:
            return None

    def getPublisher(self):
        div = self.soup.find("strong", text=re.compile("Publisher"))
        if div is not None:
            publisher = div.next_sibling.strip()
            return publisher
        else:
            return None

    def getGenres(self):
        div = self.soup.find("strong", text=re.compile("Genres"))
        if div is not None:
            genres = div.next_sibling.strip()
            return genres
        else:
            return None

    def getPlayable(self):
        div = self.soup.find("strong", text=re.compile("Playable On"))
        if div is not None:
            playable = div.next_sibling.strip()
            return playable
        else:
            return None

    def getNaRelease(self):
        div = self.soup.find("strong", text=re.compile("NA"))
        if div is not None:
            na_release = div.next_sibling.strip()
            return na_release
        else:
            return None

    def getEuRelease(self):
        div = self.soup.find("strong", text=re.compile("EU"))
        if div is not None:
            eu_release = div.next_sibling.strip()
            return eu_release
        else:
            return None

    def getJpRelease(self):
        div = self.soup.find("strong", text=re.compile("JP"))
        if div is not None:
            jp_release = div.next_sibling.strip()
            return jp_release
        else:
            return None

    def getMainStory(self):
        div = self.soup.find('td', text=re.compile("Main Story"))
        if div is not None:
            div = div.next_sibling.next_sibling
            self.mainstorypolled = div.get_text()
            div = div.next_sibling.next_sibling
            self.mainstoryaverage = div.get_text()
            div = div.next_sibling.next_sibling
            self.mainstorymedian = div.get_text()
            div = div.next_sibling.next_sibling
            self.mainstoryrushed = div.get_text()
            div = div.next_sibling.next_sibling
            self.mainstoryleisure = div.get_text()
        else:
            self.mainstorypolled = None
            self.mainstoryaverage = None
            self.mainstorymedian = None
            self.mainstoryrushed = None
            self.mainstoryleisure = None

    def getMainExtras(self):
        div = self.soup.find('td', text="Main + Extras")
        if div is not None:
            div = div.next_sibling.next_sibling
            self.mainextraspolled = div.get_text()
            div = div.next_sibling.next_sibling
            self.mainextrasaverage = div.get_text()
            div = div.next_sibling.next_sibling
            self.mainextrasmedian = div.get_text()
            div = div.next_sibling.next_sibling
            self.mainextrasrushed = div.get_text()
            div = div.next_sibling.next_sibling
            self.mainextrasleisure = div.get_text()
        else:
            self.mainextraspolled = None
            self.mainextrasaverage = None
            self.mainextrasmedian = None
            self.mainextrasrushed = None
            self.mainextrasleisure = None

    def getCompletionists(self):
        div = self.soup.find('td', text="Completionists")
        if div is not None:
            div = div.next_sibling.next_sibling
            self.completionistspolled = div.get_text()
            div = div.next_sibling.next_sibling
            self.completionistsaverage = div.get_text()
            div = div.next_sibling.next_sibling
            self.completionistsmedian = div.get_text()
            div = div.next_sibling.next_sibling
            self.completionistsrushed = div.get_text()
            div = div.next_sibling.next_sibling
            self.completionistsleisure = div.get_text()
        else:
            self.completionistspolled = None
            self.completionistsaverage = None
            self.completionistsmedian = None
            self.completionistsrushed = None
            self.completionistsleisure = None

    def getAllPlaystyles(self):
        div = self.soup.find('td', text="All PlayStyles")
        if div is not None:
            div = div.next_sibling.next_sibling
            self.allplaystylespolled = div.get_text()
            div = div.next_sibling.next_sibling
            self.allplaystylesaverage = div.get_text()
            div = div.next_sibling.next_sibling
            self.allplaystylesmedian = div.get_text()
            div = div.next_sibling.next_sibling
            self.allplaystylesrushed = div.get_text()
            div = div.next_sibling.next_sibling
            self.allplaystylesleisure = div.get_text()
        else:
            self.allplaystylespolled = None
            self.allplaystylesaverage = None
            self.allplaystylesmedian = None
            self.allplaystylesrushed = None
            self.allplaystylesleisure = None

    def getAnySpeedrun(self):
        div = self.soup.find('td', text="Any%")
        if div is not None:
            self.anyspeedrunpolled = div.next_sibling.next_sibling.get_text()
            div = div.next_sibling.next_sibling
            self.anyspeedrunaverage = div.next_sibling.next_sibling.get_text()
            div = div.next_sibling.next_sibling
            self.anyspeedrunmedian = div.next_sibling.next_sibling.get_text()
            div = div.next_sibling.next_sibling
            self.anyspeedrunfastest = div.next_sibling.next_sibling.get_text()
            div = div.next_sibling.next_sibling
            self.anyspeedrunslowest = div.next_sibling.next_sibling.get_text()
        else:
            self.anyspeedrunpolled = None
            self.anyspeedrunaverage = None
            self.anyspeedrunmedian = None
            self.anyspeedrunfastest = None
            self.anyspeedrunslowest = None

    def getFullSpeedrun(self):
        div = self.soup.find('td', class_="center time_40_text")
        self.fullspeedrunpolled = None
        self.fullspeedrunaverage = None
        self.fullspeedrunmedian = None
        self.fullspeedrunfastest = None
        self.fullspeedrunslowest = None

        if div is not None and (div.previous.previous is not None):
            if div.previous.previous == '100%':
                self.fullspeedrunpolled = div.get_text()
                div = div.next_sibling.next_sibling
                self.fullspeedrunaverage = div.get_text()
                div = div.next_sibling.next_sibling
                self.fullspeedrunmedian = div.get_text()
                div = div.next_sibling.next_sibling
                self.fullspeedrunfastest = div.get_text()
                div = div.next_sibling.next_sibling
                self.fullspeedrunslowest = div.get_text()

    def getCoop(self):
        div = self.soup.find("td", text=re.compile("Co-Op"))
        if div is not None:
            div = div.next_sibling
            self.cooppolled = div.get_text()
            div = div.next_sibling.next_sibling
            self.coopaverage = div.get_text()
            div = div.next_sibling.next_sibling
            self.coopmedian = div.get_text()
            div = div.next_sibling.next_sibling
            self.coopleast = div.get_text()
            div = div.next_sibling.next_sibling
            self.coopmost = div.get_text()
        else:
            self.cooppolled = None
            self.coopaverage = None
            self.coopmedian = None
            self.coopleast = None
            self.coopmost = None

    def getCompetitive(self):
        div = self.soup.find('td', text="Competitive")
        if div is not None:
            self.competitivepolled = div.next_sibling.next_sibling.get_text()
            div = div.next_sibling.next_sibling
            self.competitiveaverage = div.next_sibling.next_sibling.get_text()
            div = div.next_sibling.next_sibling
            self.competitivemedian = div.next_sibling.next_sibling.get_text()
            div = div.next_sibling.next_sibling
            self.competitiveleast = div.next_sibling.next_sibling.get_text()
            div = div.next_sibling.next_sibling
            self.competitivemost = div.next_sibling.next_sibling.get_text()
        else:
            self.competitivepolled = None
            self.competitiveaverage = None
            self.competitivemedian = None
            self.competitiveleast = None
            self.competitivemost = None


def main():
    # Create dataframe with all information on game's page
    data = pd.DataFrame(columns=['Url', 'Title', 'Description', 'Developer', 'Publisher', 'Genres', 'Playable On',
                                 'Released in NA', 'Released in EU', 'Released in JP', 'Main Story Polled',
                                 'Main Story Average', 'Main Story Median', 'Main Story Rushed', 'Main Story Leisure',

                                 'Main + Extras Polled', 'Main + Extras Average', 'Main + Extras Median',
                                 'Main + Extras Rushed', 'Main + Extras Leisure',

                                 'Completionists Polled', 'Completionists Average', 'Completionists Median',
                                 'Completionists Rushed', 'Completionists Leisure',

                                 'AllPlayStyles Polled', 'AllPlayStyles Average', 'AllPlayStyles Median',
                                 'AllPlayStyles Rushed', 'AllPlayStyles Leisure',

                                 'Any% Polled', 'Any% Average', 'Any% Median', 'Any% Fastest', 'Any% Slowest',
                                 '100% Polled', '100% Average', '100% Median', '100% Fastest', '100% Slowest',

                                 'Co-Op Polled', 'Co-Op Average', 'Co-Op Median', 'Co-Op Least', 'Co-Op Most',
                                 'Competetive Polled', 'Competetive Average', 'Competetive Median', 'Competetive Least',
                                 'Competetive Most'])

    for index in range(0, 70300):

        # Generate url of game
        url = "https://howlongtobeat.com/game.php?id=" + str(index)

        # Create new row in dataframe with NaN values
        data = data.append(pd.Series([np.nan]), ignore_index=True)
        if is_exist(url):
            a = Page(url)
            data['Url'][index] = url
            data['Title'].loc[index] = a.title
            data['Description'].loc[index] = a.description
            data['Developer'].loc[index] = a.developer
            data['Publisher'].loc[index] = a.publisher
            data['Genres'].loc[index] = a.genres
            data['Playable On'].loc[index] = a.playable
            data['Released in NA'].loc[index] = a.na_release
            data['Released in EU'].loc[index] = a.eu_release
            data['Released in JP'].loc[index] = a.jp_release

            data['Main Story Polled'].loc[index] = a.mainstorypolled
            data['Main Story Average'].loc[index] = a.mainstoryaverage
            data['Main Story Median'].loc[index] = a.mainstorymedian
            data['Main Story Rushed'].loc[index] = a.mainstoryrushed
            data['Main Story Leisure'].loc[index] = a.mainstoryleisure

            data['Main + Extras Polled'].loc[index] = a.mainextraspolled
            data['Main + Extras Average'].loc[index] = a.mainextrasaverage
            data['Main + Extras Median'].loc[index] = a.mainextrasmedian
            data['Main + Extras Rushed'].loc[index] = a.mainextrasrushed
            data['Main + Extras Leisure'].loc[index] = a.mainextrasleisure

            data['Completionists Polled'].loc[index] = a.completionistspolled
            data['Completionists Average'].loc[index] = a.completionistsaverage
            data['Completionists Median'].loc[index] = a.completionistsmedian
            data['Completionists Rushed'].loc[index] = a.completionistsrushed
            data['Completionists Leisure'].loc[index] = a.completionistsleisure

            data['AllPlayStyles Polled'].loc[index] = a.allplaystylespolled
            data['AllPlayStyles Average'].loc[index] = a.allplaystylesaverage
            data['AllPlayStyles Median'].loc[index] = a.allplaystylesmedian
            data['AllPlayStyles Rushed'].loc[index] = a.allplaystylesrushed
            data['AllPlayStyles Leisure'].loc[index] = a.allplaystylesleisure

            data['Any% Polled'].loc[index] = a.anyspeedrunpolled
            data['Any% Average'].loc[index] = a.anyspeedrunaverage
            data['Any% Median'].loc[index] = a.anyspeedrunmedian
            data['Any% Fastest'].loc[index] = a.anyspeedrunfastest
            data['Any% Slowest'].loc[index] = a.anyspeedrunslowest

            data['100% Polled'].loc[index] = a.fullspeedrunpolled
            data['100% Average'].loc[index] = a.fullspeedrunaverage
            data['100% Median'].loc[index] = a.fullspeedrunmedian
            data['100% Fastest'].loc[index] = a.fullspeedrunfastest
            data['100% Slowest'].loc[index] = a.fullspeedrunslowest

            data['Co-Op Polled'].loc[index] = a.cooppolled
            data['Co-Op Average'].loc[index] = a.coopaverage
            data['Co-Op Median'].loc[index] = a.coopmedian
            data['Co-Op Least'].loc[index] = a.coopleast
            data['Co-Op Most'].loc[index] = a.coopmost

            data['Competetive Polled'].loc[index] = a.competitivepolled
            data['Competetive Average'].loc[index] = a.competitiveaverage
            data['Competetive Median'].loc[index] = a.competitivemedian
            data['Competetive Least'].loc[index] = a.competitiveleast
            data['Competetive Most'].loc[index] = a.competitivemost

        time.sleep(request_interval)

        # Write game's data to csv
        data.to_csv('df.csv', mode='w', index=False, sep=';')
        index += 1


if __name__ == '__main__':
    main()