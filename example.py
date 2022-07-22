import json

from src.settings.webdriver import create_webdriver
from src.settings.logger import logger
from src.parameters import AltskinsParametersModel
from src.altskins import PyAltskins


steam_login = ''
steam_password = ''
chrome_version = None # Ex: 103 (None = latest)

Altskins = PyAltskins(driver=create_webdriver(chrome_version=chrome_version))
# Parse items prices from exchanges dmarket(1) and steamcommunity(2), and sort
# by maximum profit from buying on the first service and selling on the second 
TestParameters = AltskinsParametersModel(
    game_title='csgo',
    service1='dmarket',
    service2='steamcommunity',
    sort='service1_to_service2_profit_desc'
)

try:
    Altskins.login_via_cookies(filename=steam_login)
except Exception as e:
    logger.error(e)
    Altskins.login_via_steam(steam_login=steam_login, steam_password=steam_password)

items = {}
# Parse 5 pages
for i in range(1, 5+1):
    TestParameters.page = i
    items.update(Altskins.parse_items(TestParameters))

Altskins.driver.get('https://table.altskins.com/')
Altskins.CookieUtils.dump_cookies('vip504828')
Altskins.driver.quit()

with open('parsed_items.json', 'w') as result_file:
    json.dump(items, result_file)
    result_file.close()
