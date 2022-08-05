from email.policy import default
from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from django.core.signals import request_finished
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    deadlineDate = models.DateTimeField(default=True,null=True,blank=True)

    # @receiver(post_save, sender = )
    # def created(Task, instance, created, **kwargs):
    #     print(created)
    #     print(instance)
    #     if created:
    #         ActivityFeed.objects.all.create(action=instance)
    #     instance.save()
            
    # @receiver(post_delete, sender = )
    # def deleted(, instance, deleted, **kwargs):
    #     if deleted:
    #         ActivityFeed.objects.all.deleted(action=instance)
    #         instance.save()
    

    def __str__(self):
        return self.title

    class Meta:
        ordering=['complete']


class ActivityFeed(models.Model):

    task = models.ForeignKey(Task,on_delete=models.CASCADE,null=False,blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    action = models.CharField(max_length=255,null=False,blank=False)
    created_on = models.DateField(auto_now=True)

    def __str__(self):
        return

