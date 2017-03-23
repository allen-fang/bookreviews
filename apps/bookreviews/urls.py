from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index), # render login and registration page
    url(r'^books$', views.home), # render home page
    url(r'^process_logreg$', views.process_logreg), # process login and registration
    url(r'^logout$', views.logout), # logout
    url(r'^add_review$', views.add_review_page), # render adding a review page
    url(r'^post_review$', views.post_review), # process form with new book and review
    url(r'^books/(?P<id>\d+)$', views.books), # render book page
    url(r'^post_review2/(?P<id>\d+)$', views.post_review2), # add review from existing book page
    url(r'^user/(?P<id>\d+)$', views.user), # render user page
    url(r'^delete_review/(?P<id>\d+)$', views.delete_review), # delete a review
]
