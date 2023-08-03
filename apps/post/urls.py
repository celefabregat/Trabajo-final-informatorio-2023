from django.urls import path
from apps.post import views

app_name = "apps.post"

urlpatterns = [
    path("posts/",views.PostListView.as_view(), name ="posts"),
    path("posts/<int:id>/", views.PostDetailView.as_view(), name= "post_individual"),
    # path("posts/<int:id>/delete", views.PostDeleteView.as_view(), name= "post_individual"),
    # path("posts/<int:id>/update", views.PostUpdateView.as_view(), name= "post_individual"),
    # path("posts/create", views.PostCreateView.as_view(), name= "post_individual"),
    # path("delete_coment/<int:id>/", views.delete_coment, name= "delete_coment"),
    # path("editar_coment/<int:id>/", views.editar_coment, name= "editar_coment"),
    path("post/", views.PostCreateView.as_view(), name="crear_post"),
    path("post/categoria", views.CategoriaCreateView.as_view(), name="crear_categoria"),
    path("categoria", views.CategoriaListView.as_view(), name="categoria_list"),
    path("categoria/<int:pk>/delete/", views.CategoriaDeleteView.as_view(), name="categoria_delete"),
    path("post/<int:pk>/modificar/", views.PostUpdateView.as_view(), name="post_update"),
    path("post/<int:pk>/eliminar/", views.PostDeleteView.as_view(), name="post_delete"),
    path("comentario/<int:pk>/editar/", views.ComentarioUpdateView.as_view(), name="comentario_editar"),
    path("comentario/<int:pk>/eliminar/", views.ComentarioDeleteView.as_view(), name="comentario_eliminar"),

    
]