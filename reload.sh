#! /bin/bash

echo 'Pull'
git pull --all &> /dev/null

echo 'Remove env'
rm -r env

echo 'install virtualenv in system'
sudo pip install virtualenv

echo 'Create virtualenv'
virtualenv env

echo 'Start Virtualenv'
. ./env/bin/activate

echo 'Get from requerements.txt'
pip install -r requirements.txt

echo 'Mongo'
sudo -i pkill mongod

sleep 2

sudo -i mongod --fork --logpath mongo.log
