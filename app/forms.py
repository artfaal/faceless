# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms.fields import StringField, TextAreaField
from wtforms.validators import DataRequired, Length,  Email


class FeedbackForm(Form):
    name = StringField(u'Имя*', validators=[DataRequired()])
    email = StringField(u'E-mail', validators=[Email()])
    phone = StringField(u'Телефон')
    body = TextAreaField(u'Сообщение',
                         validators=[DataRequired(),
                                     Length(min='5', max='5000')])
