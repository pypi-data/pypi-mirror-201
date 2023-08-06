from django.urls import path
from .views import TicketCreateAPIView, TicketMetaRetrieveView

urlpatterns = [
    path(r"tickets/", view=TicketCreateAPIView.as_view(), name="ticket-create"),
    path(r"tickets/<pk>/meta/", view=TicketMetaRetrieveView.as_view(), name="ticket-meta-download"),
]
