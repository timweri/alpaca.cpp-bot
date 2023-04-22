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

5. Run the desired chat bot

```sh
python3 alpaca_cpp_interface/telegram_bot.py
```

6. Start talking to the chat bot on Telegram.

A few things to note:
- alpaca.cpp can only handle one prompt at a time. If alpaca.cpp is still generating answer for a prompt, `AlpacaCppInterface` will ignore any new prompts
- alpaca.cpp takes quite some time to generate an answer so be patient
- If you are not sure if alpaca.cpp crashed, just query the state using the appropriate chat bot command
- Async is used wherever possible

## Chat platforms

Right now, only Telegram is available out of the box.
`AlpacaCppInterface` and `AlpacaCppPool` make it very easy to expose alpaca.cpp to another chat platform.

`AlpacaCppPool` supports multiple instances of AlpacaCpps. This allows different users to interact with their own instance of AlpacaCpp.

### Telegram

Currently, the Telegram bot implementation only supports one instance of alpaca.cpp.
There are pending changes to allow more alpaca.cpp instances to be spawned.
Since this project is meant to run on a personal computer, some limit would be imposed to make sure not too many instances would spawn.

#### Whitelist

The optional whitelist function helps limit access to your bot by Telegram username.
In the `.env` file, set `TELEGRAM_USERNAME_WHITELIST` to a comma-delimited list of Telegram username to whitelist.
If it's blank, then all usernames are allowed.

When a username is not on the whitelist, the bot will ignore any message from them.

#### Commands
- `/start`: start the alpaca.cpp instance if not already started
- `/restart`: restart the alpaca.cpp instance or start one if none is running
- `/state`: check if alpaca.cpp is running
- `/kill`: kill the alpaca.cpp instance if active
