from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from zinnia.models.entry import Entry
from zinnia.admin.entry import EntryAdmin



class EntryEventAdmin(EntryAdmin):
  # In our case we put the gallery field
  # into the 'Content' fieldset
    
    
    fieldsets = EntryAdmin.fieldsets + (('Dagsetning viðburðar', {
        'fields': ('date_from', 'date_to')
        }),)
    
# Unregister the default EntryAdmin
# then register the EntryGalleryAdmin class
admin.site.unregister(Entry)
admin.site.register(Entry, EntryEventAdmin)