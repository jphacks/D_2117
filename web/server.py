from web.database import *

"""サーバの起動"""


def main():
    app.run(host='0.0.0.0', port=7777, debug=True)
