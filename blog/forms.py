from django import forms
from .models import BlogArticle


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-control"


class BlogArticleForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = BlogArticle
        fields = "__all__"
