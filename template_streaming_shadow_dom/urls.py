from django.urls import path

from streaming.views import shadow_dom_streaming_example

urlpatterns = [
    path("", shadow_dom_streaming_example),
]
