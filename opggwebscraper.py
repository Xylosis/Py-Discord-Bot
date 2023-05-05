def get_opgg_stats(summonerName):
    from selenium.webdriver.chrome.service import Service
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from webdriver_manager.chrome import ChromeDriverManager
    #service = Service(executable_path="/usr/local/bin/chromedriver")
    #initialize web driver
    service = Service(executable_path=ChromeDriverManager().install())
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    #initialize web driver
    
    with webdriver.Chrome(service=service, options=op) as driver:
        #navigate to the url
        lst = []
        driver.get("https://www.op.gg/summoners/na/{}/ingame".format(summonerName.lower()))
        #counter = 0
        #while counter < 1000000:
        #    counter += 1
        driver.implicitly_wait(5)
        summoner_Names = driver.find_elements(By.CLASS_NAME,"summoner-name")
        for name in summoner_Names:
            lst.append(name.text)
        lst.pop(0)

        for name in lst:
            if summonerName.lower() == name.lower():
                lst.remove(name)

        return lst



if __name__ == "__main__":
    username = "shogolol"
    #lst = get_opgg_stats("Vía")
    # lst = get_opgg_stats("Kasutanink")
    lst = get_opgg_stats(username)

    

    print(lst)