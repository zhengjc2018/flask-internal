from werkzeug.wrappers import Request, Response

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
  <br>
  <table>
    <tr>
      <th>argument</th>
      <th>value</th>
    </tr>
    {args_table}
  </table>
</body>
</html>
'''

ROW_TEMPLATE = '<tr><td>{}</td><td>{}</td></tr>'


# 参考:
# http://werkzeug.pocoo.org/docs/quickstart/
def wsgi_app(environ, start_response):
    request = Request(environ)

    env_table = ''.join(ROW_TEMPLATE.format(k, v)
                        for k, v in request.environ.items())
    args_table = ''.join(ROW_TEMPLATE.format(k, v)
                         for k, v in request.args.items())
    response_body = HTML_TEMPLATE.format(env_table=env_table,
                                         args_table=args_table)
    response = Response(response_body, mimetype='text/html')
    return response(environ, start_response)


if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('0.0.0.0', 5000, wsgi_app, use_reloader=True, use_debugger=True)
