from slack_bolt import App
import os
from dotenv import load_dotenv
load_dotenv()

app = App(
    token=os.environ.get('TOKEN'),
    signing_secret=os.environ.get('SECRET')
)

if __name__ == "__main__":
    app.start(port=int(3000))
