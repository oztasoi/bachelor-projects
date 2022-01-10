rm -rf ./messages.txt || (echo "Fast forward cleaning" && exit 1) && touch messages.txt
python3 -m venv venv
source ./venv/bin/activate
pip3 install -r ./requirements.txt
python3 chatter.py
deactivate
rm -rf venv