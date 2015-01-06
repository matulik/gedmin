from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',  # Examples:  # url(r'^$', 'gedmin.views.home', name='home'),
					   # url(r'^blog/', include('blog.urls')),  # url(r'^admin/', include(admin.site.urls)),
					   # # login #
					   url(r'^$', 'login.views.main'),
					   url(r'^login/$', 'login.views.login'),
					   url(r'^logout/$', 'login.views.logout'),
					   url(r'^errorpage/$', 'login.views.errorpage'),  # info #
					   url(r'^info/$', 'info.views.main'),
					   url(r'^info/system/$', 'info.views.system'),
					   url(r'^info/drives/$', 'info.views.drives'),
					   url(r'^info/network/$', 'info.views.network'),
					   url(r'^info/cpu/$', 'info.views.cpu'),
					   url(r'^info/mem/$', 'info.views.mem'),  # info_aj #
					   url(r'^info_aj/servertime/$', 'info.views.aj_servertime'),
					   url(r'^info_aj/kernelinfo/$', 'info.views.aj_kernelinfo'),
					   url(r'^info_aj/serverdate/$', 'info.views.aj_serverdate'),
					   url(r'^info_aj/uptime/$', 'info.views.aj_uptime'),
					   url(r'^info_aj/hddlist/$', 'info.views.aj_hddlist'),
					   url(r'^info_aj/partlist/$', 'info.views.aj_partlist'),
					   url(r'^info_aj/hddtemp/$', 'info.views.aj_hddtemp'),
					   url(r'^info_aj/netdevs/$', 'info.views.aj_netdevs'),
					   url(r'^info_aj/localip/$', 'info.views.aj_localip'),
					   url(r'^info_aj/globalip/$', 'info.views.aj_globalip'),
					   url(r'^info_aj/pinginfo/$', 'info.views.aj_pinginfo'),
					   url(r'^info_aj/procinfo/$', 'info.views.aj_procinfo'),
					   url(r'^info_aj/meminfo/$', 'info.views.aj_meminfo'),  # settings #
					   url(r'^settings/$', 'settings.views.main'),
					   url(r'^settings/updateparams/$', 'settings.views.updateparams'),
					   url(r'^settings/changepass/$', 'settings.views.changepass'),
					   url(r'^settings/updatepass/$', 'settings.views.updatepass'),
					   url(r'^settings/logs/$', 'settings.views.logs'),
					   url(r'^settings/logsupdate/$', 'settings.views.logsupdate'),
					   url(r'^settings/tailupdate/$', 'settings.views.tailupdate'),  # inits #
					   url(r'^inits/$', 'inits.views.main'),
					   url(r'^inits/startD/$', 'inits.views.startD'),
					   url(r'^inits/stopD/$', 'inits.views.stopD'),
					   url(r'^inits/restartD/$', 'inits.views.restartD'),  # inits_aj #
					   url(r'^inits_aj/deamons/$', 'inits.views.aj_deamons'),
					   url(r'^inits_aj/deamonoutput/$', 'inits.views.aj_deamonoutput'),  # logs #
					   url(r'^logs/$', 'logs.views.main'),  # portmin #
					   url(r'^portmin/$', 'portmin.views.main'),
					   url(r'^portmin/confiles/$', 'portmin.views.confiles'),  # portmin_aj #
					   url(r'^portmin_aj/sync/$', 'portmin.views.aj_sync'),
					   url(r'^portmin_aj/setsync/$', 'portmin.views.aj_setsync'),
					   url(r'^portmin_aj/upd/$', 'portmin.views.aj_upd'),
					   url(r'^portmin_aj/setupd/$', 'portmin.views.aj_setupd'),


)