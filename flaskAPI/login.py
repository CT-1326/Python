import base64

from flask import Flask
from flask import request
from flask import Response
from flask import jsonify

ADMIN_NAME = 'root'
ADMIN_PASSWORD = '12345'

app = Flask(__name__) # flask 앱 인스턴스화


@app.route('/login', methods=['POST'])
def login():
    # 헤더에 로그인 정보를 담아 전송하는만큼 디코딩 진행 및 관련 변수에 초기화
    auth = request.headers.get('Authorization')
    auth = auth.split()[-1]
    auth = base64.b64decode(auth).decode('UTF-8')
    name, password = auth.split(':')

    if name == ADMIN_NAME and password == ADMIN_PASSWORD:
        response = {
            'name': name,
            'message': 'ok'
        }
        return jsonify(response), 200

    return Response('Unauthorized', 401)


if __name__ == '__main__':
    app.run()