import os

from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

def uploaded_banner_handler(instance, filename):

    fsplit = filename.split('.')
    filetoken = os.urandom(16).encode('hex') + '.' + fsplit[-1]
    path = os.path.join("frontend","cms","sites")

    return os.path.join(path, filetoken.lower())


def get_form_error_messages(form):

    errors = '<ul class="errorLists">'

    for field in form:

        if field.errors:
            errors += '<li>%s' % unicode(field.label)
            errors += '<ul>'

            for error in field.errors:
                errors += '<li>' + error + '</li>'
                
            errors += '</ul>'
            errors += '</li>'

    errors += '</ul>'

    return mark_safe(errors)


def delete_record(model, pk):

    obj = get_object_or_404(model, pk=int(pk))
    obj.delete()

    return True