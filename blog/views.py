from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Comment, Vote
from blog.forms import PostForm, CommentForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import get_user_model

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    # posts = Post.objects.all().order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
@csrf_protect
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if "publish" in request.POST:
               post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
@csrf_protect
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
@csrf_protect
def post_delete_confirmation(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_delete_confirmation.html', {"post": post})

@login_required
@csrf_protect
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post = Post.objects.get(id=pk)
        post.delete()

    return render(request, 'blog/post_delete.html', {"post": post})

@login_required
@csrf_protect
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
@csrf_protect
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
@csrf_protect
def post_unpublish(request, pk):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=pk)
        post.published_date = None
        post.save()
    
    return redirect('post_detail', pk=pk)

@login_required
@csrf_protect
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form })

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        comment.approve()

    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        comment.delete()

    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_vote(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        vote = Vote.objects.filter(voter=request.user, comment=comment).first()

        # Toggle vote.
        # Limit vote to only 1 per user comment.
        request_is_upvote = request.POST.get("is_upvote") == "true"
        if vote:
            # Delete if vote is toggled
            if vote.is_upvote == request_is_upvote:
                vote.delete()
            else:
                # Update vote if opposing vote request is submitted.
                vote.is_upvote = request_is_upvote
                vote.save()
        else:
            vote = Vote()
            vote.voter = request.user
            vote.comment = comment
            vote.is_upvote = str(request.POST.get("is_upvote")) == "true"
            vote.save()
    
    return redirect('post_detail', pk=comment.post.pk)