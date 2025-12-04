from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect,Http404
from post.models import Post, UserUpvote
from django.db.models import Count
from accounts.forms import LoginForm
from django.db.models import F
from django.utils import timezone
from datetime import timedelta
from calendar import monthrange

def popular_post_filter_top_month(request):
    return home_view(request, "top_month")

def popular_post_filter_top_day(request):
    return home_view(request, "top_day")

def home_view(request,filter_option = "default"): # Top of all time filter is default
    if request.user.is_authenticated:
        post_list = Post.objects.all()

        post_ids = post_list.values_list('id', flat=True)

        upvoted_qs = UserUpvote.objects.filter(user=request.user, post_id__in=post_ids)
        upvoted_posts = set(upvoted_qs.values_list('post_id', flat=True))

        if request.user.is_authenticated:
            name = {"name" : request.user.username}
        else:
            name = {"name" : "Guest",}

        if filter_option == "top_day":
            last_24_hours = timezone.now() - timedelta(days=1)
            popular_posts = Post.objects.filter(date__gte=last_24_hours).annotate(Count('post_views')).order_by('-post_views')[:3]
        elif filter_option == "top_month":
            last_30_days = timezone.now() - timedelta(days=30)
            popular_posts = Post.objects.filter(date__gte=last_30_days).annotate(Count('post_views')).order_by('-post_views')[:3]
        else: # Top of All Time
            popular_posts = Post.objects.annotate(Count('post_views')).order_by('-post_views')[:3]

        context = {
            "popular_posts": popular_posts,
            "filter_option": filter_option,
            "account": name,
            "upvoted_posts": upvoted_posts,
        }

        return render(request, "home_templates/home.html",context)
    else:
        return redirect('accounts/login')

def upvote_post(request, id):
    
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
    return redirect("/")

def post_delete_home(request, id):

    if not request.user.is_authenticated:
        raise Http404()

    deleted_post = get_object_or_404(Post, id = id)

    if deleted_post.user == request.user:
        deleted_post.delete()
        return redirect('/')
    else:
        raise Http404("cant delete wrong user")