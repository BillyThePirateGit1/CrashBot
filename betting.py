from bs4 import BeautifulSoup as BS
from selenium import webdriver as WD
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import pickle
import os

class Bot:

    def __init__(self, isRunning=True):
        self.isRunning = isRunning

    def isUpdated(self, firstCrashValues, crashValues):
        return firstCrashValues != crashValues

    def stopBot(self):
        self.isRunning = False

    # Find the first win/loss status here
    def runBot(self, desiredStreak, baseBet=0.05):
        ''' This Function Automatically Place Bets Based On Loss Streak, Only Works For Stake Crash '''

        cwd = os.path.dirname(os.path.abspath(__file__))

        # Set up options and URL
        url = 'https://stake.com/casino/games/crash/'
        PATH = cwd + '\\chromedriver.exe'

        options = WD.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        # Access Cookies
        options.add_argument('user-data-dir=C:\\Users\\'+ os.getenv('username') +'\\AppData\\Local\\Google\\Chrome\\User Data')
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        # Load URL here
        driver = WD.Chrome(options=options, executable_path=PATH)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.get(url)

        # Wait for website to load and log in
        time.sleep(3)
        
        print("URL Loaded")
        
        loseStreak = 0
        winStreak = 0
        refreshCounter = 0

        # Check to see if it's still the same value
        latestCrashValue = 5.00 #Can be anything higher than 2.00
        crashesList = []
        resetBet = False
        betAmount = driver.find_element_by_css_selector('#betAmount')
        betAmount.send_keys(str(baseBet))

        
        while self.isRunning:
            print('Current Lose Streak', loseStreak, 'Current Bet Streak', winStreak, 'Refresh Counter', refreshCounter)
            stake = driver.page_source
            soup = BS(stake, features='html5lib')
        
            # First wave
            findFirstStatus = soup.find('div', {'class' : 'PastBets-sc-6jzeex-0 Aiaif'})
            firstCrashes = findFirstStatus.findChildren('a')
            firstCrashesList = [i.text for i in firstCrashes]
            latestCrash = firstCrashes[1].text[0:-1]
            # Remove all commas in thousands
            if ',' in latestCrash:
                latestCrash = latestCrash.replace(',', '')

            latestCrashValue = float(latestCrash)
            
            # Lose condition
            if latestCrashValue < 2.00 and self.isUpdated(firstCrashesList, crashesList):
                # If under 2, increment loss streak
                loseStreak += 1
                print("Lose Streak Incremented")
            elif latestCrashValue >= 2.00:
                loseStreak = 0
        
            # When lose streak is at desired loss
            if loseStreak >= desiredStreak and self.isUpdated(firstCrashesList, crashesList):
                try:
                    bet = driver.find_element_by_css_selector('.fbjzSA')
                    double = driver.find_element_by_css_selector('button.jrFkgF:nth-child(2)')
                    
                    # Avoid doubling first round
                    if loseStreak > desiredStreak:
                        double.click()
                    time.sleep(0.4)
                    bet.click()
                    resetBet = True
                    print("Bet Placed")

                except:
                    print("Click Failed")
                    pass
            
            # Win condition. Once bot detects a win, it will not bet until next desired lose streak.
            if latestCrashValue >= 2.00 and resetBet == True:
                    try:
                        # Reset the bet amount when win is achieved
                        betAmount.send_keys(str(baseBet))
                        # winStreak += 1
                        print("Bet Resetted")
                        resetBet = False

                    except:
                        print("Click Failed")
                        pass

            findSecondStatus = soup.find('div', {'class' : 'PastBets-sc-6jzeex-0 Aiaif'})
            crashes = findSecondStatus.findChildren('a')
            crashesList = [i.text for i in crashes]


            time.sleep(0.5)
        
        driver.quit()


class Roobet:
    
    def __init__(self, isRunning=True):
        self.isRunning = isRunning

    def isUpdated(self, firstCrashValues, crashValues):
        return firstCrashValues != crashValues

    def stopBot(self):
        self.isRunning = False

    # Find the first win/loss status here
    def runBot(self, desiredStreak, baseBet):
        ''' This Function Automatically Place Bets Based On Loss Streak, Only Works For Roobet Crash '''

        cwd = os.path.dirname(os.path.abspath(__file__))

        # Set up options and URL
        url = 'https://roobet.com/crash'
        PATH = cwd + '\\chromedriver.exe'

        options = WD.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        # Access Cookies
        options.add_argument('user-data-dir=C:\\Users\\'+ os.getenv('username') +'\\AppData\\Local\\Google\\Chrome\\User Data')
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        # Load URL here
        driver = WD.Chrome(options=options, executable_path=PATH)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.get(url)

        # Wait for website to load and log in
        time.sleep(3)
        
        print("URL Loaded")

        betAmount = driver.find_element_by_css_selector('input.MuiInputBase-input:nth-child(2)')
        time.sleep(0.4)
        betAmount.send_keys(Keys.CONTROL + 'a')
        betAmount.send_keys(str(baseBet))

        cashoutField = driver.find_element_by_css_selector('input.MuiFilledInput-input:nth-child(1)')
        time.sleep(0.5)
        cashoutField.send_keys(Keys.CONTROL + 'a')
        time.sleep(0.4)
        cashoutField.send_keys('2')
        
        loseStreak = 0
        betStreak = 0

        # Check to see if it's still the same value
        latestCrashValue = 5.00 #Random value
        crashesList = []
        resetBet = False
        
        while self.isRunning:
            print('Current Lose Streak', loseStreak)
            roobet = driver.page_source
            soup = BS(roobet, features='html5lib')
        
            # First wave
            findFirstStatus = soup.find('div', {'class' : 'jss110'})
            firstCrashes = findFirstStatus.findChildren('div')
            firstCrashesList = [i.text for i in firstCrashes]
            latestCrash = firstCrashes[0].text[0:-1]
            # Remove all commas in thousands
            if ',' in latestCrash:
                latestCrash = latestCrash.replace(',', '')

            latestCrashValue = float(latestCrash)

            # Lose condition
            if latestCrashValue < 2.00 and self.isUpdated(firstCrashesList, crashesList):
                # If under 2, increment loss streak
                loseStreak += 1
                print("Lose Streak Incremented")
            elif latestCrashValue >= 2.00:
                loseStreak = 0
        
            # When lose streak is at desired loss
            if loseStreak >= desiredStreak and self.isUpdated(firstCrashesList, crashesList):
                try:
                    bet = driver.find_element_by_css_selector('button.MuiButton-contained:nth-child(1)')
                    double = driver.find_element_by_css_selector('.jss96 > button:nth-child(2)')
                    
                    # Avoid doubling first round
                    if loseStreak > desiredStreak:
                        double.click()
                    time.sleep(0.4)
                    bet.click()
                    resetBet = True
                    print("Bet Placed")

                except:
                    print("Click Failed")
                    pass
            
            # Win condition. Once bot detects a win, it will not bet until next desired lose streak.
            if latestCrashValue >= 2.00 and resetBet == True:
                    try:
                        # Reset the bet amount when win is achieved
                        betAmount.send_keys(Keys.CONTROL + 'a')
                        betAmount.send_keys(str(baseBet))
                        print("Bet Resetted")
                        resetBet = False

                    except:
                        print("Reset Failed")
                        pass

            findSecondStatus = soup.find('div', {'class' : 'jss110'})
            crashes = findSecondStatus.findChildren('div')
            crashesList = [i.text for i in crashes]


            time.sleep(0.5)
        
        driver.quit()