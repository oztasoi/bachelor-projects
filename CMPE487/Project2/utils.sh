function dev() {
  python3 $1
}

function deployment() {
  python3 -m venv venv
  source ./venv/bin/activate
  pip3 install -r ./requirements.txt
  python3 $1
  deactivate
  rm -rf ./venv
}