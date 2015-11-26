#!/bin/bash

source "/Users/Artfaal/Dropbox/.faceless_config/VARIABLES"

echo "Отправляем конфиги настройки сервера под nginx, uwsgi и config.py проекта"
scp $config_folder/faceless.conf root@$ip_of_the_server:/home/
scp $config_folder/flask.ini root@$ip_of_the_server:/home/
scp $config_folder/config_Prod.py root@$ip_of_the_server:/home/config.py

echo 'Чистим от мусора директорию контента'
cd $share_content_yad
find . -name '*.DS_Store' -type f -delete
dot_clean $share_content_yad/

echo 'Пакуем контент из Яндекс.Диска'
tar -cvf /tmp/content.tar *

echo "Отправляем на удаленный"
scp /tmp/content.tar root@$ip_of_the_server:/home/


echo "Заходим по SSH"
ssh root@$ip_of_the_server << EOF

echo "Ключи для Mongo"
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10 &&\
echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list &&\

echo "Базовая настройка"
sudo apt-get update &&\
sudo apt-get upgrade -y &&\
sudo /bin/ln -fs /usr/share/zoneinfo/Europe/Moscow /etc/localtime &&\
sudo apt-get install -y language-pack-ru python-pip python-dev nginx git mongodb-org uwsgi uwsgi-plugin-python curl &&\
rm -rf /etc/nginx/sites-available/ &&\
rm -rf /etc/nginx/sites-enabled/ &&\
mkdir -p /data/db/ &&\
sudo pip install virtualenv &&\

echo "Для Pillow"
apt-get install -y python-dev libjpeg62 libjpeg62-dev zlib1g-dev libfreetype6 libfreetype6-dev

echo "Клоним репозиторий"
mkdir -p $path_to_project && cd $path_to_project/../
git clone https://github.com/artfaal/faceless.git

echo "Добавляем конфиг"
mv /home/config.py $path_to_project/

echo "Добавляем контент"
mkdir $path_to_project/app/static/content/
tar -xvC $path_to_project/app/static/content/ -f /home/content.tar

echo "Качаем базу в виде xlsx"
mkdir $path_to_project/tmp/ && cd $path_to_project/tmp/
curl $link_to_xlsx -o db.xlsx

echo "Релоадим проект"
cd $path_to_project
. ./reload.sh

echo "Линкуем конфиги"
sudo ln -s /home/faceless.conf /etc/nginx/conf.d/faceless.conf
sudo ln -s /home/flask.ini /etc/uwsgi/apps-enabled/flask.ini

echo "Создаем файл сокета"
touch /tmp/faceless.sock
sudo chown www-data /tmp/faceless.sock

echo "Назначаем права"
sudo chown -R www-data:www-data $path_to_project
sudo chmod -R 777 $path_to_project/tmp/

echo "Перезапускаем сервисы"
service uwsgi restart
service nginx restart

echo "Выходим из сессии SSH"
exit
EOF

echo "Удаленно пишем базу"
curl $ip_of_the_server/$xls_to_csv
curl $ip_of_the_server/$rm_cat
curl $ip_of_the_server/$rm_items
curl $ip_of_the_server/$rm_pages
curl $ip_of_the_server/$write_cat
curl $ip_of_the_server/$write_items
curl $ip_of_the_server/$write_pages