# Python file for scraping from songkick.com
# Author: Yiteng Mu(yitengm)
# Purpose: Get the all the concert data in NY for the incoming month, and store the raw data into csv file

import os
import spotipy
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

def refreshData():
    print("Refreshing Data...")
    os.environ["SPOTIPY_CLIENT_ID"] = "0c8d2f75d9c543648ad5050b5edc5aea"
    os.environ["SPOTIPY_CLIENT_SECRET"] = "6d6db241d6b14227a22d7da604a0fc8b"
    spotify = spotipy.Spotify(client_credentials_manager=spotipy.oauth2.SpotifyClientCredentials())

    # ignore this block, because it is the basic setup for web driver
    # open web silently
    driver_exe = './chromedriver'
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(driver_exe, options=options, )


    locationCodes = set()
    driver.get('https://www.songkick.com/search?page=1&per_page=10&query=NY&type=locations')

    # !!Selenium removed find_elements_by_xpath since version >= 4.3.0
    maxPageElement = driver.find_element('xpath', '//div[@class = "pagination"]/a[last() - 1]')
    maxPage = int(maxPageElement.text)
    for page in range(1, maxPage + 1):
        driver.get('https://www.songkick.com/search?page={}&per_page=10&query=NY&type=locations'.format(page))
        currentLocationElements = driver.find_elements(
            'xpath', '//div[@class = "component search event-listings events-summary"]/ul//p[@class = "summary"]/a'
        )
        # Get all the location code of cities in NY state
        for currentLocationElement in currentLocationElements:
            href = currentLocationElement.get_attribute('href')
            currentLocationCode = href.split('/')[-1]
            locationCodes.add(currentLocationCode)

    # !! Processing pagination
    overview = None
    for locationCode in locationCodes:
        #months = ("this-month", "november-2022", "december-2022")
        months = ("this-month",)
        for month in months:
            # Iterate through pages and months:
            driver.get('https://www.songkick.com/metro-areas/{}/{}'.format(locationCode, month))
            try:
                # !!Selenium removed find_elements_by_xpath since version >= 4.3.0
                maxLocationPageElement = driver.find_element('xpath', '//div[@class = "pagination"]/a[last() - 1]')
            except NoSuchElementException:
                # No events at this location
                print(f"No events for month {month} at {locationCode}.")
                continue


            # Otherwise, process the location
            print(f"Starting to process location {locationCode} and month {month}.")
            maxLocationPage = int(maxLocationPageElement.text)

            for locationPage in range(1, maxLocationPage + 1):
                print(f"Starting to process page {locationPage}.")
                driver.get('https://www.songkick.com/metro-areas/{}/{}?page={}'.format(locationCode, month, locationPage))

                # Try songkick.com
                # Scraping data for 50 rows of data
                # Pittsburgh, this month
                #driver.get('https://www.songkick.com/metro-areas/22443-us-pittsburgh/this-month')
                # !!Selenium removed find_elements_by_xpath since version >= 4.3.0
                artistsElements = driver.find_elements('xpath', '//div[@class = "artists-venue-location-wrapper"]/p[@class = "artists"]/a//strong')
                locationsElements = driver.find_elements('xpath', '//div[@class = "artists-venue-location-wrapper"]/p[@class = "location"]')
                artists = []
                locations = []

                # get the info of artists and locations
                for i in range(len(artistsElements)):
                    artists.append(artistsElements[i].text)
                    # !!replaced line breaker with comma, so that it looks pretty in the csv
                    locations.append(locationsElements[i].text.replace('\n', ','))

                print(len(artists))
                print(len(locations))

                dates = []
                links = []

                # get the date and links for the concerts
                if len(artists) == len(locations):
                    for i in range(len(artists)):
                        # !!Selenium removed find_elements_by_xpath since version >= 4.3.0
                        dates.append(artistsElements[i].find_elements('xpath', './/ancestor::li[@class = "event-listings-element"]/time')[0].get_attribute('datetime'))
                        links.append(artistsElements[i].find_elements('xpath', './/ancestor::div[@class = "event-details-wrapper"]/a[@class = "event-link chevron-wrapper"]')[0].get_attribute('href'))
                        # print("{} will hold concert in {} on {}.".format(artists[i].text, locations[i].text, date[0].get_attribute('title')))

                # # 1st part the concert overview
                # overview = pd.DataFrame({'Artists':artists,
                #                          'Locations': locations,
                #                          'Date': dates,
                #                          'href': links})
                #
                # overview.to_csv('overviewRaw.csv')

                # Dig into the links
                # get the details of the artists and concerts
                artistsLinksTemps = []
                ticketLinkElements = []
                venueDetailElements = []
                additionalDetailElements = []
                artistsLinks = []
                venueDetails = []
                additionalDetails = []

                # helper function to aggregate multiple links in artists
                def getLinks(artistLinkElement):
                    # !!Selenium removed find_elements_by_xpath since version >= 4.3.0
                    linkElements = artistLinkElement.find_elements('xpath', ".//*")
                    linkLists = []

                    for linkElement in linkElements:
                        linkLists.append(linkElement.get_attribute('href'))

                    return linkLists

                for i in range(len(artists)):
                    print(links[i])
                    driver.get(links[i])
                    print(i)
                    # artist page links, but may contain multiple names and links, need to use getLinks function!
                    # !!Selenium removed find_elements_by_xpath since version >= 4.3.0
                    artistsLinksTemps.append(driver.find_elements('xpath', '//h1[@class = "h0 summary"]/span'))
                    if(artistsLinksTemps[-1] == []):
                        artistsLinks.append("")
                    else:
                        artistsLinks.append(getLinks(artistsLinksTemps[-1][0]))
                    # url for buying tickets .get_attribute('href'), get 1 link per entity only
                    # !!Selenium removed find_elements_by_xpath since version >= 4.3.0
                    ticketLinkElements.append(driver.find_elements('xpath', '//div[@id = "tickets"]/a[0]'))
                    # url for more info of the venue (e.g. how many upcoming concerts) using [0].text()
                    # !!Selenium removed find_elements_by_xpath since version >= 4.3.0
                    venueDetailElements.append(driver.find_elements('xpath', '//div[@class = "venue-info-details"]'))
                    # additional info for the concerts (price, door open time, etc.) using [0].text()
                    # !!Selenium removed find_elements_by_xpath since version >= 4.3.0
                    additionalDetailElements.append(driver.find_elements('xpath', '//div[@class = "additional-details-container"]'))
                    if(venueDetailElements[i] == []):
                        venueDetails.append("")
                    else:
                        venueDetails.append(venueDetailElements[i][0].text.replace('\n', ','))
                    if(additionalDetailElements[i] == []):
                        additionalDetails.append("")
                    else:
                        additionalDetails.append(additionalDetailElements[i][0].text.replace('\n', ','))

                def getGenres(row):
                    try:
                        result = spotify.search(q='artist:' + row['Artists'], type='artist')
                        return result['artists']['items'][0]['genres']
                    except Exception:
                        return []

                # !! Append to existing dataframe if any
                if overview is None:
                    # 1st part the concert overview
                    overview = pd.DataFrame({'Artists':artists,
                                            'Artists Link': artistsLinks,
                                            'Locations': locations,
                                            'Venue Details': venueDetails,
                                            'Date': dates,
                                            'href': links,
                                            'Additonal Info': additionalDetails})
                    overview['Artists Genres'] = overview.apply(
                        getGenres,
                        axis=1,
                    )
                    # !!Checkpoints
                    overview.to_csv('overviewRaw_{}_{}_{}.csv'.format(locationCode, month, locationPage))
                else:
                    df = pd.DataFrame({'Artists':artists,
                                       'Artists Link': artistsLinks,
                                       'Locations': locations,
                                       'Venue Details': venueDetails,
                                       'Date': dates,
                                       'href': links,
                                       'Additonal Info': additionalDetails})
                    df['Artists Genres'] = df.apply(
                        getGenres,
                        axis=1,
                    )
                    overview = overview.append(
                        df,
                        ignore_index=True,
                    )
                    # !!Checkpoints
                    # overview.to_csv('overviewRaw_{}_{}_{}.csv'.format(locationCode, month, locationPage))
    overview.to_csv('overviewRaw.csv')









# html = urlopen("https://www.songkick.com/metro-areas/22443-us-pittsburgh/this-month")
#
# conRow = BeautifulSoup(html, 'lxml')
#
# fout = open('conRaw.txt', 'wt', encoding='utf-8')
#
# fout.write(str(conRow))
#
# fout.close()
#
# tableList = conRow.findAll('li')
# print("there are", len(tableList), "list")
#
# print(tableList[0])
