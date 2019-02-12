import base64

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
  <title>wsgi app</title>
  <link rel="icon" href="./1.png" type="image/x-icon">
</head>
<body>
  <h1>Hello World !</h1>
</body>
</html>
'''


# s = '🙈'.encode('utf-8')
# a = base64.b64encode(s)
# print(a)