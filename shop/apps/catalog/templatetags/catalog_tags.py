from django import template
from ..models import Category


register = template.Library()


@register.inclusion_tag('catalog/category_tree.html', takes_context=True)
def get_family(context):
    category_roots = Category.objects.filter(parent=None)
    categories = category_roots.get_descendants(include_self=True)
    context['categories'] = categories
    return context
