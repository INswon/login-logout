from django.urls import path, include
from . import views


app_name ='account'

urlpatterns = [
    path('', views.TempView.as_view(), name='top'),
    path('login/', views.Login.as_view(), name="login"),
    path('logout/',views.Logout.as_view(), name="logout"),
    path('my_page/<int:pk>/',views.MyPage.as_view(),name="my_page"),
    path('user_update/<int:pk>', views.UserUpdate.as_view(), name='user_update'),
    path('signup/', views.Signup.as_view(), name='signup'), # サインアップ
    path('signup_done/', views.SignupDone.as_view(), name='signup_done'), # サインアップ完了
]