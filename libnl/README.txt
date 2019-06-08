libnl feature

In order to use libnl function, scan Access Points(APs), you need to install pyenv (host multiple Python versions) and install Python 3.4 or older.

// Ubuntu
sudo apt install curl git-core gcc make zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev libssl-dev

//Latest version pyenv source
git clone https://github.com/pyenv/pyenv.git $HOME/.pyenv

//copy and paste this pyenv configurations on $HOME/.bashrc
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"

if command -v pyenv 1>/dev/null 2>&1; then
  eval "$(pyenv init -)"
fi

// restart shell
source $HOME/.bashrc

//Now you can use pyenv
//View all available versions
pyenv install -l

//Install Python 3.4.1 (this version works out for me)
pyenv install 3.4.1

//You can see all versions you have installed via
pyenv versions

//Pyenv manages virtual environments via the pyenv-virtualvenv plugin
git clone https://github.com/yyuu/pyenv-virtualenv.git   $HOME/.pyenv/plugins/pyenv-virtualenv
source $HOME/.bashrc

//Create virtual environment
pyenv virtualenv 3.4.1 projectName

//Activate virtual environment
pyenv activate projectName

If you get this message,
pyenv-virtualenv: prompt changing will be removed from future release. configure `export PYENV_VIRTUALENV_DISABLE_PROMPT=1' to simulate the behavior.
Add the line "export PYENV_VIRTUALENV_DISABLE_PROMPT=1" to "$HOME/.bashrc"
And source the file
source $HOME/.bashrc

//Deactivate environment
pyenv deactivate

scanAPs.py is fully functional
python scanAPs.py -n <interface>

If you want to use it with Node REST Server, you have all instructions in initDaemon.py.
