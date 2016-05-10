#! /usr/bin/env python
# vim:sw=4 ts=4 et:
#
# Copyright (c) 2015, 2016 Torchbox Ltd.
# 2015-04-02 ft: created
# 2016-05-10 ft: modified for TS
#

from flask import Flask, make_response
app = Flask(__name__)

import os
from kyotocabinet import DB
import settings

def text_response(text):
    response = make_response(text)
    response.headers['Content-Type'] = 'text/plain;charset=UTF-8'
    return response

@app.route("/")
def main():
    return text_response("Ready.\n")

@app.route("/purge/<domain>/<int:genid>", methods=[ 'POST' ])
def purge(domain, genid):
    db = DB()

    if not db.open(settings.GENID_DATABASE, DB.OWRITER | DB.OCREATE):
        return text_response("Failed to purge: cannot open database.\n")

    set_ok = db.set(domain, genid)
    db.close()

    if not set_ok:
        return text_response("Failed to purge: cannot set genid.\n")
    else:
        return text_response("Purged <%s>\n" % (domain,))
    
if __name__ == "__main__":
    app.run(debug = settings.DEBUG)
