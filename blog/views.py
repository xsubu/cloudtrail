from django.shortcuts import render, redirect, get_object_or_404

from datetime import datetime, timedelta
from .models import *
from .forms import BlogForm, CommentForm


def showAll(request):
    posts = Post.objects.all().filter(is_active=True)
    #posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'blog/index.html', context)

def showDetail(request, slug):
    post = get_object_or_404(Post,slug=slug)

    #update view count
    post.view_count = post.view_count+1
    post.updated_on = datetime.now()
    post.save()

    #form = CommentForm()
    # we reach here if a comment gets submitted
    #if request.method == "POST":
        #form = CommentForm(request.POST)
    #    author = request.POST.get('author','')
    #    content = request.POST.get('content','')
        #blog = post.pk
        #blog_id =request.POST.get('blog_id','')
        #comment = Comment(author=author, content=content, post=post)
        #comment.save()
    #    if form.is_valid():
    #        form = form(post=post)
    #        form.save()
            #return redirect('blog:show')

    # now gather all the comments
    comments = Comment.objects.all().filter(post=post).filter(is_active=True)
    
    context = {
        'post': post,
        'comments': comments,
        #'form': form,
    }
    return render(request, 'blog/detail.html', context)

def AddPost(request):
    form = BlogForm()
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blog:show')

    context = {'form': form}
    return render(request,'blog/addpost.html', context)


def deletePost(request, slug):
    post = get_object_or_404(Post, slug=slug)
    #if not request.user == recipe.author:
    #    return redirect('detail', recipe.id)
    #else:
    post.is_active = not post.is_active
    post.save()
    #post.updated_on = datetime
    return redirect('blog:show')
    
def editPost(request, slug):
    post = get_object_or_404(Post, slug=slug)
    context = {
        'post': post
    }
    if request.method == 'GET':
        form = BlogForm(instance=post)
        context['form'] = form
        return render(request, 'blog/editpost.html', context)
    elif request.method == 'POST':
        form = BlogForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:show')
        else:
            form = BlogForm(instance=post)
            context['form'] = form
            return render(request, 'blog/editpost.html', context)
    return render(request, 'blog/editpost.html', context)

