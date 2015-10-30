#! /bin/bash

echo 'Pull'
git pull --all &> /dev/null

echo 'Start Virtualenv'
. ./env/bin/activate

echo 'Mongo'
sudo -i pkill mongod

sleep 2

sudo -i mongod --fork --logpath mongo.log
