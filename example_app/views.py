from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_safe
from dsfr.utils import generate_summary_items

from .tag_specifics import (
    ALL_IMPLEMENTED_TAGS,
    IMPLEMENTED_TAGS,
    EXTRA_TAGS,
    NOT_YET_IMPLEMENTED_TAGS,
)

from django.views.generic import CreateView
from django.http import HttpResponse
from .forms import AuthorCreateForm, BookCreateFormSet, BookCreateFormHelper
from .models import Author, Book

# Used by the module = getattr(globals()["dsfr_tags"], f"dsfr_{tag_name}") line

from dsfr.templatetags import dsfr_tags


def init_payload(page_title: str, links: list = []):
    # Returns the common payload passed to most pages:
    # title: the page title
    # breadcrumb_data: a dictionary used by the page's breadcrumb
    # skiplinks: a list used by the page's skiplinks item

    breadcrumb_data = {
        "current": page_title,
        "links": links,
        "root_dir": "/django-dsfr",
    }

    skiplinks = [
        {"link": "#content", "label": "Contenu"},
        {"link": "#fr-navigation", "label": "Menu"},
    ]

    return {
        "title": page_title,
        "breadcrumb_data": breadcrumb_data,
        "skiplinks": skiplinks,
    }


@require_safe
def index(request):
    payload = init_payload("Accueil")

    payload["summary_data"] = generate_summary_items(
        [
            "Installation",
            "Utilisation",
            "Développement",
            "Notes",
        ]
    )

    return render(request, "example_app/index.html", payload)


@require_safe
def tags_index(request):
    payload = init_payload("Composants")
    payload["implemented_tags"] = dict(
        sorted(IMPLEMENTED_TAGS.items(), key=lambda k: k[1]["title"])
    )
    payload["extra_tags"] = dict(
        sorted(EXTRA_TAGS.items(), key=lambda k: k[1]["title"])
    )
    payload["not_yet"] = dict(
        sorted(NOT_YET_IMPLEMENTED_TAGS.items(), key=lambda k: k[1]["title"])
    )
    return render(request, "example_app/tags_index.html", payload)


@require_safe
def page_tag(request, tag_name):

    if tag_name in ALL_IMPLEMENTED_TAGS:
        current_tag = ALL_IMPLEMENTED_TAGS[tag_name]
        payload = init_payload(
            current_tag["title"],
            links=[{"url": reverse("tags_index"), "title": "Composants"}],
        )
        payload["tag_name"] = tag_name

        if tag_name == "pagination":
            sample_content = list(range(0, 100))
            paginator = Paginator(sample_content, 10)
            payload["page_obj"] = paginator.get_page(4)

        module = getattr(globals()["dsfr_tags"], f"dsfr_{tag_name}")
        payload["tag_comment"] = module.__doc__

        if "sample_data" in current_tag:
            payload["sample_data"] = current_tag["sample_data"]

        if "doc_url" in current_tag:
            payload["doc_url"] = current_tag["doc_url"]

        sidemenu_items = []
        for key in ALL_IMPLEMENTED_TAGS.keys():
            sidemenu_items.append(
                {"label": key, "link": reverse("page_tag", kwargs={"tag_name": key})}
            )

        payload["side_menu"] = {"title": "Composants", "items": sidemenu_items}
        return render(request, f"example_app/page_tag.html", payload)
    else:
        payload = init_payload("Non implémenté")
        payload["not_yet"] = {
            "text": "Le contenu recherché n'est pas encore implémenté",
            "title": "Non implémenté",
        }
        return render(request, f"example_app/not_yet.html", payload)


@require_safe
def page_tests(request):
    payload = init_payload("Tests")

    payload["side_menu"] = {
        "title": "Menu",
        "items": [
            {
                "label": "Components",
                "items": [
                    {
                        "label": "Alert",
                        "link": reverse("page_tag", kwargs={"tag_name": "alert"}),
                    },
                    {
                        "label": "Breadcrumb",
                        "link": reverse("page_tag", kwargs={"tag_name": "breadcrumb"}),
                    },
                ],
            },
            {
                "label": "Other pages",
                "items": [
                    {
                        "label": "An intermediary menu",
                        "items": [
                            {"label": "Some page", "link": "/"},
                        ],
                    },
                    {
                        "label": "Another intermediary menu",
                        "items": [
                            {"label": "A sample page", "link": "#"},
                            {"label": "Another sample page", "link": "#"},
                            {
                                "label": "Test page",
                                "link": reverse("page_tests"),
                            },
                        ],
                    },
                ],
            },
        ],
    }

    payload["callout_1"] = {
        "text": "This callout item has a normal button",
        "title": "Callout with actionable button",
        "icon_class": "fr-fi-alert-line",
        "button": {
            "onclick": "alert('button being a button')",
            "label": "button label",
            "extra_classes": "fr-btn--secondary",
        },
    }

    payload["callout_2"] = {
        "text": "This callout item has a call-to-action link",
        "title": "Callout with call to action link",
        "icon_class": "fr-fi-external-link-line",
        "button": {
            "label": "button label",
            "url": "https://www.systeme-de-design.gouv.fr/",
            "extra_classes": "fr-btn--secondary",
        },
    }

    return render(request, "example_app/tests.html", payload)


class AuthorCreateView(CreateView):
    model = Author
    form_class = AuthorCreateForm
    formset = BookCreateFormSet
    template_name = 'example_app/example-form.html'
    
    def get(self, request, *args, **kwargs):
        instance = None
        try :
            if self.object:
                instance = self.object
        except Exception:
            self.object=None
            
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = BookCreateFormSet(instance=instance)
        book_formhelper = BookCreateFormHelper()

        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )
    
    def get_context_data(self, **kwargs):
        context = super(AuthorCreateView, self).get_context_data(**kwargs)
        book_formhelper = BookCreateFormHelper()
        
        instance = None
        try:
            if self.object:
                instance = self.object
        except Exception:
            self.object=None
    
        if self.request.POST:
            context['form'] = self.form_class(self.request.POST)
            context['formset'] = BookCreateFormSet(self.request.POST, self.request.FILES, instance=instance)
            context['book_formhelper'] = book_formhelper
        else:
            context['form'] = self.form_class()
            context['formset'] = BookCreateFormSet(instance=instance)
            context['book_formhelper'] = book_formhelper
        
        context['btn_submit'] = {
                                    "label": "Soumettre",
                                    "onclick": "",
                                    "type":"submit",
                                }
        return context
    
    def post(self, request, *args, **kwargs):
        instance = None
        try:
            if self.object:
                instance = self.object
        except Exception:
            self.object=None

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = BookCreateFormSet(self.request.POST, self.request.FILES, instance=instance)
        
        if (form.is_valid() and formset.is_valid()):
            return self.form_valid(form, formset)
        return self.form_invalid(form, formset)
    
    def form_valid(self, form, formset):
        """
        Called if all forms are valid. Creates a Author instance along
        with associated books and then redirects to a success page.
        """
        self.object = form.save()
        formset.instance = self.object
        formset.save()

        return HttpResponse('Success')

    def form_invalid(self, form, formset):
        """
        Called if whether a form is invalid. Re-renders the context
        data with the data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )
