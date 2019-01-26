HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
  <title>wsgi app</title>
</head>
<style>
  table {{ border-collapse: collapse; }}
  table, th, td {{ border: 1px solid black; }}
  tr:hover {{ background-color: #f5f5f5; }}
</style>
<body>
  <h1>Hello World !</h1>
  <table>
    <tr>
      <th>environ</th>
      <th>value</th>
    </tr>
    {env_table}
  </table>
</body>
</html>
'''

ROW_TEMPLATE = '<tr><td>{}</td><td>{}</td></tr>'


# 参考:
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview
# https://www.python.org/dev/peps/pep-0333/
# http://werkzeug.pocoo.org/docs/0.14/tutorial/#step-0-a-basic-wsgi-introduction
def wsgi_app(environ, start_response):
    # environ 存放着 http request 数据
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview#Requests
    request_data = environ

    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview#Responses
    # 设置 http response header
    start_response('200 OK', [('Content-Type', 'text/html')])
    # 设置 http response body
    env_table = ''.join(ROW_TEMPLATE.format(k, v)
                        for k, v in request_data.items())
    response_body = HTML_TEMPLATE.format(env_table=env_table)
    response_body_bin = response_body.encode('utf-8')
    return [response_body_bin]


if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('0.0.0.0', 5000, wsgi_app, use_reloader=True, use_debugger=True)
