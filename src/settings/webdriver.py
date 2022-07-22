import undetected_chromedriver as uc

from .logger import logger


USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36'

def create_webdriver(headless: bool = True, chrome_version: int = None) -> None:
    # 5 attempts to create a webdriver (necessary
    # because there may be an error due to the size of the window)
    for _ in range(5):
        try:
            logger.info('Try to create webdriver object...')
            options = uc.ChromeOptions()
            options.add_argument('-start-maximized')
            options.add_argument('--mute-audio')
            options.add_argument(f'--user-agent={USER_AGENT}')
            driver = uc.Chrome(options=options, headless=headless, version_main=chrome_version)
            driver.set_window_size(1920, 1080)

            return driver

        except Exception as e:
            logger.info('Unsuccessfully create webdriver')
            if e == KeyboardInterrupt:
                exit()
            try:
                driver.quit()
            except:
                pass
