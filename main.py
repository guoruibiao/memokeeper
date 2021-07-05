# coding: utf8
import time
import pyperclip
import pyautogui as pg
import conf.conf as app_conf
from models.writer import write


def run():
    while True:
        # start interval
        time.sleep(app_conf.RUNNING_INTERVAL)

        # listening for
        pos = pg.position()
        # trigger: just let y <= N pixels maybe a better choice
        if pos[0] <= app_conf.COORDINATE_MAX_X and pos[1] <= app_conf.COORDINATE_MAX_Y:
            clip_data = pyperclip.paste()
            if clip_data == "":
                continue

            # todo structure raw data
            write(str(clip_data))

        # done at this round
        print(pos)


if __name__ == "__main__":
    run()
