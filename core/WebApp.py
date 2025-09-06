import flask

app = flask.Flask(__name__, template_folder='../webfile', static_folder='../webfile/static')

@app.errorhandler(500)
def internal_server_error(error):
    # 返回500错误的HTML页面
    return flask.render_template("/error/500.html",error=error)

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route("/testcrash/", methods=["POST"])
def testcrash():
    import traceback
    # 模拟异常
    try:
        raise FileNotFoundError("test crash")
    except FileNotFoundError as e:
        error_stack = traceback.format_exc()
        return flask.render_template("/error/500.html",error=error_stack),500
    return "test crash",500

def AppStart(host: str, port: int):
    """启动Flask应用"""
    app.run(host=host, port=port, debug=True, use_reloader=False)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
