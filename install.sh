sudo apt update
sudo apt install -y python3-dev python3-pip
yes | pip3 install --upgrade pip
yes | pip3 install --upgrade numpy
yes | pip3 install --upgrade pillow
yes | pip3 install --upgrade --no-cache-dir tensorflow
yes | pip3 install --upgrade Flask
pip3 install -e .
