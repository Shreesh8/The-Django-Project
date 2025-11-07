from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect,Http404
from .models import Post
from .forms import PostForm, CommentForm, ContactusForm
from django.contrib import messages
from django.db.models import Q

from django.core.paginator import Paginator
#from django.utils.text import slugify

def contact_us(request):
    return render(request, "info/contact.html")

def about_us(request):
    return render(request, "info/about.html")

def post_index(request):

    post_list = Post.objects.all()

    query = request.GET.get("q")

    if query:
        post_list = post_list.filter(
            Q(title__icontains=query) |
            Q(desc__icontains=query)|
            Q(user__first_name__icontains=query)|
            Q(user__last_name__icontains=query)).distinct()

    paginator = Paginator(post_list, 9)  # Show 5 posts per page.

    page = request.GET.get("page")
    posts = paginator.get_page(page)
    return render(request, "post_templates/index.html", {"posts": posts})

def post_detail(request, id):
    post = get_object_or_404(Post, id = id)

    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        print("commented")
        return HttpResponseRedirect(post.get_absolute_url())
    
    context = {
        "post" : post,
        "form" : form,
    }
    
    return render(request, "post_templates/detail.html", context)

def post_create(request):

    if not request.user.is_authenticated:
        return Http404()

#    if request.method == "POST":
#        form = postForm(request.POST)
#        if form.is_valid():
#            form.save()
#    else:
#        form = postForm()

    form = PostForm(request.POST or None, request.FILES or None)
    
    if form.is_valid():
        updated_post = form.save(commit=False)
        updated_post.user = request.user
        updated_post.save()
        return HttpResponseRedirect(updated_post.get_absolute_url())

    context = {
        "title" : "Create Post",
        "form" : form
    }

    return render(request, "post_templates/form.html", context)

def post_update(request, id):

    if not request.user.is_authenticated:
        return Http404()

    post = get_object_or_404(Post, id = id)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)

    if form.is_valid():
        form.save()
        updated_post = form.save()
        return HttpResponseRedirect(updated_post.get_absolute_url())
    
    context = {
        "title" : "Update Post",
        "form" : form,
    }
    return render(request, "post_templates/form.html", context)

def post_delete(request, id):

    if not request.user.is_authenticated:
        return Http404()

    deleted_post = get_object_or_404(Post, id = id)
    deleted_post.delete()
    return redirect('post:index')

def contact_us(request):
    form = ContactusForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, "info/contact.html", {'form':form, 'title':'Info'})