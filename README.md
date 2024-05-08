# Queen-Ant-Bot
A discord bot made in Python thats for simple moderation / having fun with users

Known issues:
The bot will fail to start if you dont specify a **channel ID** for the discord auto delete and auto shitpost functions. If you do not wish to use
these features, open a text editor / IDE and remove lines **48 - 54** and lines **56 - 62**

# Requirements
discord.py / discord-voice.py (I will be adding voice things in a later build),
pip for discord.py,
and git to download the bot

I run the discord bot on a Ubuntu Server 22.04.4 LTS VM that uses 2 cores and 2GB of RAM and have no issues with performance or runtime issues.
You can host the Discord bot on any operating system you choose, instructions below are for Windows and Linux users.

# Linux
Make sure you have git and python installed on your system before continuing, you can check if you have git and python installed by using ```git --version``` and ```python3 --version``` in Terminal.

If git isnt installed, please use the following commands to install it

Ubuntu/Debian
```sudo apt-get install git```

Arch/Fedora
```sudo pacman -S git```

If pip isnt installed use the following link to install it
https://pip.pypa.io/en/stable/installation/

Install Discord.py / Discord-voice.py using the following commands

```pip install discord.py```
```pip install discord-voice.py```

clone the repository
```git clone https://github.com/swoftii04/Queen-Ant-Bot/main/```

Once it is done downloading, go into the main folder, and then QueenAnt. In there, run QueenAnt.py in the terminal by running ```python3 QueenAnt.py```
# YOU MUST REPLACE THE TOKEN FILE IN THE QUEEN ANT FOLDER WITH YOUR OWN TOKEN OR THE BOT WILL NOT WORK


# Windows
Make sure you have git and python installed on your system before continuing, you can check if you have git and python installed by using ```git --version``` and ```Python --version``` in Command Prompt.

If git and python arent installed, please use the links below to download and follow the instrcutions to install them
https://git-scm.com/download/win https://www.python.org/downloads/ https://pip.pypa.io/en/stable/installation/

Install Discord.py / Discord-voice.py using the following commands

```pip install discord.py```
```pip install discord-voice.py```

clone the repository
```git clone https://github.com/swoftii04/Queen-Ant-Bot/main/```

Once it is done downloading, go into the main folder, and then QueenAnt. In there, run QueenAnt.py in the terminal by running ```Python QueenAnt.py```
# YOU MUST REPLACE THE TOKEN FILE IN THE QUEEN ANT FOLDER WITH YOUR OWN TOKEN OR THE BOT WILL NOT WORK
