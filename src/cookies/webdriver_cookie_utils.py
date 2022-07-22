import pickle
import os

from ..settings.logger import logger
from ..settings.base_dir import BASE_DIR


class WebdriverCookieUtils:

    def __init__(self, driver = None) -> None:
        self.driver = driver

    def dump_cookies(self, filename: str) -> None:
        '''
        Saves cookies of the site where the webdriver is located.
        Has one required argument: `filename` - file where will be saved cookies
        '''
        if not os.path.isdir(f'{BASE_DIR}/src/cookies'):
            os.mkdir(f'{BASE_DIR}/src/cookies')

        with open(f'{BASE_DIR}/src/cookies/{filename}.pkl', 'wb') as cookie_file:
            pickle.dump(self.driver.get_cookies(), cookie_file)
            cookie_file.close()
        logger.info(f'Cookies saved to file {filename}.pkl')

    def load_cookies(self, filename: str) -> None:
        '''
        Load cookies into driver.
        Next requests (get, post, ...) will contain cookies
        Has one required argument: `filename` - file with cookies
        '''
        if os.path.isfile(f'{BASE_DIR}/src/cookies/{filename}.pkl'):
            with open(f'{BASE_DIR}/src/cookies/{filename}.pkl', 'rb') as cookie_file:
                cookies = pickle.load(cookie_file)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
            logger.info(f'Cookies loaded (filename={filename}.pkl)')
        else:
            logger.error(f'File {filename}.pkl does not found')
            raise FileNotFoundError(f'File {filename}.pkl does not found')
