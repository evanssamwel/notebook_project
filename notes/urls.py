from django.urls import path
from . import views
from .views import note_list, add_note, edit_note, delete_note, search_notes

urlpatterns = [
    path('', views.note_list, name='note_list'),  # Home page or note list
    path('add/', views.add_note, name='add_note'),  # Add new note
    path('<int:pk>/edit/', views.edit_note, name='edit_note'),  # Edit note
    path('<int:pk>/delete/', views.delete_note, name='delete_note'),  # Delete note
    path('<int:pk>/', views.view_note, name='view_note'),  # View note
    path('signup/', views.signup, name='signup'),  # Signup page
    path('search/', views.search_notes, name='search_notes'),  # Search notes
    path('profile/', views.profile_view, name='profile'),  # Profile page
]
