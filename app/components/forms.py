from flask import Markup


def option(item, selected=False):
    if selected:
        selected_text = "selected"
    else:
        selected_text = ""

    return Markup(
        f'<option name="{item.name}" value="{item.id}" {selected_text}>{item.name}</option>'
    )


def options(objects, selected_item=None):
    html = ""

    for item in objects:
        html += option(item, selected=(item == selected_item))

    return Markup(html)
