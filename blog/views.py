from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Post
from .forms import PostForm, RegisterForm


# -----------------------------
# Post List
# -----------------------------
def post_list(request):
    posts_list = Post.objects.filter(
        published_date__lte=timezone.now()
    ).order_by('-published_date')

    paginator = Paginator(posts_list, 5)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, 'blog/post_list.html', {'posts': posts})


# -----------------------------
# Post Detail
# -----------------------------
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


# -----------------------------
# Create Post (Only Logged User)
# -----------------------------
@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form})


# -----------------------------
# Edit Post (Only Owner)
# -----------------------------
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return redirect('post_detail', pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form})


# -----------------------------
# Like Post
# -----------------------------
@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.likes += 1
    post.save()
    return redirect('post_detail', pk=pk)


# -----------------------------
# Register
# -----------------------------
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'blog/register.html', {'form': form})


# -----------------------------
# Login
# -----------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('post_list')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'blog/login.html')


# -----------------------------
# Logout
# -----------------------------
def logout_view(request):
    logout(request)
    return redirect('post_list')