import sys
import os
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt import App
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from pyMySQL import connectDB
from slack_sdk import WebClient

app = App(
    token=os.environ.get('TOKEN')
)
appToken = os.environ.get('APPTOKEN')


@app.message("Hello")
def message_world(message, say):
    say(f"World!<@{message['user']}>")


@app.message("help")
def message_world(message, say):
    # print(message)
    blocks = [
        {
            "type": "section",
         			"text": {
                                    "type": "plain_text",
                                				"text": "Hi :wave:, 나는 기본적으로 이런 기능을 지원해요",
                                    "emoji": True
                                }
        },
      		{
            "type": "divider"
        },
      		{
            "type": "section",
         			"text": {
                                    "type": "mrkdwn",
                                				"text": "`사용자 전체 조회` : 전체 사용자 정보를 불러와요"
                                }
        },
      		{
            "type": "section",
         			"text": {
                                    "type": "mrkdwn",
                                				"text": "`사용자 조회` : 원하는 사용자 정보를 불러와요"
                                }
        },
      		{
            "type": "section",
         			"text": {
                                    "type": "mrkdwn",
                                				"text": "`사용자 생성` : 신규 사용자를 등록해요"
                                }
        },
      		{
            "type": "section",
         			"text": {
                                    "type": "mrkdwn",
                                				"text": "`사용자 수정` : 기존의 사용자 정보를 수정해요"
                                }
        },
      		{
            "type": "section",
         			"text": {
                                    "type": "mrkdwn",
                                				"text": "`사용자 삭제` : 원하는 사용자를 삭제해요"
                                }
        }
    ]
    say(blocks=blocks)


@app.message("사용자 전체 조회")
def get_users(say):
    result = connectDB.getUsers()
    # print(result, type(result))
    say(f'{result}')


@app.message("사용자 조회")
def get_message(say):
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
            	"text": "찾고자 하는 사용자 아이디를 입력하세요",
                "emoji": True
            }
        }
    ]
    say(blocks=blocks)


@app.action("get_user")
def get_user(ack, body, say):
    ack()
    # print(body['actions'][0]['value'])
    id = body['actions'][0]['value']
    result = connectDB.getUser(id)
    # print(result, type(result))
    say(f'{result}')


@app.message("사용자 삭제")
def get_message(say):
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


@app.action("del_user")
def del_user(ack, body, say):
    ack()
    # print(body['actions'][0]['value'])
    id = body['actions'][0]['value']
    result = connectDB.delUser(id)
    # print(result, type(result))
    say(f'{result}')


@app.message("사용자 생성")
def get_message(say):
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
            	"text": "사용자를 생성합니다.",
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
            	"text": "사용자 아이디를 작성해주세요",
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
            	"text": "사용자 비밀번호를 작성해주세요",
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
            	"text": "사용자 이메일 주소를 작성해주세요",
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


@app.action("add_user")
def add_user(ack, body, say):
    ack()
    # print(body)
    num = []
    for key in body['state']['values']:
        num.append(key)
    id = body['state']['values'][num[0]]['user_id']['value']
    pw = body['state']['values'][num[1]]['user_pw']['value']
    email = body['state']['values'][num[2]]['user_email']['value']
    # print(id, pw , email)
    result = connectDB.postUser(id, pw, email)
    # print(result, type(result))
    say(f'{result}')


@app.message("사용자 수정")
def get_message(say):
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


@app.action("modify_user")
def add_user(ack, body, say):
    ack()
    # print(body)
    num = []
    for key in body['state']['values']:
        num.append(key)
    # print(num)
    id = body['state']['values'][num[0]]['user_id']['value']
    new_id = body['state']['values'][num[1]]['user_new_id']['value']
    pw = body['state']['values'][num[2]]['user_pw']['value']
    email = body['state']['values'][num[3]]['user_email']['value']
    # print(new_id, pw , email)
    result = connectDB.putUser(id, new_id, pw, email)
    # print(result, type(result))
    say(f'{result}')


@app.message("test")
def change_status_message(message, say):
    user_id = message['user']
    print(user_id)
    user_client = WebClient(token=os.environ["USERTOKEN"])
    user_client.users_profile_set(
        user=user_id,
        profile={
            "status_text": "나는 한다 상태 메시지 변경 테스트를",
            "status_emoji": "🤖",
        }
    )
    say("상태 메시지 변경 완료!")


if __name__ == "__main__":
    SocketModeHandler(app, appToken).start()
