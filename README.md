# The Official Discord Bot for Solar Racing at SBU

### How can I get started?

Anyone can get started, so long as you have some experience with Python (like, basic arrays and functions) and
are ready to accept that some libraries and frameworks can be weird. It's okay to not know the inner workings
of how things work. With a library like the one we will be using here, there is a lot that goes on behind the
scenes that we need to just accept were developed by very talented people. That being said, the library is entirely
open sourced and their support server is very friendly (I've seen it firsthand :)

### Prerequistes

There are a few prerequistes required to begin developing on the discord bot.

1. Install Python at https://www.python.org/downloads/

2. Install VSCode at https://code.visualstudio.com/Download (Or, you may use another IDE of your choice)

3. Install Git at https://git-scm.com/downloads

### Interactions.py

We will be using the Interactions.py library to program the bot. This is actively updated and supports
discords newest slash command feature, as well as other cool features.

The documentation can be found at https://interactions-py.github.io/interactions.py/Guides/01%20Getting%20Started/

If you come into shop hours, we will try our best to explain how it works. If you are an experienced programmer, you will
likely pick it up very fast. If not, you may be intimidated by the way we write functions and access user data. This is okay.
We do not expect talented developers. You may show up to learn. That being said, the way that I personally got started with
developing discord bots is through youtube tutorials. There are a lot of them, but it can be hard to find tutorials about
interactions.py specifically since there are dozens of discord bot libraries.

I'll recommend the following series: https://www.youtube.com/playlist?list=PLnI02ssmcTo3qChwe5_tRyILLqrAExZlo

(this is actually the only series I could find on this exact library but it should suffice. Other libraries follow very
similar convention, but with different syntax and decorators)

come to shop hours ☠️

### Python Virtual Enviroment

It's good practice to use a virtual environment when working on nearly any project. A virtual environment stores your
dependencies in the project folder itself, and makes it easy to update that environment with a single command if any
depencencies are changed, added, or removed. You can think of them like having a virtual machine, but it's not an
entire operating system, it is MUCH MUCH smaller and compact, and it only exist for that specific project. They are very,
very, cool.

In order to setup your own virtual environment, you should clone this repository and access a terminal (either in VScode or
standalone) whos current working directory (cd) is the root of the project folder.

1. Run **"python -m venv myenv"**. This command creates a new virtual environment named "myenv". You should name is "myenv" because
that is the name of the folder that gets ignored in .gitignore. You do not want your virtual environment to be uploaded to github.

**(NOTE):** If you got an error while trying to run that, there are two things you can do. First, "pip install virtualenv" and then
try "virtualenv myenv". If that does not work, contact me or google any errors you have. Warning, I do not recommend changing the
Execution-Policy on your device, as you may find. Although this works, it's probably a no no. Don't ask me. It's just a no no (probably).

2. After that has finished, you should now have a folder named "myenv". To activate it, run **"myenv/Scripts/activate"**. You will now notice
a "(myenv)" in front of your terminal. Congratulations. Anything you run will now run on this virtual environment. That is, libraries you
install will NOT be downloaded to your computer, but rather to this folder. If you delete this folder, you effectively delete the libraries.
Likewise, trying to run the bot when you are not in "(myenv)" mode will warn that the libraries are not installed, because they ONLY
exist on the virtual environment.

3. At this point you have a new clean virtual environment, but nothing has been downloaded. Run **"pip install -r requirements.txt"** to
download all of the dependencies listed in requirements.txt (yes, it's that easy to get started)

4. If you ever want to leave the virtual enviornment, you can run **"deactivate"**. You can also just close the terminal to get out of it.