from django.shortcuts import render, redirect, get_object_or_404, HttpResponse

from datetime import datetime, timedelta
from .models import *
from .forms import BlogForm, CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.urls import reverse_lazy
#from django.views import generic

#from django.views.generic import FormView
#from django.views.generic.detail import SingleObjectMixin
#from django.urls import reverse
#from .forms import CommentForm

from cloudtrail import app_settings


def app_info():
    app = {
    "title": app_settings.APP_NAME,
    "version": app_settings.APP_VER,
    "copyright": app_settings.APP_COPYRIGHT
    }
    return app

def list_posts_by_tag(request, tag_id):

    default_page = 1
    posts_per_page = app_settings.DEFAULT_PER_PAGE

    tag = get_object_or_404(Tag, id=tag_id)

    all_posts = Post.objects.filter(is_active=True, tags=tag)

    #let us read the page num from the GET, if not default to 1
    page_num = request.GET.get('page', default_page)

    paginator = Paginator(all_posts, per_page=posts_per_page)

    #print(paginator.num_pages)

    try:
        posts = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        posts = paginator.page(default_page)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        posts = paginator.page(paginator.num_pages)

    context = {
        "tag_name": tag.title,
        "posts": posts,
        "app": app_info(),
    }

    return render(request, 'blog/post_list.html', context)


def post_list(request):
    #posts = Post.objects.filter(is_active=True).order_by('-created_on')

    default_page = 1
    posts_per_page = app_settings.DEFAULT_PER_PAGE


    all_posts = Post.objects.filter(is_active=True).order_by('-created_on')

    #let us read the page num from the GET, if not default to 1
    page_num = request.GET.get('page', default_page)

    paginator = Paginator(all_posts, per_page=posts_per_page)

    try:
        posts = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        posts = paginator.page(default_page)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        posts = paginator.page(paginator.num_pages)

    

    context = {
        "tag_name": "all",
        "posts": posts,
        "app": app_info,
    }

    #paginate_by = 1
    return render(request, 'blog/post_list.html', context)

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
            #success_url = reverse_lazy("thanks")
            #return redirect(success_url)

    else:
        comment_form = CommentForm()

    # similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(is_active=True).filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-created_on')[:6]


    return render(request, template_name, {'post': post,
                                           'similar_posts': similar_posts,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})



def thanks(request):
    return HttpResponse("Thank you! Will get in touch soon.")

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

