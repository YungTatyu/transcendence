from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .models import Note


class NoteListView(ListView):
    model = Note
    template_name = "notes/note_list.html"


class NoteCreateView(CreateView):
    model = Note
    template_name = "notes/note_form.html"
    fields = ["title", "content"]
    success_url = reverse_lazy("note_list")


class NoteUpdateView(UpdateView):
    model = Note
    template_name = "notes/note_form.html"
    fields = ["title", "content"]
    success_url = reverse_lazy("note_list")


class NoteDeleteView(DeleteView):
    model = Note
    success_url = reverse_lazy("note_list")
