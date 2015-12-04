# -*- coding: utf-8 -*-
from __future__ import with_statement
from fabric.api import env, put, run, local, cd, settings, prefix
from fabric.contrib.files import exists

env.hosts = ['root@46.101.135.17']
env.config_local_folder = '/Users/Artfaal/Dropbox/.faceless_config/*'
env.config_remote_folder = '/home/config'
env.path_to_content = '/Users/Artfaal/Яндекс.Диск/CONTENT_EOS_SAUNA/content'
env.path_to_remote_content = '/home/YA/CONTENT_EOS_SAUNA/content'
env.base_dir = '/var/www/faceless'
env.repo = 'https://github.com/artfaal/faceless.git'
env.link_to_xlsx = 'https://docs.google.com/spreadsheets/d/1prsbNgSkrJ4Wm_Z9CHtisbVrsQ_rc3KJ2zEykJxiPSc/export?format=xlsx'
env.full_update = 'secret/nxjQNuiW6E4h8J3z7zJuYJ2KnVnJhs'


def clean_deploy():
    """Полностью чистая установка"""
    send_configs()
    clean_dot_DS(env.path_to_content)
    install_yad()
    install_common()
    install_mongo()
    install_uwsgi_stuff()
    install_nginx()
    install_pillow()
    clone_repo()
    links_configs()
    link_yad_to_content()
    download_xlsx()
    create_socket_for_uwsgi()
    update_venv()
    write_to_base()
    access_right()
    reload_nginx_and_uwsgi()


def send_configs():
    """Отправляем папку с конфигами на сервер"""
    if exists(env.config_remote_folder):
        run('rm -rf %s' % env.config_remote_folder)
    run('mkdir -p %s' % env.config_remote_folder)
    put(env.config_local_folder, env.config_remote_folder)


def clean_dot_DS(path):
    """Очишаем папку от мусора типа DS_Store"""
    local("find %s -name '*.DS_Store' -type f -delete" % path)
    local("dot_clean %s/" % path)


def install_yad():
    """Установка Yandex.Disk"""
    run('echo "deb http://repo.yandex.ru/yandex-disk/deb/ stable \
        main" | sudo tee -a /etc/apt/sources.list.d/yandex.list \
        > /dev/null && \
        wget http://repo.yandex.ru/yandex-disk/YANDEX-DISK-KEY.GPG \
        -O- | sudo apt-key add - && \
        sudo apt-get update && \
        sudo apt-get install -y yandex-disk', quiet=True)
    run('yandex-disk setup')


def install_common(Upgrade=True):
    """Базовая настрока Ubuntu. Обновление пояса и программ"""
    run('sudo apt-get update && \
        sudo /bin/ln -fs /usr/share/zoneinfo/Europe/Moscow /etc/localtime && \
        sudo apt-get install -y language-pack-ru vim curl fabric \
        python-pip python-dev git && \
        sudo pip install virtualenv', quiet=True)
    if Upgrade is True:
        run('sudo apt-get upgrade -y', quiet=True)


def install_mongo():
    """Установка MongoDB и ключей к ней"""
    run('sudo apt-key adv --keyserver \
        hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10 &&\
        echo "deb http://repo.mongodb.org/apt/ubuntu \
        trusty/mongodb-org/3.0 multiverse" | \
        sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list &&\
        apt-get update', quiet=True)
    run('apt-get install -y mongodb-org', quiet=True)
    run('mkdir -p /data/db/')


def install_uwsgi_stuff():
    """Установка uwsgi"""
    #TODO Добавить спец пути для конфигов
    run('sudo apt-get install -y uwsgi uwsgi-plugin-python', quiet=True)


def install_nginx():
    """Установка nginx"""
    #TODO Добавить спец пути для конфигов
    run('sudo apt-get install -y nginx', quiet=True)
    run('rm -rf /etc/nginx/sites-available/ && \
        rm -rf /etc/nginx/sites-enabled/')


def install_pillow():
    """Всякие штуки, что бы Pillow работал нормально"""
    run('apt-get install -y python-dev libjpeg62 libjpeg62-dev \
        zlib1g-dev libfreetype6 libfreetype6-dev', quiet=True)


def clone_repo():
    """Клонируем репозиторий"""
    run('mkdir -p %s' % env.base_dir, quiet=True)
    with cd('%s/..' % env.base_dir):
        run('git clone %s' % env.repo, quiet=True)


def links_configs():
    """Линкуем 3 конфига"""
    main_config = '%s/config.py' % env.config_remote_folder
    nginx_config = '%s/faceless.conf' % env.config_remote_folder
    flask_config = '%s/flask.ini' % env.config_remote_folder
    if exists(main_config) and exists(nginx_config) and exists(flask_config):
        with settings(warn_only=True):
            run('ln -s %s %s' % (main_config, env.base_dir))
            run('ln -s %s %s' % (nginx_config, '/etc/nginx/conf.d/'))
            run('ln -s %s %s' % (flask_config, '/etc/uwsgi/apps-enabled/'))


def link_yad_to_content():
    """Линкуем Yande.Disk с контентом сайта"""

    run('ln -s %s %s/app/static/' % (env.path_to_remote_content, env.base_dir))


def download_xlsx():
    """Скачиваем базу в виде xlsx файла"""
    if not exists('%s/tmp' % env.base_dir):
        run('mkdir -p %s/tmp' % env.base_dir)
    with cd('%s/tmp' % env.base_dir):
        run('curl %s  -o db.xlsx' % env.link_to_xlsx, quiet=True)


def create_socket_for_uwsgi():
    """Создаем файл сокета"""
    run('touch /tmp/faceless.sock')
    run('chown www-data /tmp/faceless.sock')


def update_venv():
    """Настройка окружения"""
    path = '%s/env' % env.base_dir
    if exists(path):
        print 'есть'
        run('rm -rf %s' % path)
    with cd(env.base_dir):
        run('virtualenv env')
        with prefix('source %s/bin/activate' % path):
            run('pip install -r requirements.txt')


def access_right():
    """Назначаем права"""
    run('sudo chown -R www-data:www-data %s' % env.base_dir)


def write_to_base():
    """Обновление базы"""
    run('curl %s/%s' % (env.host, env.full_update))


def reload_nginx_and_uwsgi():
    """Перезапуск Nginx & UWSGI"""
    run('service uwsgi restart && service nginx restart')
