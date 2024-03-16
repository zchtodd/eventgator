from django.urls import path
from core.views.users import signup_view, login_view
from core.views.events import (
	search_view, 
  	event_view, 
  	event_create_view, 
  	event_edit_view,
    event_register_view,
    event_unregister_view,
)

urlpatterns = [
    path("accounts/login/", login_view, name="login"),
    path("accounts/signup/", signup_view, name="signup"),
	path("search", search_view, name="search"),
    path("event/<int:event_id>", event_view, name="event"),
    path("events", event_create_view, name="event_create"),
    path("event/<int:event_id>/edit", event_edit_view, name="event_edit"),
    path("event/<int:event_id>/register", event_register_view, name="event_register"),
    path("event/<int:event_id>/unregister", event_unregister_view, name="event_unregister"),
]