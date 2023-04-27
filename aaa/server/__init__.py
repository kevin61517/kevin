from .core import app
from werkzeug.serving import run_simple


def run():
    """啟動服務"""
    host = '0.0.0.0'
    port = 6666
    run_simple(
        host,
        port,
        app,
        threaded=True,
        use_reloader=True,
        use_debugger=True)
    print('== 測試服務啟動 ==')
    # app.run(host=host, port=port, debug=True)
