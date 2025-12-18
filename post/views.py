from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect, Http404, HttpResponse
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.urls import reverse
from .models import Post, UserUpvote, UserReport
from django.contrib.auth.models import User
from .forms import PostForm, CommentForm
from admin_panel.forms import ContactusForm
from django.contrib import messages
from django.db.models import Q
from django.db.models import F

from django.core.paginator import Paginator
from django.conf import settings
#from django.utils.text import slugify

class Info():
    def contact_us(request):
        return render(request, "info/contact.html")

    def about_us(request):
        return render(request, "info/about.html")

class BlogListPosts():

    def posts_paginator(self, request):
        post_list = Post.objects.all()
        query = request.GET.get("q")

        if query: # Search query in header
            post_list = post_list.filter(
                Q(title__icontains=query) |
                Q(desc__icontains=query)|
                Q(user__first_name__icontains=query)|
                Q(user__last_name__icontains=query)).distinct()
        paginator = Paginator(post_list, 9)  # Show 9 posts per page.
        page = request.GET.get("page")
        return paginator.get_page(page)
        
    def fetch_post_data(self, request, model): # Fetches upvotes and reports
        post_list = Post.objects.all()
        post_ids = post_list.values_list('id', flat=True)

        obj_qs = model.objects.filter(user=request.user, post_id__in=post_ids)
        return set(obj_qs.values_list('post_id', flat=True))

    def post_get_upvotes(self,request):
        return self.fetch_post_data( request,UserUpvote)
    
    def post_get_reports(self,request):
        return self.fetch_post_data(request,UserReport)
    
    def list_posts(self,request):
        posts = self.posts_paginator(request)
        upvotes = self.post_get_upvotes(request)
        reports = self.post_get_reports(request)
        
        context = {
            "posts" : posts,
            "upvoted_posts" : upvotes,
            "reported_posts" : reports,
            "debug": settings.DEBUG,
        }

        suffix = ""
        for each_page in range(len(posts)):
            if len(posts[each_page].title) > 25:
                suffix = "..."
            else:
                suffix = ""
            posts[each_page].title = posts[each_page].title[:25] + suffix

        return render(request, "post_templates/index.html", context)

class PostActions():

    def upvote_in_blog(self, request, id):
        self.upvote_post(request, id)
        page = request.GET.get("page", 1)
        return redirect(f"{reverse('post:index')}?page={page}")

    def upvote_in_detail(self, request, id):
        post = self.upvote_post(request, id)
        return redirect(post.get_absolute_url())

    def upvote_post(self, request, id):
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
        
        return post

def post_detail(request, id):
    post = get_object_or_404(Post, id = id)
    post_list = Post.objects.all()

    post_ids = post_list.values_list('id', flat=True)

    upvoted_qs = UserUpvote.objects.filter(user=request.user, post_id__in=post_ids)
    reported_qs = UserReport.objects.filter(user=request.user, post_id__in=post_ids)

    upvoted_posts = set(upvoted_qs.values_list('post_id', flat=True))
    reported_posts = set(reported_qs.values_list('post_id', flat=True))

    post_views = Post.objects.filter(id=post.id).update(post_views=F("post_views") + 1)

    form = CommentForm(request.POST or None) # handles comment logic
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
        print("commented")
        return HttpResponseRedirect(post.get_absolute_url())
    
    content = {
        "post" : post,
        "form" : form,
        "upvoted_posts" : upvoted_posts,
        "reported_posts" : reported_posts,
        "post_views": post_views,
    }
    
    if post.user_html:
        # Read html content
        html_path = post.user_html.path
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        final_html = html_content

        if post.user_css: # Adds css and js files straight into one html file so i dont have to bother with multiple files
            css_path = post.user_css.path
            with open(css_path, 'r', encoding='utf-8') as f:
                css_content = f.read()
            final_html = final_html.replace('</head>', f'<style>{css_content}</style>\n</head>')

        if post.user_js:
            js_path = post.user_js.path
            with open(js_path, 'r', encoding='utf-8') as f:
                js_content = f.read()
            final_html = final_html.replace('</body>', f'<script>{js_content}</script>\n</body>')
        
        # Displays the html page
        return HttpResponse(final_html, content_type='text/html')

    return render(request, "post_templates/detail.html", content)

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

def post_report(request,id):
    if not request.user.is_authenticated:
        raise Http404()

    post = get_object_or_404(Post, id = id)


    already_reported = UserReport.objects.filter(user = request.user,post=post)

    if already_reported.exists():
        already_reported.delete()
        Post.objects.filter(id=post.id).update(reports=F("reports") - 1)
    else:
        UserReport.objects.create(user = request.user,post=post)
        Post.objects.filter(id=post.id).update(reports=F("reports") + 1)

    return redirect('post:index')

def post_delete(request, id):

    if not request.user.is_authenticated:
        raise Http404()

    deleted_post = get_object_or_404(Post, id = id)

    if deleted_post.user == request.user:
        deleted_post.delete()
        return redirect('post:index')
    else:
        raise Http404("cant delete wrong user")

def contact_us(request):
    form = ContactusForm(request.POST or None)
    if form.is_valid():
        contact = form.save(commit=False)
        contact.user = request.user
        contact.save()
        return redirect('/')
    return render(request, "info/contact.html", {'form':form, 'title':'Info'})