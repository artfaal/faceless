#! /bin/bash

echo 'Pull all from repo'
git pull --all &> /dev/null

echo 'Start Virtualenv'
. ./env/bin/activate

echo 'If run mongo - close'
sudo -i pkill mongod

sleep 2

echo 'Start mongod instanse'
sudo -i mongod --fork --logpath mongo.log
