#!/bin/bash

source "/Users/Artfaal/Dropbox/.faceless_config/VARIABLES"

scp $config_folder/faceless.conf root@$ip_of_the_server:/home/
scp $config_folder/flask.ini root@$ip_of_the_server:/home/
scp $config_folder/config_Prod.py root@$ip_of_the_server:/home/config.py

echo 'Чистим от мусора директорию контента'
cd $share_content_yad
find . -name '*.DS_Store' -type f -delete
dot_clean ../faceless/
echo 'Синхронизируем папку контента'
rsync -avzu --delete --progress -h $share_content_yad/ root@$ip_of_the_server:$path_to_project/

echo 'Пушим с локального компа'
cd $local_path_to_project
git push

echo "Заходим по SSH"
ssh root@$ip_of_the_server << EOF

echo "Добавляем конфиг"
mv /home/config.py $path_to_project/

cd $path_to_project
. ./reload.sh

echo 'Рестартуем сервисы'
service uwsgi restart
service nginx restart

exit
EOF