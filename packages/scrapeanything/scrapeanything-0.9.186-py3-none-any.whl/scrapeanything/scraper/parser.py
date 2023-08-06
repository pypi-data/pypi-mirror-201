from scrapeanything.utils.config import Config
from scrapeanything.utils.utils import Utils
from scrapeanything.scraper.scraper import Scraper

class Parser:

    scraper = None

    def __init__(self, config: Config, user_dir: str=None, headless: bool=True, fullscreen: bool=False, disable_javascript: bool=False, window: dict={}, proxy_address: str=None) -> None:
        self.config = config
        self.scraper = self.get_scraper(config=config, headless=headless, fullscreen=fullscreen, disable_javascript=disable_javascript, window=window, user_dir=user_dir, proxy_address=proxy_address)

    # region methods
    def click(self, path: str, element: any=None, timeout: int=0, pos: int=0, is_error: bool=True) -> any:
        return self.scraper.click(path=path, element=element, timeout=timeout, pos=pos, is_error=is_error)

    def hover(self, path: str, element: any=None, is_error: bool=True, timeout: int=0) -> None:
        self.scraper.hover(path=path, element=element, is_error=is_error, timeout=timeout)

    def click_and_hold(self, path: str, seconds: float, element: any=None, timeout: int=0, is_error: bool=True) -> None:
        return self.scraper.click_and_hold(path=path, element=element, timeout=timeout, seconds=seconds, is_error=is_error)

    def back(self) -> None:
        self.scraper.back()

    def get_current_url(self) -> str:
        return self.scraper.get_current_url()

    def enter_text(self, path: str, text: str, clear: bool=False, element: any=None, timeout: int=0, is_error: bool=True):
        return self.scraper.enter_text(path=path, text=text, clear=clear, element=element, timeout=timeout, is_error=is_error)

    def wget(self, url: str, tries: int=0):
        return self.scraper.wget(url, tries)

    def xPath(self, path: str, element: any=None, pos: int=None, dataType: str=None, prop: str=None, explode=None, condition=None, substring=None, transform=None, replace=None, join=None, timeout=0, is_error: bool=True):
        return self.scraper.xPath(path=path, element=element, pos=pos, dataType=dataType, prop=prop, explode=explode, condition=condition, substring=substring, transform=transform, replace=replace, join=join, timeout=timeout, is_error=is_error)

    def exists(self, path: str, element: any=None, timeout: int=0, is_error: bool=False):
        return self.scraper.exists(path=path, element=element, timeout=timeout, is_error=is_error)

    def get_css(self, element: any, prop: str):
        return self.scraper.get_css(element=self, prop=prop)

    def login(self, username_text: str=None, username: str=None, password_text: str=None, password: str=None, is_error: bool=True) -> None:
        self.scraper.login(username_text, username, password_text, password, is_error=is_error)

    def search(self, path: str=None, text: str=None, timeout: int=0, is_error: bool=True) -> None:
        self.scraper.search(path=path, text=text, timeout=timeout, is_error=is_error)

    def scroll_to_bottom(self) -> None:
        self.scraper.scroll_to_bottom()

    def get_scroll_top(self) -> None:
        return self.scraper.get_scroll_top()

    def get_scroll_bottom(self) -> None:
        return self.scraper.get_scroll_bottom()

    def select(self, path: str, option: str) -> None:
        self.scraper.select(path=path, option=option)

    def get_image_from_canvas(self, path: str, local_path: str, element: any=None) -> str:
        return self.scraper.get_image_from_canvas(path=path, local_path=local_path, element=element)

    def switch_to(self, element: any) -> None:
        self.scraper.switch_to(element=element)

    def screenshot(self, file: str) -> None:
        self.scraper.screenshot(file=file)

    def freeze(self) -> None:
        self.scraper.freeze()

    def unfreeze(self) -> None:
        self.scraper.unfreeze()

    def close(self) -> None:
        self.scraper.close()

    #endregion methods

    def get_scraper(self, config: Config, user_dir: str=None, headless: bool=True, fullscreen: bool=False, disable_javascript: bool=False, window: dict={}, proxy_address: str=None) -> Scraper:
        scraper_type = self.config.get('PROJECT', 'scraper')
        if scraper_type is not None:
            module_name = self.config.get('PROJECT', 'scraper')
            class_name = ''.join([ slug.capitalize() for slug in scraper_type.split('_') ])
        else:
            module_name = 'selenium'
            class_name = 'Selenium'

        return Utils.instantiate(module_name=f'scrapeanything.scraper.scrapers.{module_name}', class_name=class_name, args={ 'headless': headless, 'fullscreen': fullscreen, 'disable_javascript': disable_javascript, 'window': window, 'config': config, 'user_dir': user_dir, 'proxy_address': proxy_address })