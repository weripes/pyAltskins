import time

from selenium.webdriver.common.by import By

from .settings.logger import logger
from .cookies.webdriver_cookie_utils import WebdriverCookieUtils
from .parameters import AltskinsParametersModel
from .steamauth import steam_openid_auth


class PyAltskins:
    '''
    Allows you to use site 'https://table.altskins.com/' using
    python instead of a browser.
    The main purpose is to collect data from the price table of
    items on different exchanges.
    '''
    def __init__(self, driver) -> None:
        self.driver = driver
        self.BASE_URL = 'https://table.altskins.com/'
        logger.debug('Altskins driver initialized')

    @property
    def CookieUtils(self):
        '''
        It is necessary that when changing
        the driver, CookieUtils are also updated
        '''
        return WebdriverCookieUtils(driver=self.driver)

    def is_logged_in(self) -> bool:
        '''
        Returns True if are logged, else False
        '''
        self.driver.get(f'{self.BASE_URL}user/profile')
        if self.driver.find_elements(By.CLASS_NAME, 'site-error'):
            logger.debug('Site error finded -> Not logged in')
            return False

        logger.debug('Site error not finded -> Logged in')
        return True

    def login_via_steam(self, steam_login, steam_password):
        '''
        Allows you to login using Steam on site "https://table.altskins.com/"
        Has 2 required arguments: `steam_login` and `steam_password`
        '''
        if self.is_logged_in():
            logger.error('You are already logged in')
            raise ConnectionAbortedError('You are already logged in')

        self.driver.get(f'{self.BASE_URL}login/steam')
        time.sleep(2)
        steam_openid_auth(
            driver=self.driver,
            steam_login=steam_login, steam_password=steam_password
        )
        if not self.is_logged_in():
            logger.error('Unsuccessfully login via steam')
            raise ConnectionError('Unsuccessfully login via steam')

        assert self.is_logged_in() == True, 'Login via steam failed'
        logger.info('Successfully logged in via steam')

    def login_via_cookies(self, filename: str):
        '''
        Allows you to login using cookies on site "https://table.altskins.com/"
        Has one required argument: `filename` - file with saved cookies
        '''
        self.driver.get('https://table.altskins.com/')
        try:
            self.CookieUtils.load_cookies(filename)
        except FileNotFoundError:
            raise FileNotFoundError(f'Cookie with {filename=} does not exists')
        except Exception as e:
            raise(e)

        assert self.is_logged_in() == True, 'Login via cookies failed'

    def save_cookies(self, filename: str):
        '''
        Allows you to save cookies from site "https://table.altskins.com/"
        Has one required argument: `filename` - name of file where will be saved cookies
        '''
        self.driver.get('https://table.altskins.com/')
        self.CookieUtils.dump_cookies(filename)

    def __format_parameters_to_url_path(self, Parameters: AltskinsParametersModel) -> str:
        parameters_dict = Parameters.dict(exclude={'game_title'})
        logger.debug(f'{parameters_dict=}')
        no_itemsfilter_keys = ['sort', 'page']
        parameters_list = []
        for key, value in parameters_dict.items():
            if key in no_itemsfilter_keys:
                parameters_list.append(f'{key}={value}')
                continue
            parameters_list.append(f'ItemsFilter%5B{key}%5D={value or ""}')
        parameters_list.append('refreshonoff=0')
        logger.debug(f'{parameters_list=}')
        return '?' + '&'.join(parameters_list)

    def parse_items(self, Parameters: AltskinsParametersModel) -> dict:
        '''
        Allows you to parse items by parameters from site "https://table.altskins.com/"
        Has one required argument: `Parameters`, object of type `AltskinsParametersModel`
        with entered parameters
        You must be logged in.
        '''
        assert self.is_logged_in() == True, 'To parse items, you must be logged in'

        logger.info(f'Parse items started ({Parameters.page=})')
        url_parameters = self.__format_parameters_to_url_path(Parameters)
        self.driver.get(f'{self.BASE_URL}site/items{url_parameters}')

        tbody = self.driver.find_element(By.TAG_NAME, 'tbody')
        table_rows = tbody.find_elements(By.TAG_NAME, 'tr')

        items_dict = {}
        for item_id, tr in enumerate(table_rows):
            item_name = tr.find_elements(By.TAG_NAME, 'td')[0].text
            service1_price = tr.find_elements(By.TAG_NAME, 'td')[-4].text
            service2_price = tr.find_elements(By.TAG_NAME, 'td')[-3].text
            service1_to_service2_profit = tr.find_elements(By.TAG_NAME, 'td')[-2].text
            service2_to_service1_profit = tr.find_elements(By.TAG_NAME, 'td')[-1].text
            # For example current page = 1, (1-1)*30 = 0 + item_id(0..29) = keys from 0 to 29
            #     example current page = 2, (2-1)*30 = 30 + item_id(0..29) = keys from 30 to 59
            items_dict.update({(Parameters.page-1)*30 + item_id: {
                'item_name': item_name,
                'service1_price': float(service1_price.split()[0].replace('$', '')),
                'service2_price': float(service2_price.split()[0].replace('$', '')),
                'service1_to_service2_profit': service1_to_service2_profit,
                'service2_to_service1_profit': service2_to_service1_profit
            }})

        return items_dict
