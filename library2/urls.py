
"""Library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from django.urls import path,include
from . import views


urlpatterns = [
  path('',views.home,name = 'home'),
  path('signin/',views.sign_in,name = 'sign_in'),
  path('signup/',views.sign_up,name = 'sign_up'),
  path('logout/',views.logout_wt,name= 'logout_'),
  path('book/<int:sno>/',views.book_spec,name = 'book_spec'),
  path('borrow_book/<int:sno>/',views.borrow_book,name = 'book_borrow'),
  path('return_book/<int:sno>/',views.return_book,name = 'return_borrow'),
  path('settings/',views.settings,name = 'settings'),
  path('comment/',views.submit_comment,name  = 'submitcomment'),

  
  

    ]