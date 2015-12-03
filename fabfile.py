# -*- coding: utf-8 -*-
from __future__ import with_statement
from fabric.api import env, put, settings, run, local, cd

env.hosts = ['root@46.101.135.17']
# env.user = 'root'
env.config_local_folder = '/Users/Artfaal/Dropbox/.faceless_config/*'
env.config_remote_folder = '/home/config/'
env.path_to_content = '/Users/Artfaal/Яндекс.Диск/CONTENT_EOS_SAUNA/production'


def send_configs():
    """Отправляем папку с конфигами на сервер в папку /tmp/conf/"""
    put(env.config_local_folder, '/tmp/')


def exists(path):
    """Проверяем существование папки"""
    with settings(warn_only=True):
        return run('test -e %s' % path)


def clean_dot_DS(path):
    """Очишаем папку от мусора типа DS_Store"""
    local("find %s -name '*.DS_Store' -type f -delete" % path)
    local("dot_clean %s/" % path)


def mac_send_content():
    clean_dot_DS(env.path_to_content)


def install_yad():
    """Установка Yandex.Disk"""
    run('echo "deb http://repo.yandex.ru/yandex-disk/deb/ stable main" | sudo tee -a /etc/apt/sources.list.d/yandex.list > /dev/null && wget http://repo.yandex.ru/yandex-disk/YANDEX-DISK-KEY.GPG -O- | sudo apt-key add - && sudo apt-get update && sudo apt-get install -y yandex-disk')
    run('yandex-disk setup')


def base_clean_install(Upgrade=True):
    """Базовая настрока Ubuntu. Обновление пояса и программ"""
    # run('sudo apt-get update && \
    #     sudo /bin/ln -fs /usr/share/zoneinfo/Europe/Moscow /etc/localtime && \
    #     sudo apt-get install -y language-pack-ru', quiet=True)
    if Upgrade:
        print 'LOL'
        run('sudo apt-get upgrade -y', quiet=True)


def install_mongo():
    """Установка MongoDB и ключей к ней"""
    run('sudo apt-key adv --keyserver \
        hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10 &&\
        echo "deb http://repo.mongodb.org/apt/ubuntu \
        trusty/mongodb-org/3.0 multiverse" | \
        sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list', quiet=True)
    run('apt-get update, quiet')