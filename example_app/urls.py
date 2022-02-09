from django.urls import path

from django_distill import distill_path

from . import views
from .tag_specifics import ALL_TAGS


def get_all_tags():
    for key in ALL_TAGS:
        yield ({"tag_name": key})


urlpatterns = [
    distill_path("", views.index, name="index", distill_file="django-dsfr/index.html"),
    distill_path(
        "tags/",
        views.tags_index,
        name="tags_index",
        distill_file="django-dsfr/tags/index.html",
    ),
    distill_path(
        "tags/<slug:tag_name>/",
        views.page_tag,
        name="page_tag",
        distill_func=get_all_tags,
    ),
    distill_path(
        "forms/",
        views.AuthorCreateView.as_view(),
        name="forms",
        distill_file="django-dsfr/example-form.html",
    ),
]
