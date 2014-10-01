from django.contrib import admin
from django.contrib.flatpages.admin import FlatpageForm, FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import ugettext_lazy as _

from sites_flatpage.models import ExtendedFlatPage

class ExtendedFlatPageForm(FlatpageForm):

    class Meta:
        model = ExtendedFlatPage
    
    def __init__(self, *args, **kwargs):
        super(ExtendedFlatPageForm, self).__init__(*args, **kwargs)

        # if you want to do it to all of them
        # for field in self.fields.values():
        #     field.error_messages = {'required':'The field %s is required' % unicode(field.label)}

        # self.fields['url'].error_messages = {'invalid': 'Enter a valid value in field URL'}


class ExtendedFlatPageAdmin(FlatPageAdmin):
    form = ExtendedFlatPageForm
    fieldsets = ((None, {'fields': ('url', 'title', 'content','sites', 'banner', 'banner_thumbnail' )}),)


admin.site.unregister(FlatPage)
admin.site.register(ExtendedFlatPage, ExtendedFlatPageAdmin)