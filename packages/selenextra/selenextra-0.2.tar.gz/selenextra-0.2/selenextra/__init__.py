from .typer import Typer
from selenium.common.exceptions import TimeoutException
from seleniumwire.request import Request, Response
from typing import Union, Callable, Any
from .patcher import CustomPatcher
from .exceptions import *

import re
import random as rnd
import time
import os
import json
import seleniumwire.undetected_chromedriver as webdriver

ChromeOptions = webdriver.ChromeOptions


class ChromeDriver(webdriver.Chrome):
    def __init__(self, **kwargs) -> None:
        driver_executable_path = kwargs.get('driver_executable_path', None)

        self.can_delete_executable = not driver_executable_path
        self.custom_patcher = CustomPatcher(
            executable_path=driver_executable_path,
            force=kwargs.get('patcher_force_close', False),
            version_main=kwargs.get('version_main', None)
        )

        self.custom_patcher.auto()

        release = self.custom_patcher.fetch_release_number()
        version = release.version[0]

        kwargs['driver_executable_path'] = self.custom_patcher.executable_path

        super().__init__(
            version_main=version,
            **kwargs
        )

    def get_user_agent(self) -> str:
        return self.execute_script('return navigator.userAgent')

    def get_cookie_string(self) -> str:
        cookies = self.get_cookies()
        cookies = [f'{item["name"]}={item["value"]}' for item in cookies]

        return '; '.join(cookies) + ';'

    def get_browser_ip(self) -> str:
        self.get('https://httpbin.org/ip')

        try:
            request = self.wait_for_request('/ip')
            if not request.response.status_code == 200:
                raise RequestException("Request failed with status code: {}".format(
                    request.response.status_code))
        except Exception as e:
            raise RequestException("Failed to retrieve IP: {}".format(str(e)))

        try:
            body = request.response.body.decode('utf-8')
            data = json.loads(body)
        except:
            return None

        return data['origin']

    def process_requests(self, callback: Callable[[Request, Response], Any], timeout: Union[int, float] = 30) -> Any:
        end_time = time.time() + timeout

        while time.time() < end_time:
            for request in self.requests:
                if not request.response:
                    continue

                response = request.response
                result = callback(request, response)

                if not result:
                    continue

                return result

        raise TimeoutException(
            'Request processing timed out after the specified timeout period.')

    def sleep_random_time(self, a: Union[int, float], b: Union[int, float]) -> None:
        time.sleep(round(rnd.uniform(a, b), 1))

    def add_cookie_string(self, cookie_string: str) -> None:
        cookie_regex = re.compile(r"([^=]+)=([^;]+)?;")
        cookies = cookie_regex.findall(cookie_string)

        for cookie in cookies:
            name, value = cookie
            name = name.strip()
            value = value.strip()

            self.add_cookie({'name': name, 'value': value})

        self.sleep_random_time(1, 2.5)
        self.refresh()

    def remove_executable(self) -> None:
        if self.can_delete_executable:
            os.remove(self.custom_patcher.executable_path)

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        super().__exit__(exc_type, exc_val, exc_tb)
        self.remove_executable()

    def __del__(self) -> None:
        super().__del__()
        self.remove_executable()
