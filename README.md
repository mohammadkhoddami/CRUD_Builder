# CRUD Builder

## 📌 Introduction
`crud_builder` is a Django package that **automatically generates CRUD views and templates** for your Django models. Just install the package, add it to `INSTALLED_APPS`, and let it handle the repetitive CRUD work for you!

## 🚀 Installation
Install the package using pip:
```sh
pip install crud-builder
```

Then, add `crud_builder` to your `INSTALLED_APPS` in `settings.py`:
```python
INSTALLED_APPS = [
    ...,
    "crud_builder",  # Enable the package
]
```

## 🛠 Usage
### 1️⃣ **Register the CRUD views for your models**
In your `urls.py`, import and use the `generate_crud_urls` function:
```python
from django.urls import path, include
from crud_builder.generators import generate_crud_urls
from myapp.models import MyModel

urlpatterns = [
    path("mymodel/", include(generate_crud_urls(MyModel))),
]
```
This will automatically create URLs for listing, creating, updating, and deleting `MyModel` objects.

### 2️⃣ **Access the CRUD Views**
Once the URLs are registered, you can access them via:
- `http://127.0.0.1:8000/mymodel/` (List view)
- `http://127.0.0.1:8000/mymodel/create/` (Create view)
- `http://127.0.0.1:8000/mymodel/<id>/` (Detail view)
- `http://127.0.0.1:8000/mymodel/<id>/update/` (Update view)
- `http://127.0.0.1:8000/mymodel/<id>/delete/` (Delete view)

### 3️⃣ **Customize Templates**
The package provides default templates inside:
```
crud_builder/templates/crud_builder/
```
You can override them by creating your own templates in your app's `templates/` directory.

## 📜 License
This package is licensed under the MIT License.

## ❤️ Contributing
Feel free to submit issues and pull requests on GitHub!

## 📬 Contact
For any questions, reach out at mohammadh.khoddami@gmail.com

