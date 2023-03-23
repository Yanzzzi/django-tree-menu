from django import template
from menu.models import Item, Menu

register = template.Library()


@register.filter
def get_type(value):
    return type(value).__name__


@register.inclusion_tag('menu/draw.html', takes_context=True)
def draw_menu(context, main_menu):
    items = list(Menu.objects.values('items__pk', 'items__title', 'items__childrens', 'items__parent', 'items__slug').filter(title=main_menu))
    childs = {}
    for i in items:
        print(i)
    print('-'*100)
    items_to_render = {'menu_name': main_menu, main_menu: {}}
    for item in items:
        if not item['items__childrens'] and not item['items__parent']:
            items_to_render[main_menu][item['items__title']] = item['items__slug']
        elif item['items__childrens'] and not item['items__parent']:
            if item['items__title'] not in items_to_render[main_menu]:
                items_to_render[main_menu][item['items__title']] = {'child_ids': []}
            items_to_render[main_menu][item['items__title']]['child_ids'].append(item['items__childrens'])
        elif not item['items__childrens'] and item['items__parent']:
            childs[item['items__pk']] = items[item['items__pk']]
        else:
            # TODO сделать кейс когда есть и родитель и ребенок
            pass
    print('childs')
    print(childs)
    while childs:
        for k, v in items_to_render[main_menu].items():
            if type(v) == dict:
                child_id = v['child_ids'].pop(0)
                child = childs.pop(child_id)
                v[child['items__title']] = child['items__slug']
                if not childs:
                    del v['child_ids']
    print('###########context############')
    print(items_to_render)
    return items_to_render
