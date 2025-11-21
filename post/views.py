from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect, Http404
from django.urls import reverse
from .models import Post, UserUpvote, ContactInfo
from django.contrib.auth.models import User
from .forms import PostForm, CommentForm, ContactusForm
from django.contrib import messages
from django.db.models import Q
from django.db.models import F

from django.core.paginator import Paginator
#from django.utils.text import slugify

def contact_us(request):
    return render(request, "info/contact.html")

def about_us(request):
    return render(request, "info/about.html")

def upvote_post(request, id):
    #posts = Post.objects.get(id=id)
    post = get_object_or_404(Post, id = id)

    if not request.user.is_authenticated:
        raise Http404()

    already_upvoted = UserUpvote.objects.filter(user = request.user,post=post)

    if already_upvoted.exists():
        already_upvoted.delete()
        Post.objects.filter(id=post.id).update(upvotes=F("upvotes") - 1)
    else:
        UserUpvote.objects.create(user = request.user,post=post)
        Post.objects.filter(id=post.id).update(upvotes=F("upvotes") + 1)

    page = request.GET.get("page", 1)
    return redirect(f"{reverse('post:index')}?page={page}")

def upvote_post_detail(request, id):
    
    post = get_object_or_404(Post, id = id)

    if not request.user.is_authenticated:
        raise Http404()

    already_upvoted = UserUpvote.objects.filter(user = request.user,post=post)

    if already_upvoted.exists():
        already_upvoted.delete()
        Post.objects.filter(id=post.id).update(upvotes=F("upvotes") - 1)
    else:
        UserUpvote.objects.create(user = request.user,post=post)
        Post.objects.filter(id=post.id).update(upvotes=F("upvotes") + 1)

    return redirect(post.get_absolute_url())

def post_index(request):

    post_list = Post.objects.all()

    post_ids = post_list.values_list('id', flat=True)

    upvoted_qs = UserUpvote.objects.filter(user=request.user, post_id__in=post_ids)
    upvoted_posts = set(upvoted_qs.values_list('post_id', flat=True))


    query = request.GET.get("q")

    if query:
        post_list = post_list.filter(
            Q(title__icontains=query) |
            Q(desc__icontains=query)|
            Q(user__first_name__icontains=query)|
            Q(user__last_name__icontains=query)).distinct()

    paginator = Paginator(post_list, 9)  # Show 9 posts per page.

    page = request.GET.get("page")
    posts = paginator.get_page(page)

    context = {
        "posts" : posts,
        "upvoted_posts" : upvoted_posts,
    }

    return render(request, "post_templates/index.html", context)

def post_detail(request, id):
    post = get_object_or_404(Post, id = id)
    post_list = Post.objects.all()

    post_ids = post_list.values_list('id', flat=True)

    upvoted_qs = UserUpvote.objects.filter(user=request.user, post_id__in=post_ids)
    upvoted_posts = set(upvoted_qs.values_list('post_id', flat=True))

    post_views = Post.objects.filter(id=post.id).update(post_views=F("post_views") + 1)

    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
        print("commented")
        return HttpResponseRedirect(post.get_absolute_url())
    
    context = {
        "post" : post,
        "form" : form,
        "upvoted_posts" : upvoted_posts,
        "post_views": post_views,
    }
    
    return render(request, "post_templates/detail.html", context)

def post_create(request):

    if not request.user.is_authenticated:
        raise Http404("not_athenticated")

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



def modify_contact_adminpanel(request, id):

    if not request.user.is_authenticated and not request.user.is_staff:
        raise Http404("not_athenticated")

    contact = get_object_or_404(ContactInfo, id = id)

    if contact.user == request.user or request.user.is_staff: # cant update posts if its a different user ... but if he is staff he can
        form = ContactusForm(request.POST or None, request.FILES or None, instance=contact)
        if form.is_valid():
            form.save()
            form.save()
            return  redirect('/accounts/admin_panel/contacts')
        
        context = {
            "title" : "Update Contact",
            "form" : form,
        }
        return render(request, "post_templates/form.html", context)
    else:
        raise Http404("cant update wrong user")


def post_update(request, id):

    if not request.user.is_authenticated:
        raise Http404("not_athenticated")

    post = get_object_or_404(Post, id = id)

    if post.user == request.user or request.user.is_staff: # cant update posts if its a different user ... but if he is staff he can
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
    else:
        raise Http404("cant update wrong user")

def post_delete(request, id):

    if not request.user.is_authenticated:
        raise Http404()

    deleted_post = get_object_or_404(Post, id = id)

    if deleted_post.user == request.user:
        deleted_post.delete()
        return redirect('post:index')
    else:
        raise Http404("cant delete wrong user")

def delete_post_adminpanel(request, id):

    if not request.user.is_authenticated:
        raise Http404()

    deleted_post = get_object_or_404(Post, id = id)

    if request.user.is_staff:
        deleted_post.delete()
        return redirect('/accounts/admin_panel/posts')

def delete_contact_adminpanel(request, id):

    if not request.user.is_authenticated:
        raise Http404()

    deleted_contact = get_object_or_404(ContactInfo, id = id)

    if request.user.is_staff:
        deleted_contact.delete()
        return redirect('/accounts/admin_panel/contacts')

def contact_us(request):
    form = ContactusForm(request.POST or None)
    if form.is_valid():
        contact = form.save(commit=False)
        contact.user = request.user
        contact.save()
        return redirect('/')
    return render(request, "info/contact.html", {'form':form, 'title':'Info'})