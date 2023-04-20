from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.edit import FormMixin
from posts.forms import PostForm, CommentForm
from posts.models import Post


class IndexView(ListView):
    template_name = 'posts.html'

    context_object_name = 'posts'
    model = Post

    def get_queryset(self):
        if self.request.user.is_authenticated:
            posts = Post.objects.filter(author__in=self.request.user.subscriptions.all()).order_by('created_at')
            if not posts:
                posts = Post.objects.all().exclude(author=self.request.user).order_by('created_at')
            return posts.annotate(
                is_liked=Count(
                    'user_likes',
                    filter=Q(user_likes=self.request.user),
                    distinct=True
                ),
                likes_number=Count(
                    'user_likes',
                    distinct=True
                )
            )
        else:
            return Post.objects.all().order_by('created_at').annotate(
                likes_number=Count(
                    'user_likes',
                    distinct=True
                )
            )


class CreatePostView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = 'post_create.html'
    model = Post
    form_class = PostForm
    success_message = 'Пост создан'

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        self.object = post
        return HttpResponseRedirect(self.get_success_url())


def like_post(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        request.user.liked_posts.add(post)
        url_from = request.META.get('HTTP_REFERER', '/')
        return redirect(url_from)
    return redirect('login')


def unlike_post(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        request.user.liked_posts.remove(post)
        url_from = request.META.get('HTTP_REFERER', '/')
        return redirect(url_from)
    return redirect('login')


class PostDetailView(FormMixin, DetailView):
    template_name = 'post_detail.html'
    model = Post
    form_class = CommentForm
    context_object_name = 'post'

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.kwargs.get('pk')})

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            form = self.get_form()
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = self.request.user
                comment.post = self.get_object()
                comment.save()
                return HttpResponseRedirect(self.get_success_url())
            else:
                self.form_invalid(form)
        else:
            return HttpResponseRedirect(reverse('login'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        post = self.get_object()
        context['comments_number'] = post.comments.count()
        context['likes_number'] = post.user_likes.count()
        context['is_liked'] = post.user_likes.filter(pk=self.request.user.pk).exists()
        return context
