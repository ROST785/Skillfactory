from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import NewsFilter
from .forms import NewForm
from django.urls import reverse_lazy


class NewsList(ListView):
    model = Post
    ordering = 'post_datetime'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10


class NewDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


class NewCreate(CreateView):
    form_class = NewForm
    model = Post
    template_name = 'new_edit.html'


class NewUpdate(UpdateView):
    form_class = NewForm
    model = Post
    template_name = 'new_edit.html'


class NewDelete(DeleteView):
    model = Post
    template_name = 'new_delete.html'
    success_url = reverse_lazy('new_list')


class NewsSearch(ListView):
    model = Post
    ordering = 'post_datetime'
    template_name = 'news_search.html'
    context_object_name = 'news'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
