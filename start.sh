#! /bin/bash

echo 'start virtualenv'
. ./env/bin/activate

echo 'start mongod instanse'
sudo -i pkill mongod
sudo -i mongod --fork --logpath mongo.log
