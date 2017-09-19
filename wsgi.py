#!/usr/bin/env python
# encoding: utf-8

from time import time
import logging

import bottle

from sungroup import shuffle_groups, check_result


@bottle.get("/")
@bottle.jinja2_view("index.html")
def get():
    return {}


@bottle.post("/")
@bottle.jinja2_view("index.html")
def post():

    try:
        surfers = bottle.request.forms.surfers
        surfers_list = list(i.strip() for i in surfers.strip().split('\n'))
        n_groups = int(bottle.request.forms.n_groups)
    except ValueError:
        bottle.abort(400)

    surfers_list.sort()

    score = 0

    t0 = time()

    while time() - t0 < 1.0:
        r, s = shuffle_groups(surfers_list, n_groups)
        if s > score:
            result, score = r, s

    try:
        if not check_result(surfers_list, n_groups, result):
            logging.info("bad result: %s")
    except:
        logging.error("bad result: %s", result, exc_info=True)

    return {
        "surfers": surfers,
        "n_groups": n_groups,
        "result": result,
        "score": score,
    }


app = bottle.default_app()
