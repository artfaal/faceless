#!/bin/bash

source "/Users/Artfaal/Dropbox/.faceless_config/VARIABLES"

scp $config_folder/faceless.conf root@$ip_of_the_server:/home/
scp $config_folder/flask.ini root@$ip_of_the_server:/home/
scp $config_folder/config_Prod.py root@$ip_of_the_server:/home/config.py

echo 'Чистим от мусора директорию контента'
cd $share_content_yad
find . -name '*.DS_Store' -type f -delete
dot_clean $share_content_yad/

echo 'Синхронизируем папку контента'
rsync -avzu --delete --progress -h --exclude 'thumb' $share_content_yad/ root@$ip_of_the_server:$path_to_project/app/static/content/

echo 'Пушим с локального компа'
cd $local_path_to_project
git push &> /dev/null

echo "Заходим по SSH"
ssh root@$ip_of_the_server > /dev/null << EOF

echo "Добавляем конфиг"
mv /home/config.py $path_to_project/

cd $path_to_project
. ./reload.sh > /dev/null

echo "Качаем базу в виде xlsx"
mkdir $path_to_project/tmp/ && cd $path_to_project/tmp/ && rm -r *
curl $link_to_xlsx -o db.xlsx > /dev/null

echo "Назначаем права"
sudo chown -R www-data:www-data $path_to_project
sudo chmod -R 777 $path_to_project/tmp/

echo 'Рестартуем сервисы'
service uwsgi restart
service nginx restart

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