# from django.forms import ModelForm
# from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
# from .forms import NoteForm
from .models import Note


class IndexView(generic.ListView):
    template_name = 'notes/index.j2'
    context_object_name = 'latest_notes_list'

    def get_queryset(self):
        return Note.objects.order_by('-update_date')[:10]

class DetailView(generic.DetailView):
    model = Note
    template_name = 'notes/detail.j2'

    def get_queryset(self):
        return Note.objects.filter(update_date__lte=timezone.now())

class AddView(generic.edit.CreateView):
    model = Note
    template_name = 'notes/add.j2'
    fields = ['title', 'content']
    success_url = reverse_lazy('notes:home')

class EditView(generic.edit.UpdateView):
    model = Note
    template_name = 'notes/edit.j2'
    fields = ['title', 'content']
    # success_url = reverse_lazy('notes:edit') -- what to set this with notification of success
    success_url = reverse_lazy('notes:home')

class DeleteView(generic.edit.DeleteView):
    model = Note
    template_name = 'notes/delete.j2'
    success_url = reverse_lazy('notes:home')
