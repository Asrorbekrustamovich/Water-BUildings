"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/roles/', RoleListCreateView.as_view(), name='role-list-create'),
    path('api/roles/<int:pk>/', RoleDetailView.as_view(), name='role-detail'),
    path('api/send-email/', send_email_view, name='send_email'),
    path('api/users/', UserListCreateView.as_view(), name='user-list-create'),
    path('api/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('api/viloyats/', ViloyatListCreateView.as_view(), name='viloyat-list-create'),
    path('api/viloyats/<int:pk>/', ViloyatDetailView.as_view(), name='viloyat-detail'),
    path('api/mchjs/', MCHJListCreateView.as_view(), name='mchj-list-create'),
    path('api/mchjs/<int:pk>/', MCHJDetailView.as_view(), name='mchj-detail'),
    path('api/xodimlars/', XodimlarListCreateView.as_view(), name='xodimlar-list-create'),
    path('api/xodimlars/<int:pk>/', XodimlarDetailView.as_view(), name='xodimlar-detail'),
    path('api/mchjusers/', MCHJUserListCreateView.as_view(), name='mchjuser-list-create'),
    path('api/mchjusers/<int:pk>/', MCHJUserDetailView.as_view(), name='mchjuser-detail'),
    path('api/types/', TypeListCreateView.as_view(), name='type-list-create'),
    path('api/types/<int:pk>/', TypeDetailView.as_view(), name='type-detail'),
    path('api/holats/', HolatListCreateView.as_view(), name='holat-list-create'),
    path('api/holats/<int:pk>/', HolatDetailView.as_view(), name='holat-detail'),
    path('api/messages/', MessageListCreateAPIView.as_view(), name='message-list-create'),
    path('api/messages/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
    path('notifications/', NotificationListCreateView.as_view(), name='notification-list-create'),
    path('notifications/<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
    path('api/instruments/', InstrumentListCreateView.as_view(), name='instrument-list-create'),
    path('api/instruments/<int:pk>/', InstrumentDetailView.as_view(), name='instrument-detail'),
    path('api/instruments/mchj/<int:mchj_id>/', Get_Instruments_Based_On_MCHJ.as_view(), name='get-instruments-based-on-mchj'),
    path('api/mchjs/viloyat/<int:viloyat_id>/', Get_MCHJ_based_on_viloyat.as_view(), name='get-mchj-based-on-viloyat'),
    path('api/counts/viloyat/<int:viloyat_id>/', Get_MCHJ_count_and_instruments_count_and_Xodimlar_count_based_on_viloyat.as_view(), name='get-counts-based-on-viloyat'),
    path('api/counts/mchj/<int:mchj_id>/', GetCountsBasedOnMCHJ.as_view(), name='get-counts-based-on-mchj'),
    path('api/counts/all/', GetAllCountsbasedMCHJ.as_view(), name='get-all-counts'),
    path("api/get_all_mchj_all_infos/<int:viloyat_id>/",Get_MCHJ_and_counts_based_on_viloyat.as_view(),name='get-mchj-and-counts-based-on-viloyat'),
    path('api/notifications/<int:notification_id>/read/', MarkNotificationAsRead.as_view(), name='mark_notification_as_read'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/ALLCOUNTS/', GetAllCounts.as_view(), name='all-counts'),
    # path('messages/admin/send/<int:mchj_id>/', AdminSendMessageToMCHJView.as_view(), name='admin-send-message-to-mchj'),
    # path('messages/admin/<int:mchj_id>/', AdminMCHJMessagesView.as_view(), name='admin-mchj-messages'),
    path('api/messages/admin/send/<int:mchj_id>/', AdminSendMessageToMCHJView.as_view(), name='admin-send-message-to-mchj'),
    path('api/messages/mchj/send/<int:mchj_id>/', MCHJSendMessageToAdminView.as_view(), name='mchj-send-message-to-admin'),
    path('api/messages/<int:pk>/<int:role_id>/', MessageDetailView1.as_view(), name='message-detail'),
    path('api/GeTallmessagesbetweenMCHJandAdmin/admin/<int:mchj_id>/', GetMessagesBetweenAdminAndMCHJ.as_view(), name='admin-mchj-messages'),
    path('api/GetMessagesBetweenAdminAndMCHJ/mchj/<int:mchj_id>/',GetMessagesBetweenAdminAndMCHJ2.as_view(),name='mchj-admin-messages'),
    path('api/UnreadMessagesForMCHJView/',UnreadMessagesForMCHJView.as_view()),
    path('api/CountUnreadMessagesForAdminView/',CountUnreadMessagesForAdminView.as_view()),
    path('api/unread-messages-for-mchj/<int:mchj_id>/', CountUnreadMessagesForMCHJView.as_view(), name='unread-messages-for-mchj'),
    path("api/mchj_boshliqlar_raqamlari/",MCHJUserListView.as_view()),
    path('api/documents/', DocumentListCreateView.as_view(), name='document-list-create'),
    path('api/documents/<int:pk>/', DocumentRetrieveUpdateDestroyView.as_view(), name='document-retrieve-update-destroy'),
    path('api/documents/user/<int:user_id>/', UserDocumentListView.as_view(), name='user-document-list')
    ]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)