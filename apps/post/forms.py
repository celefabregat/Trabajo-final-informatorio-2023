from django import forms
from .models import Comentario, Post, Categoria

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields =["texto"]

class CrearPostForm(forms.ModelForm):
    categoria=forms.ModelChoiceField(queryset=Categoria.objects.all(), empty_label="seleccionar categoria")
    class Meta:
        model = Post
        fields = ["titulo","subtitulo","texto","activo","categoria","imagen"]

class NuevaCategoriaForm(forms.ModelForm):
    class Meta: 
        model= Categoria
        fields = "__all__"