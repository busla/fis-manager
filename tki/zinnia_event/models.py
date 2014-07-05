from django.db import models
from zinnia.models_bases.entry import AbstractEntry



class EntryEvent(AbstractEntry):
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)

    
    class Meta(AbstractEntry.Meta):
        abstract = True

