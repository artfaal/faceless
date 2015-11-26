#!/bin/bash

source "/Users/Artfaal/Dropbox/.faceless_config/VARIABLES"


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

echo 'Пулим'
cd $path_to_project
git pull

echo 'Рестартуем сервис'
service uwsgi restart

exit
EOF