#! /bin/bash

echo 'Pull all from repo'
git pull --all &> /dev/null

echo 'remove env'
rm -r env

echo 'create virtualenv'
virtualenv env

echo 'Start Virtualenv'
. ./env/bin/activate

echo 'Get from requerements.txt'
pip install -r requirements.txt

echo 'If run mongo - close'
sudo -i pkill mongod

sleep 2

echo 'Start mongod instanse'
sudo -i mongod --fork --logpath mongo.log
