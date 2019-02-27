from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

# @receiver(post_save, sender=User)
# def createUserProfile(sender, **kwargs):
# 	if kwargs['created']:
# 		user = kwargs['instance']
# 		UserProfile.objects.create()
