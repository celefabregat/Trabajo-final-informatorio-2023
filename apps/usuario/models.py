from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# Create your models here.
class Usuario(models.Model):
    usuario= models.OneToOneField(User,on_delete=models.CASCADE)
    imagen= models.ImageField(upload_to= "usuario", default= "static/usuariodefault.png")
    es_colaborador = models.BooleanField(default= False)

@receiver(post_save, sender=User)
def crear_actualizar_usuario(sender, instance, created, **kwargs):
    if created:
        Usuario.objects.create(usuario=instance)
    else:
        try:
            instance.usuario.save()
        except Usuario.DoesNotExist:
            pass

        
    


    