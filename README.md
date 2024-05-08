# Queen-Ant-Bot
A discord bot made in Python thats for simple moderation / having fun with users | Version 1.1 <3

Known issues:
The bot will fail to start if you dont specify a **channel ID** for the discord auto delete and auto shitpost functions. If you do not wish to use
these features, open a text editor / IDE and remove lines **53 - 59** and lines **61 - 67**

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

# Using the bot

Theres a built in help menu for you to get to know the bot. Its used by typing ```!menu``` in any channel.

Use the ```!menu``` command at any time to bring up the help page, which displays the following:

!deletetrash (deletes messages in the channel its used in, in testing it wipes about 12 hours of messages before being rate limited by discord)

!shitpost (posts a random image or words put in the Quotes text file)

!badwords (mod only, shows a list of bad words the bot knows, can be edited by adding words in the Bad Words text file)

# features
Deletes messages every 3 hours (can be changed) in specific channels you specify. You can add multiple channels to delete by copying the code found in line **53 - 59** and putting it below the other code snippet, just be sure to add the channel ID of the channel you want to delete or the bot will fail to start. You can change the time by editing line **53**, you can change it to minutes by changing the word (hours) and edit the timing by changing the number (3)

Sends a message every 30 minutes (can be changed) in specific channels you specify. You can add and remove quotes the bot says by opening the Quotes file. You can also make the bot say things in
other channels manually by using ```!shitpost``` or copying lines **61 - 67** and putting it below the other code snippet, just be sure to add the channel ID for the channel you want it to send the messages to or the bot will fail to start. You can change the time by editing line **61**, you can change it to hourss by changing the word (minutes) and edit the timing by changing the number (30)

When a user says a bad word in any channel the bot will respond to the user by pinging them and yelling at them. Im working on a feature right now that you can toggle that turns on and off auto message delete as well. What the bot says in this situation can be changed by editing line **124**. You can always check what words will raise this situation by using the ```!badwords``` command. Note that only moderators can use this command.

# Future Changes
add more shitposts that get sent in chat

make the bot join vc and say things (i have no idea how im gonna do this)

auto delete bad messages

greet users when they join

Anything else my brain didnt think of rn that ill add here later
