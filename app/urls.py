from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns=[
path('about/',views.about,name='about'),
path('resetpass/',views.resetpass,name='resetpass'),
path('ai/',views.ai,name='ai'),
path('contact/',views.contact_us, name='contact_us'),
path('Forgotpass/',views.Forgotpass,name='Forgotpass'),
path('history/',views.history,name='history'),
path('',views.index,name='index'),
path('login/',views.logins,name='login',),
path('Register/',views.Register,name='Register'),
path('service/',views.service,name='service'),
path('reset_password', auth_views.PasswordResetView.as_view(),name='reset_password'),
path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
path('logout/',views.user_logout, name='logout'),
    path('profile/edit/',views.profile_edit, name='profile_edit'),
    path('profile/', views.profile_view, name='profile_view'),
path('change-password/', views.change_password, name='change_password'),
path("reply/<int:message_id>/",views.reply_message, name="reply_message"),
path('messages/',views.user_messages, name='user_messages'),
path('check_usernames/',views.check_usernames, name='check_usernames'),
path('check_username/',views.check_username, name='check_username'),
path("predict/", views.predict),
]