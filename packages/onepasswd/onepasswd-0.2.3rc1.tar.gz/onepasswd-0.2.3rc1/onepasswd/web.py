from flask import Flask
from flask import render_template
from flask import request, make_response
from onepasswd import crypto
from onepasswd import ltlog
from onepasswd.onepasswd import DB
import time
import datetime
import os
from pathlib import Path

log = ltlog.getLogger('onepasswd.web')

_db_path = ''
_web_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'templates'))
app = Flask("onepasswd", template_folder=_web_path)


def init(cfg):
    global _db_path
    _db_path = cfg['db']


@app.route("/")
def index():
    _db = DB(_db_path)
    items = []
    for entry in _db.getkeys():
        v = _db.get_item(entry)
        items.append(v)
    items = sorted(items, key=lambda v: float(v['time']), reverse=True)
    for i, v in enumerate(items):
        items[i] = {
            'time': str(datetime.datetime.fromtimestamp(int(float(v['time'])))),
            'entry': v['entries'],
            'data': v['passwd']
        }
    return render_template('index.html', items=items)


@app.post("/decrypt")
def decrypt():
    data = request.json['data']
    passwd = request.json['passwd']
    log.debug(request.json)
    try:
        text = crypto.decrypt_passwd(data, passwd)
    except:
        resp = make_response()
        resp.status_code = 500
        return resp
    return {'data': text}
