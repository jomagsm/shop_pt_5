from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api_v1.views import get_token_view, ProductView, OrderView

app_name = 'api_v1'

router = DefaultRouter()
# router.register(r'article', ProductView)
# router.register(r'order', OrderView)

urlpatterns = [
    path('get-token/', get_token_view, name='get_token'),
    path('', ProductView.as_view(), name='index'),
    path('product/<int:pk>', ProductView.as_view(), name='detail_view'),
    path('product/add/<int:pk>', ProductView.as_view()),
    path('order/<int:pk>', OrderView.as_view()),
    path('order/', OrderView.as_view())
    # path('', include(router.urls))
]