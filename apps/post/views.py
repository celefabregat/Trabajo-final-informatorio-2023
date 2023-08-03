# from django.shortcuts import render
from typing import Any, Dict

from django.db.models.query import QuerySet
from django.db.models.functions import Lower
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from .models import Post, Comentario, Categoria
from .forms import ComentarioForm,CrearPostForm, NuevaCategoriaForm
from django.views.generic import ListView, DetailView, CreateView,UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib import messages

#Vista basada en funciones
# def posts(request):
#     posts =Post.objects.all()
#     print(posts)
#     return render(request, "posts.html", {"posts" : posts})

#Vista basada en clases
class PostListView(ListView):
    model = Post
    template_name = "posts/posts.html"
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        orden = self.request.GET.get("orden")
        if orden == "reciente":
            queryset = queryset.order_by("-fecha")
        elif orden== "antiguo":
            queryset = queryset.order_by("fecha")
        elif orden == "alfabeticoA-Z":
            queryset = queryset.annotate(titulo_lower=Lower("titulo")).order_by("titulo_lower")
        elif orden == "alfabeticoZ-A":
            queryset = queryset.annotate(titulo_lower=Lower("titulo")).order_by("-titulo_lower")

        categoria_seleccionada = self.request.GET.get("categoria")
        if categoria_seleccionada:
            categoria = get_object_or_404(Categoria, nombre=categoria_seleccionada)
            queryset = queryset.filter(categoria=categoria)
        return queryset  


        # elif orden == "categoria":
        #     print(self, "================")
        #     queryset = queryset.filter(categoria_id=self.kwargs["id"])
        # return queryset
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["orden"] = self.request.GET.get("orden", "reciente")
        context["categorias"] = Categoria.objects.all()
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_individual.html"
    context_object_name = "posts"
    pk_url_kwarg = "id"
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["post"] = Post.objects
        context["form"] = ComentarioForm()
        context["comentarios"] = Comentario.objects.filter(posts_id=self.kwargs["id"])
        return context
    
    def post(self, request, *args, **kwargs): 
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.posts_id = self.kwargs["id"]
            comentario.save()
            return redirect("apps.post:post_individual", id=self.kwargs["id"])
        else:
            context = self.get_context_data(**kwargs)
            context["form"] = form
            return self.render_to_response(context)

class PostCreateView(LoginRequiredMixin,CreateView):
    model= Post
    form_class = CrearPostForm
    template_name = "posts/crear_post.html"
    success_url = reverse_lazy("apps.post:posts")

    def form_valid(self, form):
        post = form.save(commit=False)
        post.usuario = self.request.user
        post.save()
        return super().form_valid(form)
    

    def get_success_url(self):
        messages.success(self.request, "Se ha creado un post con exito!")
        
        return reverse_lazy("apps.post:posts")

class CategoriaCreateView(LoginRequiredMixin,CreateView):
    model= Categoria
    form_class = NuevaCategoriaForm
    template_name = "posts/crear_categoria.html"

    def get_success_url(self):
        messages.success(self.request, "¡La categoría ha sido agregada con éxito!")
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        else:
            return reverse_lazy("apps.post:crear_post")
 
class CategoriaListView(ListView):
    model = Categoria
    template_name = "posts/categoria_list.html"
    context_object_name = "categoria"

class CategoriaDeleteView(LoginRequiredMixin,DeleteView):
    model = Categoria
    template_name = 'posts/categoria_confirm_delete.html'
    success_url = reverse_lazy('apps.post:categoria_list')

    def get_success_url(self):
        messages.success(self.request, "Se ha borrado una categoria!")
        
        return reverse_lazy("apps.post:posts")
    

class PostUpdateView(LoginRequiredMixin,UpdateView):
    model = Post
    form_class = CrearPostForm
    template_name = 'posts/modificar_post.html'
    success_url = reverse_lazy('apps.post:posts')

    def get_success_url(self):
        messages.success(self.request, "Se ha editado un post con exito!")
        
        return reverse_lazy("apps.post:posts")



class PostDeleteView(DeleteView):
   model = Post
   template_name = "posts/eliminar_post.html"
   success_url = reverse_lazy('apps.post:posts')

   def get_success_url(self):
        messages.warning(self.request, "Se ha borrado un post")
        
        return reverse_lazy("apps.post:posts")

class ComentarioCreateView(LoginRequiredMixin, CreateView):

    model = Comentario
    form_class = ComentarioForm
    template_name = "comentario/agregarComentario.html"
    success_url = "comentario/comentarios"

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.posts_id = self.kwargs["posts_id"]
        return super().form_valid(form)
    
    def get_success_url(self):
        messages.success(self.request, "Has creado un comentario")
        return reverse('apps.post:post_individual', args=[self.object.posts.id])

class ComentarioUpdateView(LoginRequiredMixin, UpdateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'comentario/comentario_form.html'
    def get_success_url(self):
        messages.success(self.request, "Has editado un comentario")
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('apps.post:post_individual', args=[self.object.posts.id])

class ComentarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Comentario
    template_name = 'comentario/comentario_confirm_delete.html'
    def get_success_url(self):
        messages.warning(self.request, "Has borrado un comentario")
        return reverse('apps.post:post_individual', args=[self.object.posts.id])

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     post_id = kwargs.get('post_id')
    #     context['post_id'] = post_id
    #     return context


# Vista acerca de nosotros

def acerca_de(request):
    template = 'About/acerca_de_nosotros.html'
    context= {}
    return render(request, template, context)