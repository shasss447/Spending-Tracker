from django.urls import path
from . import views


urlpatterns=[
    path("",views.home,name="home"),
    path("show_graph/",views.show_graph,name="show_graph"),
    path("analytics/",views.analytics,name="analytics"),
    path("budget/",views.set_budget,name="budget"),
    path("insights/",views.insights,name="insights")
]