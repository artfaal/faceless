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
    """Установка
    run('echo "deb http://repo.yandex.ru/yandex-disk/deb/ stable main" | sudo tee -a /etc/apt/sources.list.d/yandex.list > /dev/null && wget http://repo.yandex.ru/yandex-disk/YANDEX-DISK-KEY.GPG -O- | sudo apt-key add - && sudo apt-get update && sudo apt-get install -y yandex-disk')
    run('yandex-disk setup')