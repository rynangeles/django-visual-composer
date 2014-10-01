from datetime import datetime, timedelta

from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import HttpResponse, redirect, render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, QueryDict, HttpResponseForbidden
from django.contrib import auth, messages
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.utils.safestring import mark_safe
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from backoffice.models import LoginLog

class LoginView(object):

    class Login(View):

        def get(self, request, *args, **kwargs):
            #can't access this via GET
            return HttpResponseRedirect(settings.BACKOFFICE_LOGIN_REDIRECT)

        def post(self, request, *args, **kwargs):
            logout(request)

            loginLog = LoginLog.objects.filter(created__gte=(datetime.now() - timedelta(minutes=5)), ip_address=request.META['REMOTE_ADDR'])
            next = request.POST['next'] if str(request.POST['next']).strip() != "" else settings.BACKOFFICE_LOGIN_REDIRECT
            username = request.POST['username']
            password = request.POST['password']
            request.session['admin_username'] = username
            request.session['admin_password'] = password

            user = authenticate(username=username, password=password)

            if loginLog.count() >= 5:
                messages.error(request, _('Please try to login after 5 minutes'), extra_tags='login_error')

                return HttpResponseRedirect(next)

            if str(username).strip() == "" or str(password).strip() == "":
                
                if str(username).strip() == "":
                    messages.error(request, _('Username field is required'), extra_tags='user_empty')

                if str(password).strip() == "":
                    messages.error(request, _('Password field is required'), extra_tags='password_empty')

                return HttpResponseRedirect(next)

            if user is not None:

                if user.is_active and user.is_staff:
                    login(request, user)

                    try:
                        del request.session['admin_username']
                        del request.session['admin_password']

                    except KeyError:
                        pass

                    LoginLog.objects.filter(ip_address=request.META['REMOTE_ADDR']).delete()

                else:
                    messages.error(request, _('Sorry this account is disabled'))
            else:
                loginLog = LoginLog()
                loginLog.created = datetime.now()
                loginLog.ip_address = request.META['REMOTE_ADDR']
                loginLog.save()

                messages.error(request, _('Sorry we could not verify your username and password'), extra_tags='login_error')

            return HttpResponseRedirect(next)

    class Logout(View):

        def get(self, request, *args, **kwargs):
            try:
                del request.session['admin_username']
                del request.session['admin_password']

            except KeyError:
                pass

            logout(request)

            return HttpResponseRedirect(settings.BACKOFFICE_LOGIN_REDIRECT)



class BackofficeView(object):

    class Index(View):

        template_name = 'backoffice/index.html'
        info = {}

        def get(self, request, *args, **kwargs):
            return render_to_response(self.template_name ,self.info, RequestContext(request))
            # return redirect(reverse('backoffice_manage_flatpages'))

        @method_decorator(staff_member_required)
        def dispatch(self, *args, **kwargs):
            return super(BackofficeView.Index, self).dispatch(*args, **kwargs)
