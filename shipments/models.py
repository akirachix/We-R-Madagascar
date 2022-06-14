from django.db import models
from django.db.models.signals import post_save
import datetime as dt

from django.utils import timezone
from bulk_update_or_create import BulkUpdateOrCreateQuerySet


# STATUS_CHOICES = (
#  ('Pending','Pending'),
#  ('Processed', 'Processed'),
#  ('Dispatched','Dispatched'),
#  ('Delayed','Delayed'),
#  ('Completed','Completed'),

# )
# # Create your models here.
# class Schedule(models.Model):
#     UID_quantification_planning = models.CharField(max_length=7)
#     UID_planning = models.CharField(max_length=20)
#     product_type = models.CharField(max_length=20)
#     units = models.CharField(max_length=5)
#     delivery_date = models.DateField(default=timezone.now)
#     take_of_time= models.TimeField(default=dt.time(00, 00))
#     delivery_time = models.TimeField(default=dt.time(00, 00))
#     status = models.CharField(max_length=30, choices=STATUS_CHOICES,default='dispatched')
#     destination = models.CharField(max_length=20)
#     delay_reasons= models.CharField(max_length=20,default='Air Traffic')

           
           
         
      


    # def __str__(self):
    #     return self.status

class Schedules(models.Model):
    
    UID_quantification_planning = models.CharField(max_length=100)
    UID_planning = models.CharField(max_length=100)
    type_produit = models.CharField(max_length=100)
    produit = models.CharField(max_length=100)
    UID_produit = models.CharField(max_length=100)
    livraison_produit = models.CharField(max_length=100)
    quantite_prevu = models.CharField(max_length=100)
    quantite_envoyee = models.CharField(max_length=100)
    quantite_recu = models.CharField(max_length=100)
    quantite_intact = models.CharField(max_length=100)
    quantite_abime = models.CharField(max_length=100)
    quantite_perdu = models.CharField(max_length=100)
    explication = models.CharField(max_length=100)
    objects = BulkUpdateOrCreateQuerySet.as_manager()


    def __str__(self):
        return self.UID_produit
        

