from django.shortcuts import render, redirect, get_object_or_404

from datetime import datetime, timedelta
from .models import *
from .forms import BlogForm, CommentForm
from django.views import generic

#from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
#from .forms import CommentForm



def list_posts_by_tag(request, tag_id):

    tag = get_object_or_404(Tag, id=tag_id)

    posts = Post.objects.filter(is_active=True, tags=tag)

    context = {
        "tag_name": tag.title,
        "posts": posts
    }

    return render(request, 'blog/post_list.html', context)


def post_list(request):
    posts = Post.objects.filter(is_active=True).order_by('-created_on')
    #paginate_by = 1
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, slug):
    template_name = 'blog/post_detail.html'
    post = get_object_or_404(Post, slug=slug)

    #update view count
    post.view_count = post.view_count+1
    post.updated_on = datetime.now()
    post.save()

    comments = post.comments.filter(approved_comment=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})



def AddPost(request):
    form = BlogForm()
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blog:showall')

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
    return redirect('blog:showall')
    
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
            return redirect('blog:showall')
        else:
            form = BlogForm(instance=post)
            context['form'] = form
            return render(request, 'blog/editpost.html', context)
    return render(request, 'blog/editpost.html', context)

