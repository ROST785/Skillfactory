from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from .filters import NewsFilter
from .forms import NewForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.core.cache import cache


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

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj


class NewCreate(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    form_class = NewForm
    model = Post
    template_name = 'new_edit.html'
    permission_required = 'news.add_post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'Статья'
        return super().form_valid(form)


class NewUpdate(UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    form_class = NewForm
    model = Post
    template_name = 'new_edit.html'
    permission_required = 'news.change_post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'Статья'
        return super().form_valid(form)


class NewDelete(DeleteView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Post
    template_name = 'new_delete.html'
    success_url = reverse_lazy('new_list')
    permission_required = 'news.delete_post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'Статья'
        return super().form_valid(form)


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


class CategoryList(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.categories = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(categories=self.categories).order_by('-post_datetime')
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
