from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect,Http404
from post.models import Post, UserUpvote
from django.db.models import Count
from accounts.forms import LoginForm
from django.db.models import F

# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        post_list = Post.objects.all()

        post_ids = post_list.values_list('id', flat=True)

        upvoted_qs = UserUpvote.objects.filter(user=request.user, post_id__in=post_ids)
        upvoted_posts = set(upvoted_qs.values_list('post_id', flat=True))

        if request.user.is_authenticated:
            name = {"name" : request.user.username}
        else:
            name = {"name" : "Guest",}

        popular_posts = Post.objects.annotate(num_comments=Count('post_views')).order_by('-post_views')[:3]

        context = {
            "popular_posts": popular_posts,
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