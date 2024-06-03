from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('servicemailing/', ClientListView.as_view(), name='client_list'),
    # path('servicemailing/<slug:slug>/', ClientDetailView.as_view(), name='client_detail'),
    # path('servicemailing/create/', ClientCreateView.as_view(), name='client_create'),
    # path('servicemailing/<slug:slug>/update/', ClientUpdateView.as_view(), name='client_update'),
    # path('servicemailing/<slug:slug>/delete/>', ClientDeleteView.as_view(), name='client_delete'),
]
