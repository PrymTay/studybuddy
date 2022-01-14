
from django.urls import path
from . import views

urlpatterns = [
    path('edit-message/<str:pk>/',views.edit_message,name='edit_message'),
    path('login/',views.login_page,name='login'),
    path('logout/',views.logout_user,name='logout_user'),
    path('register/',views.register_user,name='register'),
    path('',views.home, name='home' ),
    path('room/<str:pk>',views.room, name='room' ),
    path('create',views.create_room,name='create_room'),
    path('update/<str:pk>/',views.update_room,name='update_room'),
   
    path('delete-message/<str:pk>/',views.delete_message,name='delete_message'),
    path('delete/<str:pk>/',views.delete_room,name='delete_room'),
    path('userprofile/<str:pk>/',views.userProfile,name='user-profile'),
    
        

]
