from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, ListView
from accounts.forms import LoginForm, CustomUserCreationForm, UserChangeForm, SearchForm


class LoginView(TemplateView):
    template_name = 'login.html'
    form = LoginForm

    def get(self, request, *args, **kwargs):
        form = self.form
        context = {'form': form}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if not form.is_valid():
            messages.error(request, 'Некорректные данные')
            return redirect('login')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, email=email, password=password)
        if not user:
            messages.warning(request, 'Неправильное имя пользователя или пароль')
            return redirect('login')
        messages.success(request, 'Добро пожаловать')
        next = request.GET.get('next')
        login(request, user)
        if next:
            return redirect(next)
        return redirect('index')


def logout_view(request):
    logout(request)
    return redirect('index')


class RegisterView(CreateView):
    template_name = 'registration.html'
    form_class = CustomUserCreationForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(self.success_url)
        context = {'form': form}
        return self.render_to_response(context)


class ProfileView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'user_detail.html'
    paginate_related_by = 9
    paginate_related_orphans = 0

    def get_context_data(self, **kwargs):
        posts = self.object.posts.order_by('-created_at')
        paginator = Paginator(
            posts,
            self.paginate_related_by,
            orphans=self.paginate_related_orphans
        )
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        kwargs['subscribe'] = self.request.user.subscriptions.filter(pk=kwargs.get('object').pk).exists()
        kwargs['user_obj'] = kwargs.get('object')
        kwargs['posts_count'] = self.object.posts.count()
        kwargs['subscribers'] = self.object.subscribers.count()
        kwargs['subscriptions'] = self.object.subscriptions.count()
        kwargs['page_obj'] = page
        kwargs['posts'] = page.object_list
        kwargs['is_paginated'] = page.has_other_pages()
        return super().get_context_data(**kwargs)


class UserChangeView(UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = 'user_change.html'
    context_object_name = 'user'

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})


def subscribe_on_account(request, pk):
    if request.user.is_authenticated:
        account_to_follow = get_object_or_404(get_user_model(), pk=pk)
        request.user.subscriptions.add(account_to_follow)
        return redirect('profile', account_to_follow.pk)
    return redirect('login')


def unsubscribe_on_account(request, pk):
    if request.user.is_authenticated:
        account_to_unsubscribe = get_object_or_404(get_user_model(), pk=pk)
        request.user.subscriptions.remove(account_to_unsubscribe)
        return redirect('profile', account_to_unsubscribe.pk)
    return redirect('login')


class SearchAccountsView(ListView):
    template_name = 'search_accounts.html'

    context_object_name = 'accounts'
    model = get_user_model()
    ordering = ['-username']

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(email__icontains=self.search_value) | Q(username__icontains=self.search_value) | Q(
                first_name__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None
