from django.db import models

from auditable.models import Auditable

from .Credential import Credential


class Name(Auditable):
    credential = models.ForeignKey(Credential, related_name="names")
    text = models.TextField(null=True)
    language = models.TextField(null=True)

    class Meta:
        db_table = "name"
