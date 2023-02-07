import socketserver
import threading
import socket

HOST = socket.gethostbyname(socket.gethostname())  # 본인 ip로 서버 주소 할당
PORT = 3000
lock = threading.Lock()  # 동기화 진행 관련 스레드 생성


class UserManager:  # 사용자 관련 이벤트 클래스
    def __init__(self):
        self.users = {}

    def addUser(self, username, conn, addr):
        if username in self.users:
            conn.send('이미 등록된 사용자입니다\n'.encode())
            return None

        lock.acquire()  # 스레드 동기화 방지를 위한 락 설정
        self.users[username] = (conn, addr)
        lock.release()  # 업데이트 후 락 해제

        self.sendMessageToAll('[%s]님이 입장했습니다.' % username)
        print("현재 대화 참여자 수 [%d]" % len(self.users))

        return username

    def removeUser(self, username):
        if username not in self.users:
            return

        lock.acquire()
        del self.users[username]
        lock.release()

        self.sendMessageToAll('[%s]님이 퇴장했습니다.' % username)
        print("현재 대화 참여자 수 [%d]" % len(self.users))

    def messageHandaler(self, username, msg):
        if msg[0] != '/':
            self.sendMessageToAll('[%s]%s' % (username, msg))
            return
        if msg.strip() == '/quit':
            self.removeUser(username)
            return -1

    def sendMessageToAll(self, msg):
        for conn, addr in self.users.values():
            conn.send(msg.encode())


class MyTcpHandler(socketserver.BaseRequestHandler):  # 사용자 연결 핸들링 클래스
    userman = UserManager()

    def handle(self):
        print('[%s] 연결됨' % self.client_address[0])

        try:
            username = self.registerUsername()
            msg = self.request.recv(1024)
            while msg:
                print(msg.decode())
                if self.userman.messageHandaler(username, msg.decode()) == -1:
                    self.request.close()
                    break
                msg = self.request.recv(1024)
        except Exception as err:
            print(err)

        print('[%s] 접속종료' % self.client_address[0])
        self.userman.removeUser(username)

    def registerUsername(self):
        while True:
            self.request.send('로그인ID:'.encode())
            username = self.request.recv(1024)
            username = username.decode().strip()
            if self.userman.addUser(username, self.request, self.client_address):
                return username

class ChatingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def runServer():
    print('채팅 서버를 시작합니다!')
    print('채팅 서버를 끝내려면 Ctrl-C를 누르세요')

    try:
        server = ChatingServer((HOST,PORT), MyTcpHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print('채팅 서버를 종료합니다...')
        server.shutdown()
        server.server_close()

runServer()