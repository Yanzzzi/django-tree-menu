from django import template
from menu.models import Item
from django.db.models import Q

register = template.Library()


@register.filter
def get_type(value):
    return type(value).__name__


@register.inclusion_tag('menu/draw.html')
def draw_menu(main_menu):
    items = Item.objects.filter(menu__title=main_menu)
    items_val = list(items.values())

    items_with_childs = items.filter(childrens__isnull=False).values('childrens')

    items_to_render = get_items_dict(items, items_val, items_with_childs)
    menu_items = {'menu_name': main_menu, 'items': items_to_render}
    return menu_items


def get_items_dict(items, items_val, items_with_childs):
    items_to_render = {}
    for item in items_val:
        if items.filter(Q(pk=item['id']) & Q(childrens__isnull=True)).exists():
            if check_field_added(items_to_render, item['title']):
                items_to_render[item['title']] = item['slug']
        else:  # have childs
            childs_val = items.filter(Q(pk__in=items_with_childs) & Q(parent_id=item['id'])).values()
            sub_items = get_items_dict(items, childs_val, items_with_childs)
            items_to_render[item['title']] = sub_items

    return items_to_render


def check_field_added(items, item_title):
    for k, v in items.items():
        if type(v) == dict:
            ans = check_field_added(v, item_title)
            if not ans:
                return False
        else:
            if k == item_title:
                return False
    return True
