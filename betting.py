from bs4 import BeautifulSoup as BS
from selenium import webdriver as WD
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import os

class Bot:

    def __init__(self, isRunning=True):
        self.isRunning = isRunning

    def isUpdated(self, firstCrashValues, crashValues):
        return firstCrashValues != crashValues

    def stopBot(self):
        self.isRunning = False

    # Find the first win/loss status here
    def runBot(self, desiredStreak):
        ''' This Function Automatically Place Bets Based On Loss Streak, Only Works For Stake Crash '''

        cwd = os.path.dirname(os.path.abspath(__file__))

        # Set up options and URL
        url = 'https://stake.com/casino/games/crash/automated'
        PATH = cwd + '\\chromedriver.exe'

        options = WD.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        # Load URL here
        driver = WD.Chrome(options=options, executable_path=PATH)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.get(url)

        # Wait for website to load and log in
        time.sleep(60)
        
        print("URL Loaded")
        
        loseStreak = 0
        betStreak = 0
        # Set field variables
        # autoButton = driver.find_element_by_css_selector('button.dEISFa:nth-child(2)')
        # betAmountField = driver.find_element_by_css_selector('#betAmount')
        # cashoutField = driver.find_element_by_css_selector('.GridRow-wniw1g-0 > label:nth-child(1) > span:nth-child(1) > span:nth-child(1) > input:nth-child(1)')

        # Check to see if it's still the same value
        global crashesList
        global latestCrashValue
        latestCrashValue = 5.00 #Random value
        crashesList = []
        cancelBet = False
        
        while self.isRunning:
            print('Current Lose Streak', loseStreak)
            roobet = driver.page_source
            soup = BS(roobet, features='html5lib')
        
            # First wave
            findFirstStatus = soup.find('div', {'class' : 'PastBets-sc-6jzeex-0 Aiaif'})
            firstCrashes = findFirstStatus.findChildren('a')
            firstCrashesList = [i.text for i in firstCrashes]
            latestCrash = firstCrashes[1].text[0:-1]
            # Remove all commas in thousands
            if ',' in latestCrash:
                latestCrash = latestCrash.replace(',', '')

            latestCrashValue = float(latestCrash)
            

            # print(firstCrashesList, crashesList)
            # print(latestCrashValue)

            # Lose condition
            if latestCrashValue < 2.00 and self.isUpdated(firstCrashesList, crashesList):
                # If under 2, increment loss streak
                loseStreak += 1
                print("Lose Streak Incremented")
            elif latestCrashValue >= 2.00:
                loseStreak = 0
        
            # When lose streak is at desired loss
            if loseStreak == desiredStreak and self.isUpdated(firstCrashesList, crashesList):
                try:
                    bet = driver.find_element_by_css_selector('.fbjzSA')
                    bet.click()
                    cancelBet = True
                    time.sleep(1)
                    print("Bet Placed")

                except:
                    print("Click Failed")
                    pass
            
            # Win condition. Once bot detects a win, it will not bet until next desired lose streak.
            if latestCrashValue >= 2.00 and cancelBet == True:
                    try:
                        bet = driver.find_element_by_css_selector('.fbjzSA')
                        bet.click()
                        betStreak += 1
                        cancelBet = False
                        time.sleep(1)
                        print("Bet Cancelled")

                    except:
                        print("Click Failed")
                        pass

            findSecondStatus = soup.find('div', {'class' : 'PastBets-sc-6jzeex-0 Aiaif'})
            crashes = findSecondStatus.findChildren('a')
            crashesList = [i.text for i in crashes]


            time.sleep(0.5)
        
        driver.quit()


