from django.shortcuts import render
from apps.post.models import Post

def index(request):
    post_recientes = Post.objects.all().order_by("-fecha")[0:3]
    contexto = {
        "post_recientes": post_recientes
    }
    return render(request, "index.html",contexto)

