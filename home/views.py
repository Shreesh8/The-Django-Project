from django.shortcuts import render
from post.models import Post
from django.db.models import Count
from accounts.forms import LoginForm

# Create your views here.
def home_view(request):

    if request.user.is_authenticated:
        name = {"name" : request.user.username}
    else:
        name = {"name" : "Guest",}

    popular_posts = Post.objects.annotate(num_comments=Count('comments')).order_by('-num_comments')[:3]

    context = {
        "popular_posts":popular_posts,
        "account":name
    }


    return render(request, "home_templates/home.html",context)
