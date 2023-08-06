import os
import logging
import time

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

logging.basicConfig(format='%(levelname)s:%(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(os.getenv('LOG_LEVEL', 'INFO'))


class Browser:
    def __init__(self, url):
        self.url = url
        self.browser = None
        self.page = None
        self.content = ""
        self.soup = None
        self.sleep = False

    def create_browser_ice_fox(self, time_sleep=3.0):
        """ Getting the content of the simple web page. """
        with sync_playwright() as p:
            logger.debug('Setup browser')
            self.browser_set_up(p, time_sleep)
            logger.debug('Gathering data from page')
            content = self.page.content()
            logger.debug('Close browser')
            self.close_browser_and_page()
            return content


    def create_browser_totoro(self, clicks, return_latest_content=False, time_sleep=3.0):
        """ Getting the content of the page with clicks which are necessary to get the right data.
        Parameters:
            clicks: dict where key is selector and value is number of click repeats  (0 is while it exist) example:
            clicks={'selector_tag': 1, 'selector_tag_2': 0}
            return_latest_content: if True returns only last page content, default False
            time_sleep: optional, default value 3.0
        """
        with sync_playwright() as p:
            logger.debug('Setup browser')
            self.browser_set_up(p, time_sleep)
            logger.debug('Starting with clicks')
            self.clicks(clicks, return_latest_content)
            logger.debug('Close browser')
            self.close_browser_and_page()
            return self.content

    def create_browser_spiderman(self, filters, clicks=None, return_latest_content=False, time_sleep=3.0,
                                 additional_page=None):
        """" Getting the content of the page with filters and clicks which are necessary to get the right data.
        Parameters:
            filters: list of dicts where the key 'filter_field' represents selector where filter exists and 'type' key
            with value what is going to type in that filter; example filters = [{"filter_field": "selector_tag",
            "type": "Schweiz"}]
            clicks: dict where key is selector and value is number of click repeats  (0 is while it exist) example:
            clicks={'selector_tag': 1, 'selector_tag_2': 0}, default value None
            return_latest_content: if True returns only last page content, default False
            time_sleep: optional, default value 3.0
            additional_page: optional, for collecting content from other page after filter apply
        """
        with sync_playwright() as p:
            logger.debug('Setup browser')
            self.browser_set_up(p, time_sleep)
            logger.debug('Do page filters')
            self.filter_page(filters, time_sleep)
            if clicks:
                logger.debug('Starting with clicks')
                self.clicks(clicks, return_latest_content)
            if additional_page:
                self.url = additional_page
                self.page_goto(0)
                self.content = self.page.content()
            logger.debug('Close browser')
            self.close_browser_and_page()
            return self.content

    def create_browser_the_room(self, date_selector, stop_date, scroll, scroll_sleep=4.0):
        """ Getting the BeautifulSoup content of the page that needs scrolling to load all the data. Scrolling is based
            on the date that the ad is posted on.
        Parameters:
            date_selector: selector for job posting date
            stop_date: date that the scrolling will be stopped on
            scroll: selector for scrolling the page
            scroll_sleep: optional, default value 4.0
        """
        with sync_playwright() as p:
            logger.debug('Setup browser')
            self.browser_set_up(p, 4.0)
            logger.debug('Starting with scrolling')
            while True:
                content = self.page.content()
                soup = BeautifulSoup(content, 'html.parser')
                try:
                    date = soup.select(date_selector)[-1].text.strip()
                    logger.debug(f'Collected date: {date}')
                except Exception as e:
                    logger.error(f'Unable to find date, Exception: {e}')
                    date = None
                if date == stop_date:
                    logger.debug('Scrolling is finished')
                    break
                else:
                    logger.debug('Scrolling continuation')
                    self.page.evaluate(scroll)
                    time.sleep(scroll_sleep)

            return soup

    def create_browser_wakanda(self, click_selector, break_selector, filters=None):
        with sync_playwright() as p:
            logger.debug('Setup browser')
            self.browser_set_up(p, 0)
            if filters:
                logger.debug('Do page filters')
                self.filter_page(filters, 0)
            logger.debug('Starting with clicks')
            while True:
                self.content = self.page.content()
                self.soup = BeautifulSoup(self.content, 'html.parser')
                try:
                    break_value = self.soup.select_one(break_selector)
                    logger.debug(f'Collected break value: {break_value}')
                except Exception as e:
                    logger.error(f'Unable to find break selector: {break_selector}, Exception: {e}')
                    break_value = None

                if break_value:
                    break

                self.click(click_selector)

            logger.debug('Close browser')
            self.close_browser_and_page()
            return self.content

    def browser_set_up(self, p, time_sleep):
        logger.debug("Starting a browser")
        self.browser = p.chromium.launch(headless=True)
        logger.debug("Open incognito mode")
        incognito_browser = self.create_new_context()
        logger.debug("Open new page in incognito browser")
        self.page = incognito_browser.new_page()
        logger.debug(f'Current url: {self.url}')
        logger.debug("Running page goto")
        self.page_goto(time_sleep)

    def page_goto(self, time_sleep):
        logger.debug(f'Page go to url: {self.url}')
        try:
            self.page.goto(self.url, timeout=60 * 10000)
            self.page.wait_for_load_state('domcontentloaded')
            if self.sleep:
                time.sleep(self.sleep)
        except Exception as e:
            logger.error(f' Invalid URL: {self.url} -> Exception: {e}')

    def create_new_context(self):
        incognito_browser = self.browser.new_context(
            ignore_https_errors=True,
            user_agent='jobcloud-kumo'
        )
        return incognito_browser

    def click(self, selector):
        try:
            logger.debug(f'Try to find selector {selector} for the click')
            button = self.page.locator(selector)
            button.wait_for(state="attached", timeout=5000)
            num_of_buttons = button.count()
            logger.debug(f'Number of buttons for click: {num_of_buttons}')
            if num_of_buttons == 1:
                button.click()
            else:
                logger.debug(f'Problem with finding selector: {selector} on page')
                return False
            self.page.wait_for_load_state('domcontentloaded')
            if self.sleep:
                logger.debug(f'Sleep for {self.sleep} seconds')
                time.sleep(self.sleep)
            logger.debug('Page click passed')
            logger.debug('Evaluate a new url')
            new_url = self.page.evaluate('() => window.location.href')
            logger.debug(f'Set new url: {new_url}')
            self.set_current_url(new_url)
        except Exception as e:
            logger.debug('Exception on page click')
            logger.info(f'Page click Exception:{e}')
            return False
        return True

    def clicks(self, clicks, return_latest_content):
        logger.debug(f'Clicks: {clicks}')
        logger.debug(f'Return latest content: {return_latest_content}')
        for selector, repeats in clicks.items():
            logger.debug(f'Click on selector: {selector}')
            logger.debug(f'Number of click repeats: {repeats}')
            for _ in range(repeats):
                logger.debug('Repeats loop')
                self.content += self.page.content()
                logger.debug('Content updated')
                self.click(selector)
                logger.debug('Click on selector passed move on another click or finish')
            if not repeats:
                logger.debug('Infinity loop started')
                click_num = 1
                while True:
                    logger.debug(f'Infinity loop click: {click_num}')
                    self.content += self.page.content()
                    logger.debug('Content updated')
                    page_click = self.click(selector)
                    logger.debug(f'Page click response: {page_click}')
                    if not page_click:
                        logger.debug('Infinity loop break')
                        break
            else:
                logger.debug('Finishing repeats loop with content update')
                self.content += self.page.content()
        if return_latest_content:
            logger.debug('Return content only after last click')
            self.content = self.page.content()
        logger.debug('End of the clicks part')

    def filter_page(self, filters, time_sleep):
        for one_filter in filters:
            filter_type = one_filter.get('type')
            filter_selector = one_filter.get('selector')
            filter_value = one_filter.get('value')
            logger.debug(f'Filter - type: {filter_type}, value: {filter_value}, selector: {filter_selector}')
            if filter_type == 'click':
                logger.debug('Click on filter selector')
                self.click(filter_selector)
            elif filter_type == 'type':
                logger.debug('Type text in filter input field')
                self.page.type(filter_selector, filter_value)
                self.page.wait_for_load_state('domcontentloaded')
            elif filter_type == 'press':
                logger.debug('Press button for filter apply')
                self.page.press(filter_selector, filter_value)
                self.page.wait_for_load_state('domcontentloaded')
            elif filter_type == 'sleep':
                logger.debug(f'Sleep for {filter_value} seconds')
                time.sleep(filter_value)
            elif filter_type == 'select':
                logger.debug('Select option for filter apply')
                self.page.select_option(filter_selector, filter_value)
                self.page.wait_for_load_state('domcontentloaded')
        logger.debug('Filtration passed')

    def close_browser_and_page(self):
        logger.debug('Close browser page')
        self.page.close()
        logger.debug('Close browser instance')
        self.browser.close()
        self.sleep = False

    def set_current_url(self, new_url):
        self.url = new_url

    def get_current_url(self):
        return self.url

    def delete_bs4_obj(self):
        if self.soup:
            del self.soup
