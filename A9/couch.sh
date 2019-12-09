# install brew
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
# install python 3.7.5
brew install python3
brew upgrade python3
# install a Couchbase instance. Not necessary to just upload messages.
brew cask install couchbase-server-enterprise
# upgrades pip
pip3 install --upgrade pip
# installs markovify, which will generate random sentences
pip3 install markovify
# installs the library necessary for Couchbase
brew install libcouchbase
# installs the Couchbase python SDK
pip3 install couchbase
# pings the computer you want to upload messages to 
ping <IP address> -c 3
# installs and upgrades wget, which will grab text from the web to train markovify
brew install wget
brew upgrade wget
# grab text from the web and renames (-O <renamed files>)
wget https://www.gutenberg.org/files/2591/2591-0.txt -O 1.txt
wget http://www.gutenberg.org/cache/epub/5200/pg5200.txt -O 2.txt
wget https://www.gutenberg.org/files/16/16-0.txt -O 3.txt
wget https://www.gutenberg.org/files/1184/1184-0.txt -O 4.txt
