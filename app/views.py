# -*- coding: utf-8 -*-
from app import app
from flask import render_template, send_from_directory, \
    request, redirect, url_for
from models import DB, MailSend, bg_for_index
from app.auth import requires_auth
from forms import FeedbackForm, ServiceRequest

# CONSTANT
db = DB()
cat = db.get_db(app.config['CATEGORY_COLLECTION'])
items = db.get_db(app.config['ITEM_COLLECTION'])
p = db.get_db(app.config['PAGES_COLLECTION'])
n = db.get_db(app.config['NEWS_COLLECTION'])


# Инициализируем классы
mail = MailSend()


#  Функия для вомзможности множественного вызова внутри страницы.
def category():
    return cat.find().sort('position')


def pages():
    return p.find().sort('position')


@app.route('/', methods=['GET'])
@app.route('/index/', methods=['GET'])
def index():
    return render_template('index.html',
                           category=category,
                           pages=pages,
                           bg=bg_for_index)


@app.route('/catalog/', methods=['GET'])
@app.route('/catalog/<category_slug>', methods=['GET'])
@app.route('/catalog/<category_slug>/<item_slug>', methods=['GET', 'POST'])
def catalog(category_slug=None, item_slug=None):
    #  Получаем значения
    item_page = items.find_one({'slug': item_slug})
    category_page = cat.find_one({'slug': category_slug})

    # Страница продукта?
    if item_page:
        # Form start
        form = FeedbackForm(request.form)
        if request.method == 'POST':
            mail.send_feedback(request.base_url, form.name.data,
                               form.email.data, form.phone.data,
                               form.body.data)

        return render_template('catalog.html',
                               form=form,
                               category=category,
                               category_slug=category_slug,
                               category_page=category_page,
                               item_page=item_page,
                               pages=pages)
    #  Страница категории?
    elif category_page:
        def items_from_child_category(child):
            return items.find({'main_category': category_page['name'],
                               'child_category': child}).sort('position')

        def items_from_main_category():
            return items.find({'main_category':
                               category_page['name']}).sort('position')

        return render_template('catalog.html',
                               category=category,
                               category_slug=category_slug,
                               category_page=category_page,
                               items_from_child_category=
                               items_from_child_category,
                               items_from_main_category=
                               items_from_main_category,
                               pages=pages)
    #  Значит catalog/
    else:
        return render_template('catalog.html',
                               category=category,
                               category_slug=category_slug,
                               category_page=category_page,
                               pages=pages)


@app.route('/pages/<slug>', methods=['GET', 'POST'])
def page(slug):
    page = p.find_one({"slug": slug})
    form = FeedbackForm(request.form)
    service_form = ServiceRequest(request.form)
    if request.method == 'POST' and request.form['feedback'] == 'Default_Send':
        print 'RLLY'
        mail.send_feedback(request.base_url, form.name.data,
                           form.email.data, form.phone.data,
                           form.body.data)
        return redirect(url_for('page', slug=slug))

    elif request.method == 'POST' and request.form['feedback'] == 'Service_Send':
        mail.send_service_query(
            service_form.equipment.data, service_form.name.data,
            service_form.email.data, service_form.phone.data,
            service_form.body.data, service_form.comment.data)
        return redirect(url_for('page', slug=slug))

    return render_template('pages.html',
                           form=form,
                           service_form=service_form,
                           category=category,
                           pages=pages,
                           page=page)


@app.route('/news/', methods=['GET'])
def news_list():
    news = n.find().sort('position', -1)
    return render_template('news_list.html',
                           category=category,
                           pages=pages,
                           news=news)


@app.route('/news/<slug>', methods=['GET', 'POST'])
def news(slug):
    news = n.find_one({"slug": slug})
    form = FeedbackForm(request.form)
    if request.method == 'POST':
        mail.send_feedback(request.base_url, form.name.data,
                           form.email.data, form.phone.data,
                           form.body.data)
    return render_template('news.html',
                           form=form,
                           category=category,
                           pages=pages,
                           news=news)


@app.route('/admin', methods=['GET', 'POST'])
@requires_auth
def admin():
    if request.method == 'POST' and request.form['send'] == 'UPD_IMG_DB':
        print 'test'
    return render_template('admin.html')


@app.route('/test_img', methods=['GET'])
def test_img():
    names = db.get_all_img()
    return render_template('test_img.html',
                           category=category,
                           pages=pages,
                           names=names)


@app.route('/img/<path:filename>')
def img(filename):
    return send_from_directory(app.config['MEDIA_FOLDER'], filename)


@app.route('/doc/<path:filename>')
def doc(filename):
    return send_from_directory(app.config['DOC_FOLDER'], filename)


@app.route('/cache/<path:filename>')
def cache(filename):
    return send_from_directory(app.config['MEDIA_THUMBNAIL_FOLDER'], filename)


@app.errorhandler(404)
def page_not_found_404(e):
    return render_template('404.html', category=category,
                           pages=pages,), 404


@app.errorhandler(502)
def page_not_found_502(e):
    return render_template('502.html'), 502


@app.route('/pages/novosti')
def r_news():
    return redirect(url_for('news_list'))


@app.route('/pages/software_downloads')
def r_soft_d():
    return redirect(app.config['SOFTWARE_URL'])
