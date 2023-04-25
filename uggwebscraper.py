def get_ugg_stats(champName,role):
    from selenium.webdriver.chrome.service import Service
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from webdriver_manager.chrome import ChromeDriverManager
    #service = Service(executable_path="/usr/local/bin/chromedriver")
    #initialize web driver
    service = Service(executable_path=ChromeDriverManager().install())
    fuckerNames = {"chogath":"Cho'Gath", "masteryi":"Master Yi"}
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    #initialize web driver
    with webdriver.Chrome(service=service, options=op) as driver:
        #navigate to the url
        if role == "":
            driver.get("https://u.gg/lol/champions/{}/build".format(champName.lower()))
        else:
            driver.get("https://u.gg/lol/champions/{}/build/{}".format(champName.lower(),role.lower()))
        champList = []
        win_rate = []
        total_matches = []
        all_champ_names = driver.find_elements(By.CLASS_NAME, "champion-name")
        for champ in all_champ_names:
            if champ.text == '' or champ.text == "All Champions": #or champ.text.lower() == champName.lower() 
                continue
            #if champName.lower() in fuckerNames.keys() and champ.text == fuckerNames[champName]:
            #        continue
            champList.append(champ.text)
            #print(champ.text)
        all_shinggo_win_rates = driver.find_elements(By.CLASS_NAME,"win-rate.shinggo-tier")
        for winRate in all_shinggo_win_rates:
            if winRate.text == '' or any(c.isalpha() for c in winRate.text):
                continue
            win_rate.append(winRate.text)
        all_meh_win_rates = driver.find_elements(By.CLASS_NAME,"win-rate.meh-tier")
        for winRate in all_meh_win_rates:
            if winRate.text == '' or any(c.isalpha() for c in winRate.text):
                continue
            win_rate.append(winRate.text)
            #print(winRate.text)
        all_okay_win_rates = driver.find_elements(By.CLASS_NAME,"win-rate.okay-tier")
        for winRate in all_okay_win_rates:
            if winRate.text == '':
                continue
            win_rate.append(winRate.text)
            #print(winRate.text)
        all_good_win_rates = driver.find_elements(By.CLASS_NAME,"win-rate.good-tier")
        for winRate in all_good_win_rates:
            if winRate.text == '':
                continue
            win_rate.append(winRate.text)
        all_great_win_rates = driver.find_elements(By.CLASS_NAME,"win-rate.great-tier")
        for winRate in all_great_win_rates:
            if winRate.text == '':
                continue
            win_rate.append(winRate.text)
        all_volxd_win_rates = driver.find_elements(By.CLASS_NAME,"win-rate.volxd-tier")
        for winRate in all_volxd_win_rates:
            if winRate.text == '':
                continue
            win_rate.append(winRate.text)
        all_matches = driver.find_elements(By.CLASS_NAME,"total-matches")
        for matches in all_matches:
            if matches.text == '':
                continue
            total_matches.append(matches.text)
            #print(matches.text)


    for val in win_rate:
        if any(c.isalpha() for c in val):
            win_rate.remove(val)

    return champList, win_rate, total_matches

if __name__ == "__main__":
    champName = "chogath"
    role = "top"
    champList, win_rate, total_matches = get_ugg_stats(champName,role)

    for i in range(len(champList)):
        print(champList[i])
        print(win_rate[i])
        print(total_matches[i])