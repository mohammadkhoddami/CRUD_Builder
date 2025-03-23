import os
from django.conf import settings
from django.urls import path
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.forms import modelform_factory

APP_TEMPLATE_DIR = os.path.join(settings.BASE_DIR, "crud_builder", "templates", "crud_builder")

TEMPLATE_CONTENTS = {
    "list": """{% extends "base.html" %}

{% block content %}
<h1>لیست {{ model_name_plural }}</h1>
<ul>
    {% for object in object_list %}
        <li><a href="{{ object.get_absolute_url }}">{{ object }}</a></li>
    {% endfor %}
</ul>
<a href="{% url app_label|add:':'|add:model_lower|add:'_create' %}">ایجاد جدید</a>
{% endblock %}""",

    "detail": """{% extends "base.html" %}

{% block content %}
<h1>جزئیات {{ object }}</h1>
<p>{{ object }}</p>
<a href="{% url app_label|add:':'|add:model_lower|add:'_update' object.pk %}">ویرایش</a>
<a href="{% url app_label|add:':'|add:model_lower|add:'_delete' object.pk %}">حذف</a>
{% endblock %}""",

    "form": """{% extends "base.html" %}

{% block content %}
<h1>فرم {{ model_name }}</h1>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">ذخیره</button>
</form>
{% endblock %}""",

    "delete": """{% extends "base.html" %}

{% block content %}
<h1>حذف {{ object }}</h1>
<p>آیا مطمئن هستید که می‌خواهید {{ object }} را حذف کنید؟</p>
<form method="post">
    {% csrf_token %}
    <button type="submit">بله، حذف کن</button>
</form>
{% endblock %}""",
}

def create_templates_if_not_exist(model_name):
    """
    Creates default CRUD templates if they do not exist.
    """
    if not os.path.exists(APP_TEMPLATE_DIR):
        os.makedirs(APP_TEMPLATE_DIR)

    for view_type, content in TEMPLATE_CONTENTS.items():
        template_path = os.path.join(APP_TEMPLATE_DIR, f"{model_name}_{view_type}.html")
        if not os.path.exists(template_path):
            with open(template_path, "w", encoding="utf-8") as f:
                f.write(content)

def generate_crud(model, app_name):
    """
    Generates CRUD views and URL patterns for a given Django model.
    """

    model_name = model.__name__.lower()
    model_form = modelform_factory(model, fields="__all__")

    create_templates_if_not_exist(model_name)

    ModelListView = type(
        f"{model.__name__}ListView",
        (ListView,),
        {
            "model": model,
            "template_name": f"crud_builder/{model_name}_list.html",
            "extra_context": {
            "model_name": model.__name__,
            "model_name_plural": model.__name__ + "s",
            "app_label": app_name,
            "model_lower": model_name,
        }
        }
    )

    ModelDetailView = type(
        f"{model.__name__}DetailView",
        (DetailView,),
        {
            "model": model,
            "template_name": f"crud_builder/{model_name}_detail.html",
            "extra_context": {
            "model_name": model.__name__,
            "model_name_plural": model.__name__ + "s",
            "app_label": app_name,
            "model_lower": model_name,
        }
        }
    )

    ModelCreateView = type(
        f"{model.__name__}CreateView",
        (CreateView,),
        {
            "model": model,
            "form_class": model_form,
            "template_name": f"crud_builder/{model_name}_form.html",
            "success_url": f"/{app_name}/{model_name}/",
            "extra_context": {
            "model_name": model.__name__,
            "model_name_plural": model.__name__ + "s",
            "app_label": app_name,
            "model_lower": model_name,
        }
        }
    )

    ModelUpdateView = type(
        f"{model.__name__}UpdateView",
        (UpdateView,),
        {
            "model": model,
            "form_class": model_form,
            "template_name": f"crud_builder/{model_name}_form.html",
            "success_url": f"/{app_name}/{model_name}/",
            "extra_context": {
            "model_name": model.__name__,
            "model_name_plural": model.__name__ + "s",
            "app_label": app_name,
            "model_lower": model_name,
        }
        }
    )

    ModelDeleteView = type(
        f"{model.__name__}DeleteView",
        (DeleteView,),
        {
            "model": model,
            "template_name": f"crud_builder/{model_name}_delete.html",
            "success_url": f"/{app_name}/{model_name}/",
            "extra_context": {
            "model_name": model.__name__,
            "model_name_plural": model.__name__ + "s",
            "app_label": app_name,
            "model_lower": model_name,
        }
        }
    )

    urlpatterns = [
        path(f"{model_name}/", ModelListView.as_view(), name=f"{model_name}_list"),
        path(f"{model_name}/<int:pk>/", ModelDetailView.as_view(), name=f"{model_name}_detail"),
        path(f"{model_name}/create/", ModelCreateView.as_view(), name=f"{model_name}_create"),
        path(f"{model_name}/<int:pk>/update/", ModelUpdateView.as_view(), name=f"{model_name}_update"),
        path(f"{model_name}/<int:pk>/delete/", ModelDeleteView.as_view(), name=f"{model_name}_delete"),
    ]

    return urlpatterns
