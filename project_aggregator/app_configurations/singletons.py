from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class SingletonModelSettings(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except ObjectDoesNotExist:
            return cls()
