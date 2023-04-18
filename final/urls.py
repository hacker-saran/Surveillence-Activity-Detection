from django.urls import path
from . import views
urlpatterns = [
path('video',views.video,name="video"),
path('output/<str:f1>/<str:f2>',views.output,name="output_vids"),
]