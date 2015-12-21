# -*- coding: utf-8 -*-
from __future__ import with_statement
from fabric.api import env, put, run, cd, lcd, settings, prefix, local
from fabric.contrib.files import exists
import os
env.roledefs['prod'] = ['root@46.101.188.95']
env.roledefs['stage'] = ['root@46.101.209.124']
env.config_local_folder = '~/Dropbox/.faceless_config/*'
env.config_remote_folder = '/home/config'
env.path_to_content = '~/Яндекс.Диск/CONTENT_EOS_SAUNA/content'
env.path_to_remote_content = '/home/YA/CONTENT_EOS_SAUNA/content'
env.base_dir = '/var/www/faceless'
env.repo = 'https://github.com/artfaal/faceless.git'
env.link_to_xlsx = 'https://docs.google.com/spreadsheets/d/1prsbNgSkrJ4Wm_Z9CHtisbVrsQ_rc3KJ2zEykJxiPSc/export?format=xlsx'
env.full_update = 'secret/nxjQNuiW6E4h8J3z7zJuYJ2KnVnJhs'
env.local_base_dir = os.path.abspath(os.path.dirname(__file__))


def clean_deploy():
    """Полностью чистая установка"""
    install_yad()
    send_configs()
    #clean_dot_DS(env.path_to_content)
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
    access_right()
    reload_nginx_and_uwsgi()
    write_to_base()


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
    print "УКАЗАТЬ ПУТЬ ПО УМОЛЧАНИЮ '/home/YA'"
    run('yandex-disk setup')
    print "Добавляем в крон. Если уже есть запись. Запишется ещё одна"
    with settings(warn_only=True):
        backup_cron = run('crontab -l > mycron')
        if backup_cron.return_code == 0:
            run('echo "@reboot yandex-disk start" >> mycron && \
                crontab mycron && rm mycron')
        elif backup_cron.return_code == 1:
            run('echo "@reboot yandex-disk start" >> mycron && \
                crontab mycron && rm mycron')
        else:
            print backup_cron
            raise SystemExit()


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
    flask_config = '%s/flask.ini' % env.config_remote_folder
    # Определяем, куда деплоим nginx и instance конфиги
    if env.host_string in env.roledefs['stage']:
        instance_config = '%s/config_Stage.py' % env.config_remote_folder
        nginx_config = '%s/faceless_Stage.conf' % env.config_remote_folder
    elif env.host_string in env.roledefs['prod']:
        instance_config = '%s/config_Prod.py' % env.config_remote_folder
        nginx_config = '%s/faceless_Prod.conf' % env.config_remote_folder
    else:
        raise ValueError('No valid role specified!')

    if exists(main_config) and exists(nginx_config) and exists(flask_config):
        with settings(warn_only=True):
            run('ln -s %s %s' % (main_config, env.base_dir))
            run('mkdir -p %s/instance' % env.base_dir, quiet=True)
            run('ln -s %s %s/instance/config.py' % (instance_config,
                                                    env.base_dir))
            run('ln -s %s %s' % (nginx_config, '/etc/nginx/conf.d/'))
            run('ln -s %s %s' % (flask_config, '/etc/uwsgi/apps-enabled/'))


def link_yad_to_content():
    """Линкуем Yande.Disk с контентом сайта"""

    run('ln -s %s %s/app/static/' % (env.path_to_remote_content, env.base_dir))


def download_xlsx(l=False):
    """Скачиваем базу в виде xlsx файла (можно локально)"""
    if l is False:
        if not exists('%s/tmp' % env.base_dir):
            run('mkdir -p %s/tmp' % env.base_dir)
        else:
            run('rm -rf %s/tmp/*' % env.base_dir)
        with cd('%s/tmp' % env.base_dir):
            run('curl %s  -o db.xlsx' % env.link_to_xlsx, quiet=True)
        access_right()
    else:
        with lcd('%s/tmp' % env.local_base_dir):
            local('rm -rf %s/tmp/*' % env.local_base_dir)
            local('curl %s  -o db.xlsx' % env.link_to_xlsx)


def create_socket_for_uwsgi():
    """Создаем файл сокета"""
    run('touch /tmp/faceless.sock')
    run('chown www-data /tmp/faceless.sock')


def update_venv(l=False):
    """Настройка окружения (можно локально)"""
    if l is False:
        path = '%s/env' % env.base_dir
        if exists(path):
            run('rm -rf %s' % path)
        with cd(env.base_dir):
            run('virtualenv env')
            with prefix('. %s/bin/activate' % path):
                run('pip install -r requirements.txt', quiet=True)
    else:
        path = '%s/env' % env.local_base_dir
        if os.path.exists(path):
            local('rm -rf %s' % path)
        with lcd(env.local_base_dir):
            local('virtualenv env')
            with prefix('. %s/bin/activate' % path):
                local('pip install -r %s/requirements.txt' % env.local_base_dir)


def access_right():
    """Назначаем права"""
    run('sudo chown -R www-data:www-data %s' % env.base_dir)


def write_to_base(l=False):
    """Обновление базы (можно локально)"""
    if l is False:
        run('curl %s/%s' % (env.host, env.full_update))
        access_right()
    else:
        local('curl localhost:5000/%s' % env.full_update)


def reload_nginx_and_uwsgi():
    """Перезапуск Nginx & UWSGI"""
    run('service uwsgi restart && service nginx restart')


def repo_update():
    """Hard Pull from repo"""
    with cd(env.base_dir):
        run('git fetch --all && git reset --hard origin/master')


def ufw():
    """ Закрываем все порты Firewall, кроме ssh и www"""
    run('apt-get install ufw', quiet=True)
    run('ufw default deny incoming &&\
         ufw default allow outgoing &&\
         ufw allow ssh &&\
         ufw allow http &&\
         ufw allow https &&\
         ufw enable')


def just_update():
    """apt update & upgrade"""
    run('apt-get update && apt-get upgrade -y')
