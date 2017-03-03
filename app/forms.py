# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms.fields import StringField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length,  Email


class FeedbackForm(Form):
    name = StringField(u'Имя*:', validators=[DataRequired()])
    email = StringField(u'E-mail*:', validators=[Email()])
    phone = StringField(u'Телефон:')
    body = TextAreaField(u'Сообщение*:',
                         validators=[DataRequired(),
                                     Length(min=5, max=5000)])


class BuildRequest(Form):
    name = StringField(u'Имя*:', validators=[DataRequired()])
    email = StringField(u'E-mail*:', validators=[Email()])
    phone = StringField(u'Телефон:')
    body = TextAreaField(u'Сообщение*:',
                         validators=[DataRequired(),
                                     Length(min=5, max=5000)])


class ServiceRequest(Form):

    '''
    Форма для страницы: "Он-лайн заявка на проведение Сервисного обслуживания"
    '''
    equipment = StringField(u'Оборудование*:', validators=[DataRequired()])
    body = TextAreaField(u'Описание неисправности*:',
                         validators=[DataRequired(),
                                     Length(min=5, max=5000)])
    name = StringField(u'Имя*:', validators=[DataRequired()])
    phone = StringField(u'Телефон:')
    email = StringField(u'E-mail*:', validators=[Email()])
    comment = StringField(u'Комментарий:')


class SendByPostMail(Form):
    '''
    Для отправки печатной продукции на физический почтовый адрес
    '''
    first_name = StringField(u'Имя: *', validators=[DataRequired()])
    second_name = StringField(u'Фамилия: *', validators=[DataRequired()])
    middle_name = StringField(u'Отчество:')
    contact_info = StringField(u'E-mail или телефон для связи: *', validators=[DataRequired()])
    company_name = StringField(u'Название кампании:')
    count = StringField(u'Количество каталогов: *', validators=[DataRequired()], default=1)
    index = StringField(u'Индекс: *', validators=[DataRequired()])
    city = StringField(u'Город/Населенный пункт: *', validators=[DataRequired()])
    adrress = StringField(u'Улица, дом, корпус/строение, квартира/офис: *', validators=[DataRequired()])
    body = TextAreaField(u'Сообщение:')


class Empty(Form):
    pass
