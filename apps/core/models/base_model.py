from django.db import models
from django.db.models import QuerySet
from django.db.models.manager import BaseManager as DjangoBaseManager
from django.utils.translation import gettext_lazy as _

class BaseQuerySet(QuerySet):
    def delete(self):
        self.update(is_deleted=True)

    def hard_delete(self):
        super().delete()


class BaseManager(DjangoBaseManager):
    def get_queryset(self):
        return BaseQuerySet(self.model).filter(is_deleted=False)

    def hard_delete(self):
        self.get_queryset().hard_delete()

    def deleted(self):
        return BaseQuerySet(self.model).filter(is_deleted=True)

    def all_objects(self):
        return BaseQuerySet(self.model)

    def get_by_id(self, id):
        return self.get_queryset().get(id=id)

    def get_by_id_or_raise(self, id):
        return self.get_queryset().get(id=id)


    def get_or_raise(self, **kwargs):
        return self.get_queryset().get(**kwargs)


class BaseModel(models.Model):
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    # objects = BaseManager()
    # all_objects = BaseManager()

    class Meta:
        abstract = True

    # def delete(self):
    #     self.is_deleted = True
    #     self.save()

    # def hard_delete(self):
    #     super().delete()

    # def restore(self):
    #     self.is_deleted = False
    #     self.save()

    # def save(self, *args, **kwargs):
    #     if self.is_deleted:
    #         self.is_deleted = False
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.__class__.__name__} object ({self.id})"

    def __repr__(self):
        return f"{self.__class__.__name__} object ({self.id})"

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.id == self.id
