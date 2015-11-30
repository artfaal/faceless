#!/bin/bash

source "/Users/Artfaal/Dropbox/.faceless_config/VARIABLES"


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

echo 'Пулим'
cd $path_to_project
git pull > /dev/null

echo "Качаем базу в виде xlsx"
mkdir $path_to_project/tmp/
cd $path_to_project/tmp/
rm -r *
curl $link_to_xlsx -o db.xlsx > /dev/null

echo 'Рестартуем сервис'
service uwsgi restart > /dev/null

echo "Назначаем права"
sudo chown -R www-data:www-data $path_to_project
sudo chmod -R 777 $path_to_project/tmp/

exit
EOF

echo "Удаленно пишем базу"
curl $ip_of_the_server/$full_update_db