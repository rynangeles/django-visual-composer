from django.db import models
from django.contrib.flatpages.models import FlatPage

from sites_flatpage.utils import uploaded_banner_handler


class ExtendedFlatPage(FlatPage):

    banner_thumbnail = models.FileField(upload_to=uploaded_banner_handler, null=True, blank=True)
    banner = models.FileField(upload_to=uploaded_banner_handler, null=True, blank=True, \
    	help_text="Upload image not less than 1200 x 600 pixels, but not greater than 2 megabytes")

