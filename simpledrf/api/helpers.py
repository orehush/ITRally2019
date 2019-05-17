from django.core.exceptions import ObjectDoesNotExist
from django.db.models import OneToOneField, OneToOneRel


def get_child_related(model):

    related_objects = [
        f for f in model._meta.get_fields()
        if isinstance(f, OneToOneRel)]

    return [
        rel for rel in related_objects
        if isinstance(rel.field, OneToOneField)
        and issubclass(rel.field.model, model)
        and model is not rel.field.model
    ]


def get_child_models(model):
    related = get_child_related(model)
    return [rel.field.model for rel in related]


def get_child_related_name(model):
    related = get_child_related(model)
    return [rel.get_accessor_name() for rel in related]


def get_sub_obj(obj):
    related = get_child_related_name(obj.__class__)

    for child in related:
        try:
            return getattr(obj, child)
        except ObjectDoesNotExist:
            continue

    return obj
