#! /bin/bash

echo 'Push all from repo'
git push --all origin #&> /dev/null

echo 'Stop Virtualenv'
deactivate

echo 'Close mongo'
sudo -i pkill mongod
