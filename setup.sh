sudo apt -y update
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
sudo apt install python3-venv
python3.6 -m venv venv
source venv/bin/activate
pip install wheel
pip install gunicorn flask