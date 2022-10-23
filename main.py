import logging
from collections import defaultdict
from datetime import datetime
from typing import Optional, List
import threading

from fastapi import FastAPI
from pydantic import parse_obj_as
from tinydb import TinyDB

from constants import LogSeverityEnum
from logging_service import log_data
from pydantic_schemas import TagIncrementPydantic, TagStatisticsDict, LogPydantic
from db import db_service

from subprocess import Popen, PIPE

import os, time

from playwright.sync_api import Page, sync_playwright, Playwright


app = FastAPI()

logging.basicConfig(level=logging.INFO)
logging.debug(f'Starting........')


EMAIL = "brdhunga+wew@gmail.com"
PASSWORD = os.environ['PASSWORD']
PRODUCTION = not os.environ.get('DEBUG', "") in ['True', 'TRUE']


def check_button_clicked(page: Page) -> None:
    """"""
    btn = page.get_by_test_id('primary-button')
    if "Book for 1 credit" in btn.inner_html():
        logging.info("Already booked")
    elif "Book for 0 credit" in btn.inner_html():
        logging.info("Booking now....")
        btn.click()
    else:
        raise Exception(f"the button did not work: {str(btn.inner_html())}")


def run(playwright: Playwright):
    """"""
    browser = playwright.chromium.launch(headless=PRODUCTION)
    context = browser.new_context()

    page = context.new_page()
    page.goto('https://members.wework.com/desks')
    page.get_by_text('Log in').wait_for()

    email_field = page.locator('id=1-email')
    email_field.fill(EMAIL)
    assert page.locator('id=1-email').input_value() == EMAIL  # .input_value() to get content

    password_field = page.locator('id=1-password')
    password_field.fill(PASSWORD)

    login_button = page.locator('id=1-submit')
    login_button.click()

    page.get_by_test_id("cta-book-now").click()

    for i in range(5):
        time.sleep(3)
        check_button_clicked(page)


@app.get("/")
def root():
    return {"message": "Hello World"}


def long_function():
    """"""
    logging.info("Starting playwright now...")
    with sync_playwright() as play:
        play: Playwright
        run(play)


@app.get("/bg")
def bg():
    t = threading.Thread(target=long_function,
                            args=[],
                            kwargs={})
    t.setDaemon(True)
    t.start()
    return {"message": "Success"}


@app.get('/sp')
def sub_process():
    process = Popen(['playwright', 'install'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    return {"out": str(stdout), "error": str(stderr)}

    

