from django.conf.urls import patterns, include, url
from django.conf import settings

from backoffice.views import LoginView, BackofficeView
from sites_flatpage.views import SitesView

urlpatterns =  patterns('backoffice.views',
	#LoginView 
	url(r'^admin_login/$', LoginView.Login.as_view(), name='admin_login'),
	url(r'^admin_logout/$', LoginView.Logout.as_view(), name='admin_logout'),
	#BackofficeView
	url(r'^$', BackofficeView.Index.as_view(), name='admin'),
)

#sites module
urlpatterns += patterns('sites_flatpage.views',
    url(r'^site_pages/$', SitesView.FlatPages.as_view(), name='backoffice_manage_flatpages'),
    url(r'^site_pages/add/$', SitesView.AddPage.as_view(), name="backoffice_add_flatpages"),
    url(r'^site_pages/edit/(?P<page_id>\d+)/$', SitesView.EditPage.as_view(), name="backoffice_edit_flatpages"),
)