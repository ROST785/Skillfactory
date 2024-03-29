from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Announcement, Category, Response
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AnnouncementForm, ResponseForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .filters import ResponsesFilter


class AdsList(ListView):
    model = Announcement
    ordering = 'date'
    template_name = 'ads.html'
    context_object_name = 'ads'


class AnnouncementDetail(DetailView):
    model = Announcement
    template_name = 'announcement.html'
    context_object_name = 'announcement'


class AnnouncementCreate(CreateView, LoginRequiredMixin):
    form_class = AnnouncementForm
    model = Announcement
    template_name = 'announcement_edit.html'


class AnnouncementUpdate(UpdateView, LoginRequiredMixin):
    form_class = AnnouncementForm
    model = Announcement
    template_name = 'announcement_edit.html'


class AnnouncementDelete(DeleteView, LoginRequiredMixin):
    form_class = AnnouncementForm
    model = Announcement
    template_name = 'announcement_delete.html'
    success_url = reverse_lazy('ads_list')


class CategoryList(ListView):
    model = Announcement
    template_name = 'category_list.html'
    context_object_name = 'category_ads_list'

    def get_queryset(self):
        self.categories = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Announcement.objects.filter(categories=self.categories).order_by('-date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.categories.subscribers.all()
        context['categories'] = self.categories
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы подписались на рассылку новостей категории'
    return render(request, 'subscribe.html', {'category': category, 'message': message})


class ResponsesList(ListView, LoginRequiredMixin):
    model = Response
    ordering = 'date'
    template_name = 'responses.html'
    context_object_name = 'responses'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ResponsesFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ResponseDetail(DetailView, LoginRequiredMixin):
    model = Response
    template_name = 'response.html'
    context_object_name = 'response'


class ResponseCreate(CreateView, LoginRequiredMixin):
    form_class = ResponseForm
    model = Announcement
    template_name = 'response_create.html'
