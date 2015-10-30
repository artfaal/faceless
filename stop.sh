#! /bin/bash

echo 'Push'
git push --all origin #&> /dev/null

echo 'Stop Virtualenv'
deactivate

echo 'Close Mongo'
sudo -i pkill mongod
