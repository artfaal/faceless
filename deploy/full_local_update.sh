#!/bin/bash

source "/Users/Artfaal/Dropbox/.faceless_config/VARIABLES"


echo 'Чистим от мусора директорию контента'
cd $share_content_yad
find . -name '*.DS_Store' -type f -delete
dot_clean $share_content_yad/

echo 'Синхронизируем папку контента'
rsync -avzu --delete --progress -h --exclude 'thumb' $share_content_yad/ $local_path_to_project/app/static/content/

echo 'Ребутим проект'
cd $local_path_to_project
. ./reload.sh > /dev/null

echo "Качаем локально базу в виде xlsx"
mkdir $local_path_to_project/tmp/
cd $local_path_to_project/tmp/
rm -r *
curl $link_to_xlsx -o db.xlsx > /dev/null

echo 'Запускаем локально'
cd $local_path_to_project
. ./env/bin/activate
sudo -i pkill python
sleep 1
python run.py &
sleep 2

echo "Перезаписываем локальную базу"
curl localhost:5000$xls_to_csv
curl localhost:5000$rm_cat
curl localhost:5000$rm_items
curl localhost:5000$rm_pages
curl localhost:5000$write_cat
curl localhost:5000$write_items
curl localhost:5000$write_pages