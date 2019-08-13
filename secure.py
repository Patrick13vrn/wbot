import os


def tg_token():
    token = os.getenv("TG_TOKEN")
    return token


def owm_token():
    token = os.getenv("OWM_TOKEN")
    return token
