# -*- coding: utf-8 -*-
from app import app
from flask import render_template, send_from_directory, \
    request, redirect, url_for, flash, make_response
from models import DB, MailSend, bg_for_index
from app.auth import requires_auth
from forms import FeedbackForm, ServiceRequest, BuildRequest, SendByPostMail, Empty
from app.evil import secret
import datetime
from app import recaptcha

# CONSTANT
db = DB()
cat = db.get_db(app.config['CATEGORY_COLLECTION'])
items = db.get_db(app.config['ITEM_COLLECTION'])
p = db.get_db(app.config['PAGES_COLLECTION'])
n = db.get_db(app.config['NEWS_COLLECTION'])
i_n = db.get_db(app.config['INDEX_NEWS_COLLECTION'])
i_s = db.get_db(app.config['INDEX_SLIDER_COLLECTION'])
d = db.get_db(app.config['DEALERS_COLLECTION'])


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
    i_news = i_n.find().sort('position', -1)
    i_slider = i_s.find().sort('position')
    list_best = []
    for i in i_slider:
        list_best.append(i['name'])
    slice_items = items.find({'name': {'$in': list_best}})

    return render_template('index.html',
                           category=category,
                           pages=pages,
                           bg=bg_for_index,
                           i_news=i_news,
                           slice_items=slice_items)


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
        if request.method == 'POST' and form.validate() and recaptcha.verify():
            mail.send_feedback(request.base_url, form.name.data,
                               form.email.data, form.phone.data,
                               form.body.data)
            flash(app.config['ANSWER_1'])
            return redirect(url_for('catalog', category_slug=category_slug,
                                    item_slug=item_slug))
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
    build_form = BuildRequest(request.form)
    postmail_form = SendByPostMail(request.form)
    if request.method == 'POST' and request.form['feedback'] == 'Default_Send' and form.validate() and recaptcha.verify():
        mail.send_feedback(request.base_url, form.name.data,
                           form.email.data, form.phone.data,
                           form.body.data)
        flash(app.config['ANSWER_1'])
        return redirect(url_for('page', slug=slug))

    elif request.method == 'POST' and request.form['feedback'] == 'Service_Send' and service_form.validate() and recaptcha.verify():
        mail.send_service_query(
            service_form.equipment.data, service_form.name.data,
            service_form.email.data, service_form.phone.data,
            service_form.body.data, service_form.comment.data)
        flash(app.config['ANSWER_2'])
        return redirect(url_for('page', slug=slug))
    elif request.method == 'POST' and request.form['feedback'] == 'Build_Send' and build_form.validate() and recaptcha.verify():
        mail.send_build_query(request.base_url, build_form.name.data,
                              build_form.email.data, build_form.phone.data,
                              build_form.body.data)
        flash(app.config['ANSWER_3'])
        return redirect(url_for('page', slug=slug))
    elif request.method == 'POST' and request.form['feedback'] == 'Postmail_Send' and postmail_form.validate() and recaptcha.verify():
        mail.send_postmail_query(postmail_form.first_name.data, postmail_form.second_name.data, postmail_form.contact_info.data, postmail_form.count.data, postmail_form.index.data, postmail_form.city.data, postmail_form.adrress.data, postmail_form.middle_name.data, postmail_form.company_name.data, postmail_form.body.data)
        flash(app.config['ANSWER_4'])
        return redirect(url_for('page', slug=slug))
    return render_template('pages.html',
                           form=form,
                           service_form=service_form,
                           postmail_form=postmail_form,
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


@app.route('/news_category/', methods=['GET'])
def news_list2():
    recent_news = n.find().sort('position', -1).limit(4)
    return render_template('news_list2.html',
                           category=category,
                           pages=pages,
                           recent_news=recent_news)

@app.route('/news_category/<slug>', methods=['GET'])
def news_list2_section(slug):
    news = n.find({"section": slug}).sort('position', -1)
    return render_template('news_list.html',
                           category=category,
                           pages=pages,
                           news=news)


@app.route('/news/<slug>', methods=['GET', 'POST'])
def news(slug):
    news = n.find_one({"slug": slug})
    form = FeedbackForm(request.form)
    if request.method == 'POST' and form.validate() and recaptcha.verify():
        mail.send_feedback(request.base_url, form.name.data,
                           form.email.data, form.phone.data,
                           form.body.data)
        flash(app.config['ANSWER_1'])
        return redirect(url_for('news', slug=slug))
    return render_template('news.html',
                           form=form,
                           category=category,
                           pages=pages,
                           news=news)


@app.route('/dealers/', methods=['GET', 'POST'])
def dealers():
    form = FeedbackForm(request.form)
    dealers = d.find({}, {'city': 1, '_id': 0}).sort('city', 1)
    city = []
    for i in dealers:
        for k in i:
            if i[k] not in city:
                city.append(i[k])

    def get_dealers(c):
        sort_d = d.find({'city': c})
        return sort_d

    if request.method == 'POST' and form.validate() and recaptcha.verify():
        mail.send_feedback(request.base_url, form.name.data,
                           form.email.data, form.phone.data,
                           form.body.data)
        flash(app.config['ANSWER_1'])
        return redirect(url_for('dealers'))
    return render_template('dealers.html',
                           city=city,
                           d=get_dealers,
                           category=category,
                           pages=pages,
                           form=form)


@app.route('/admin', methods=['GET', 'POST'])
@requires_auth
def admin():
    form = Empty(request.form)
    if request.method == 'POST' and request.form['send'] == 'UPD_IMG_DB':
        import os
        for the_file in os.listdir(app.config['TMP_PATH']):
            file_path = os.path.join(app.config['TMP_PATH'], the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception, e:
                print e
        import urllib
        urllib.urlretrieve (app.config['GOOGLE_BASE'], "%sdb.xlsx" % app.config['TMP_PATH'])
        secret(app.config['FULL_RM_WRITE'])
    return render_template('admin.html', form=form)


@app.route('/test_img', methods=['GET'])
def test_img():
    names = db.get_all_img()
    return render_template('test_img.html',
                           category=category,
                           pages=pages,
                           names=names)


@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    """Generate sitemap.xml """
    pages = []
    site = app.config['SITE_URL']
    ten_days_ago = datetime.datetime.now() - datetime.timedelta(days=10)
    ten_days_ago = datetime.datetime.date(ten_days_ago)
    # All pages registed with flask apps
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and len(rule.arguments) == 0:
            if not any(rule.rule[0:] in s for s in
                       app.config['EXCEPT_SITEMAP']):
                pages.append((site + rule.rule, ten_days_ago))
    # Категории
    all_cat = cat.find({}, {'slug': 1})
    for i in all_cat:
        if i['slug']:
            pages.append((('%s/catalog/%s' % (site, i['slug'])), ten_days_ago))
    # Товары
    all_items = items.find({}, {'slug_category': 1, 'slug': 1})
    for i in all_items:
        if i['slug']:
            pages.append((('%s/catalog/%s/%s' %
                          (site, i['slug_category'], i['slug'])), ten_days_ago))
    # Статика
    all_pages = p.find({}, {"slug": 1})
    for i in all_pages:
        if not any(rule.rule[0:] in s for s in
                   app.config['EXCEPT_SITEMAP']):
            if i['slug']:
                pages.append((('%s/pages/%s' % (site, i['slug'])),
                              ten_days_ago))
    # Новости
    all_news = n.find({}, {'slug': 1}).sort('position', -1)
    for i in all_news:
        if i['slug']:
            pages.append((('%s/news/%s' % (site, i['slug'])), ten_days_ago))
    sitemap_xml = render_template('sitemap.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"
    return response


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
                           pages=pages), 404


@app.errorhandler(502)
def page_not_found_502(e):
    return render_template('502.html'), 502


@app.route('/robots.txt')
def robots_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route('/pages/novosti')
def r_news():
    return redirect(url_for('news_list'))


@app.route('/pages/software_downloads')
def r_soft_d():
    return redirect(app.config['SOFTWARE_URL'])
