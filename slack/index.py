import os
from flask import Flask, request
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from logger import Logger
logger = Logger()
from dotenv import load_dotenv
load_dotenv()
from connectDB import connect


flask_app = Flask(__name__)


app = App(token=os.environ.get('TOKEN'),
          signing_secret=os.environ.get('SECRET'))
handler = SlackRequestHandler(app)


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


@flask_app.route("/")
def hello():
    # logger.info("%s, %s" %(os.environ.get('TOKEN'), os.environ.get('SECRET')))
    return "Hello World!"


@app.event("message")
def handle_message(event, say):
    # logger.info("%s" %event)
    if event.get("type") == "message" and "text" in event:
        if event.get('text') == "사용자 전체 조회":
            result = connect.get_all_users()
            # logger.info("%s, %s"%(result, type(result)))
            if not result:
                say(f"현재 등록된 사용자가 없습니다.")
            else:
                say(f"사용자 전체 조회 결괍니다 : \n'{result}'")
        elif event.get('text') == "사용자 조회" :
            blocks = [
                {
                    "dispatch_action": True,
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "get_user"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "조회하고자 하는 사용자 아이디를 입력하세요",
                        "emoji": True
                    }
                }
            ]
            say(blocks=blocks)
        elif event.get('text') == "사용자 등록" :
            blocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "사용자를 등록합니다.",
                        "emoji": True
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "user_id"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "등록할 사용자 아이디를 작성해주세요",
                        "emoji": True
                    }
                },
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "user_pw"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "등록할 사용자 비밀번호를 작성해주세요",
                        "emoji": True
                    }
                },
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "user_email"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "등록할 사용자 이메일 주소를 작성해주세요",
                        "emoji": True
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "확인",
                                "emoji": True
                            },
                            "value": "click_me_123",
                            "action_id": "add_user"
                        }
                    ]
                }
            ]
            say(blocks=blocks)
        elif event.get('text') == "사용자 수정":
            blocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "사용자 정보를 수정합니다.",
                        "emoji": True
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "user_id"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "수정하고자 하는 사용자 아이디를 작성해주세요",
                        "emoji": True
                    }
                },
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "user_new_id"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "수정할 아이디를 작성해주세요",
                        "emoji": True
                    }
                },
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "user_pw"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "수정할 비밀번호를 작성해주세요",
                        "emoji": True
                    }
                },
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "user_email"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "수정할 이메일 주소를 작성해주세요",
                        "emoji": True
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "수정",
                                "emoji": True
                            },
                            "value": "click_me_123",
                            "action_id": "modify_user"
                        }
                    ]
                }
            ]
            say(blocks=blocks)
        elif event.get('text') == "사용자 삭제":
            blocks = [
                {
                    "dispatch_action": True,
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "del_user"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "삭제하고자 하는 사용자 아이디를 입력하세요",
                        "emoji": True
                    }
                }
            ]
            say(blocks=blocks)
        elif event.get('text') == "체인지!":
            ack()
            user_id = message['user']
            user_client = WebClient(token=os.environ["USERTOKEN"])
            user_client.users_profile_set(
                user=user_id,
                profile={
                    "status_text": "나는 한다 상태 메시지 변경 테스트를",
                    "status_emoji": "🤖",
                }
            )
            say(f"상태 메시지 변경 완료!")
        else:
            say(f"<@{event.get('user')}>님은 '{event.get('text')}' 라고 말씀하신거군요!")


if __name__ == "__main__":
    flask_app.run(port=int(os.environ.get("PORT", 5000)))


@app.action("get_user")
def getuser(ack, body, say):
    ack()
    id = body['actions'][0]['value']
    if id is None:
        say(f"빈 칸을 채워주세요!")
        return
    result = connect.get_user(id)
    if not result:
        say(f"등록되지 않은 사용자 입니다.")
    else:
        say(f'{result}')


@app.action("add_user")
def add_user(ack, body, say):
    ack()
    num = []
    for key in body['state']['values']:
        num.append(key)
    id = body['state']['values'][num[0]]['user_id']['value']
    pw = body['state']['values'][num[1]]['user_pw']['value']
    email = body['state']['values'][num[2]]['user_email']['value']
    if None not in(id, pw, email):
        data = {'id':id, 'pw':pw, 'email':email}
        result = connect.post_user(data)
        if result is None:
            say(f"이미 등록된 사용자 입니다.")
        else:
            say(f"사용자 등록에 성공했습니다.")
    else:
        say(f"빈 칸을 채워주세요!")


@app.action("modify_user")
def add_user(ack, body, say):
    ack()
    num = []
    for key in body['state']['values']:
        num.append(key)
    id = body['state']['values'][num[0]]['user_id']['value']
    new_id = body['state']['values'][num[1]]['user_new_id']['value']
    pw = body['state']['values'][num[2]]['user_pw']['value']
    email = body['state']['values'][num[3]]['user_email']['value']
    if None not in(id, pw, email):
        data = {'id':new_id, 'pw':pw, 'email':email}
        result = connect.put_user(id, data)
        if result is None:
            say(f"등록되지 않은 사용자 입니다.")
        else:
            say(f"해당 사용자 정보가 수정되었습니다.")
    else:
        say(f"빈 칸을 채워주세요!")


@app.action("del_user")
def del_user(ack, body, say):
    ack()
    id = body['actions'][0]['value']
    if id is None:
        say(f"빈 칸을 채워주세요!")
        return
    result = connect.del_user(id)
    if result is None:
        say(f"등록되지 않은 사용자 입니다.")
    else:
        say(f"해당 사용자는 삭제 되었습니다.")