import decimal

from django import template
from django.utils.safestring import mark_safe
from django.contrib.humanize.templatetags.humanize import naturaltime, intcomma
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from urllib import quote, quote_plus
from django.utils import simplejson

register = template.Library()

@register.filter
def display_messages(messages, tag=None):

    if messages:


        if tag:
            return_message = ['<li>%s</li>' % (m) for m in messages if str(tag) in m.tags]
            tags = [(m.tags) for m in set(messages) if str(tag) in m.tags]

        else:
            return_message = ['<li>%s</li>' % (m) for m in messages]
            print return_message
            tags = [(m.tags) for m in set(messages)]
        
        if not return_message:
            return ""
        else:
            html_message = """
            <div class="messages %s">
                <ul>%s</ul>
            </div>
            """ % ("".join(tags), "\n".join(return_message))

            return mark_safe(html_message)
    
    return ""


@register.filter
def display_field_errors(field_errors):

    if field_errors:
        return_message = ["<li>%s</li>" % m for m in field_errors]
        html_message = """
        <div class="messages fieldErrors error">
            <ul> %s </ul>
        </div>
        """ % ("\n".join(return_message))

        return mark_safe(html_message)

    return ""


@register.filter
def fullname(user):

    fullname = ""

    if user.first_name and user.last_name:
        fullname += "%s, %s" % (user.last_name, user.first_name)
    
    return fullname.title()


@register.filter
def readable_usertype(value):

    usertype = 'admin' if value else 'member'

    return usertype.title()