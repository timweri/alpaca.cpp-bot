# alpaca.cpp-bot
Allow chat bots to interact with local alpaca.cpp instances. You can run alpaca.cpp on your local computer and serve it to Telegram, Discord, ...

To make this happen, alpaca.cpp-bot acts as a middleman, extracting and forwarding alpaca.cpp's output to the Python runtime, and forwarding prompts
from the Python runtime back to alpaca.cpp. alpaca.cpp-bot runs alpaca.cpp as a subprocess, and reads from and writes to the pipes connected to the
stdout and stdin of the alpaca.cpp subprocess.

## Get started

### Requirements

Here are what you need:
- Python 3
- A working executable of alpaca.cpp and a compatible alpaca model. I used https://github.com/rupeshs/alpaca.cpp. Make sure the alpaca.cpp executable doesn't print colors.

### Get alpaca.cpp-bot working

1. First, clone the project

```sh
git clone https://github.com/timweri/alpaca.cpp-bot.git
cd alpaca.cpp-bot
```

2. Then, install the Python dependencies

```sh
pip3 install -r requirements
```

3. Rename `.env.stub` to `.env`

```
mv .env.stub .env
```

4. Fill in `.env`

5. Run

```sh
python3 alpaca_cpp_interface/telegram_bot.py
```

6. Start talking to the chat bot on Telegram
