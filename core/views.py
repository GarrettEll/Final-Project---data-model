from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from .models import Post, Comment, Category, Conversation
from .forms import PostForm, CommentForm, ConversationForm

import random

class PostListView(ListView):
    model = Post
    template_name = 'core/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__name=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        # Add random quote
        quotes = [
            {"text": "The beautiful thing about learning is nobody can take it away from you.", "author": "B.B. King"},
            {"text": "Education is the most powerful weapon which you can use to change the world.", "author": "Nelson Mandela"},
            {"text": "The expert in anything was once a beginner.", "author": "Helen Hayes"},
            {"text": "Learning never exhausts the mind.", "author": "Leonardo da Vinci"},
        ]
        context['quote'] = random.choice(quotes)
        return context


# Post Detail View
class PostDetailView(DetailView):
    model = Post
    template_name = 'core/post_detail.html'

# Post Create View
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'core/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Post Update View
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'core/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Post Delete View
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    template_name = 'core/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Add Comment to Post
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'core/add_comment.html', {'form': form})

# User Signup View
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})

# Conversations Page (with search + create)
from .forms import ConversationForm, ReplyForm

def conversations_page(request):
    query = request.GET.get('q')
    form = ConversationForm()
    reply_form = ReplyForm()

    if request.method == 'POST':
        if 'conversation-submit' in request.POST:
            form = ConversationForm(request.POST)
            if form.is_valid():
                convo = form.save(commit=False)
                convo.author = request.user
                convo.save()
                return redirect('conversations')

        elif 'reply-submit' in request.POST:
            reply_form = ReplyForm(request.POST)
            convo_id = request.POST.get('conversation_id')
            convo = get_object_or_404(Conversation, id=convo_id)
            if reply_form.is_valid():
                reply = reply_form.save(commit=False)
                reply.author = request.user
                reply.conversation = convo
                reply.save()
                return redirect('conversations')

    conversations = Conversation.objects.all().order_by('-created_at')
    if query:
        conversations = conversations.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    return render(request, 'core/conversations.html', {
        'form': form,
        'reply_form': reply_form,
        'conversations': conversations,
    })


# Edit Conversation (Staff only)
class ConversationUpdateView(UserPassesTestMixin, UpdateView):
    model = Conversation
    form_class = ConversationForm
    template_name = 'core/conversation_form.html'
    success_url = reverse_lazy('conversations')

    def test_func(self):
        return self.request.user.is_staff

# Delete Conversation (Staff only)
class ConversationDeleteView(UserPassesTestMixin, DeleteView):
    model = Conversation
    template_name = 'core/conversation_confirm_delete.html'
    success_url = reverse_lazy('conversations')

    def test_func(self):
        return self.request.user.is_staff
