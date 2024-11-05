from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .models import Note, Profile
from .forms import NoteForm, SignUpForm, ProfileForm
from django.http import JsonResponse
from django.db.models import Q

@login_required
def note_list(request):
    notes = Note.objects.filter(user=request.user)
    return render(request, 'notes/note_list.html', {'notes': notes})

@login_required
def add_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'notes/add_note.html', {'form': form})

@login_required
def edit_note(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/edit_note.html', {'form': form})

@login_required
def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('note_list')
    return render(request, 'notes/note_confirm_delete.html', {'note': note})

def home(request):
    if request.user.is_authenticated:
        return redirect('note_list')
    return render(request, 'notes/home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('note_list')
    else:
        form = SignUpForm()
    return render(request, 'notes/signup.html', {'form': form})

def view_note(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)  # Ensure the note belongs to the user
    return render(request, 'notes/view_note.html', {'note': note})
@login_required
def note_list(request):
    notes = Note.objects.filter(user=request.user)

    # Handle search query for the initial load (optional)
    query = request.GET.get('q', '')
    if query:
        notes = notes.filter(title__icontains=query)

    return render(request, 'notes/note_list.html', {'notes': notes, 'query': query})

@login_required
def search_notes(request):
    query = request.GET.get('q', '')
    notes = Note.objects.filter(user=request.user, title__icontains=query)
    return JsonResponse({'notes': list(notes.values('id', 'title'))})
@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'notes/profile.html', {'form': form})