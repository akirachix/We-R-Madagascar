from django.db import models

from django.utils import timezone

class FlightRequest(models.Model):
    # BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
    # STATUS_CHOICES = (
    #     ('Pending','Pending'),
    #     ('Scheduled', 'Scheduled'),
    #     ('Delayed','Delayed')
    # )

    UID_planning= models.CharField(max_length=300)
    pays= models.CharField(max_length=300)
    region= models.CharField(max_length=300)
    district= models.CharField(max_length=300)
    commune=models.CharField(max_length=300)
    Centre= models.CharField(max_length=300)
    type_centre= models.CharField(max_length=300)
    UID_centre = models.CharField(max_length=300)
    code_vol= models.CharField(max_length=300)
    date_planning= models.CharField(max_length=300)
    heure_planning=models.CharField(max_length=300)
    situation_vol=models.CharField(max_length=300)
    situation_livraison=models.CharField(max_length=300)
    motif_report=models.CharField(max_length=300)
    motif_annulation=models.CharField(max_length=300)
    cancel=models.CharField(max_length=6)
    project=models.CharField(max_length=300)
 




    def __str__(self):
        return self.date_planning
