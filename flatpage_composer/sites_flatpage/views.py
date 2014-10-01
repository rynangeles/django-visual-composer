import logging
import django_wysiwyg

# django
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseNotFound, Http404
from django.conf import  settings
from django.shortcuts import render_to_response, redirect, HttpResponse, render, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.contrib import messages, admin
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

# sites
from sites_flatpage.models import ExtendedFlatPage
from sites_flatpage.forms import ExtendedFlatPageForm
from sites_flatpage.utils import get_form_error_messages, delete_record

class SitesView(object):

    class FlatPages(View):
        template_name = 'sites_flatpage/flatpages.html'
        info = {}
        
        def get(self, request, *args, **kwargs):
            pk = request.GET.get('pk')
            if request.GET.get('action') == 'del':
                if delete_record(ExtendedFlatPage, pk=pk):
                    messages.success(request, _('Site page has been deleted'))
                    return redirect('backoffice_manage_flatpages')

            self.info['flatpages'] = ExtendedFlatPage.objects.all() 
            return render(request, self.template_name, self.info)

        @method_decorator(staff_member_required)
        def dispatch(self, *args, **kwargs):
            return super(SitesView.FlatPages, self).dispatch(*args, **kwargs)


    class AddPage(View):
        template_name = 'sites_flatpage/create_page.html'
        info = {}
        form = ExtendedFlatPageForm

        def get(self, request, *args, **kwargs):
            self.info['form'] = self.form()
            return render(request, self.template_name, self.info)

        def post(self, request, *args, **kwargs):
            data = request.POST.copy()
            data['sites'] = 1
            data['content'] = django_wysiwyg.clean_html(data['content'])
            data['flatPage'] = ExtendedFlatPage
            form = self.form(data)

            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, _('New site page has been added'))
                    return redirect('backoffice_manage_flatpages')
                    
                except Exception as e:
                    messages.error(request, _('An error has occurred'))
            else:
                # error = get_form_error_messages(form)
                messages.error(request, _('Please correct the errors, and resubmit the form.'), extra_tags='form_error')
                
            self.info['form'] = form
            return render(request, self.template_name, self.info)

        @method_decorator(staff_member_required)
        def dispatch(self, *args, **kwargs):
            return super(SitesView.AddPage, self).dispatch(*args, **kwargs)


    class EditPage(View):
        template_name = 'sites_flatpage/create_page.html'
        form = ExtendedFlatPageForm
        info = {}

        def get(self, request, *args, **kwargs):
            instance = get_object_or_404(ExtendedFlatPage, id=int(kwargs.get('page_id')))
            self.info['form'] = self.form(instance=instance)

            return render(request, self.template_name, self.info)

        def post(self, request, *args, **kwargs):
            instance = get_object_or_404(ExtendedFlatPage, id=int(kwargs.get('page_id')))
            data = request.POST.copy()
            data['sites'] = 1
            data['content'] = django_wysiwyg.clean_html(data['content'])
            form = self.form(data, instance=instance)

            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, _('Site page has been updated'))
                    return redirect('backoffice_manage_flatpages')
                except Exception as e:
                    messages.error(request, _('An error has occurred'))
                form.save()

            else:
                # error = get_form_error_messages(form)
                messages.error(request, _('Please correct the errors, and resubmit the form.'), extra_tags='form_error')
                
            self.info['form'] = form
            return render(request, self.template_name, self.info)

        @method_decorator(staff_member_required)
        def dispatch(self, *args, **kwargs):
            return super(SitesView.EditPage, self).dispatch(*args, **kwargs)