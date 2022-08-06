from flask import Markup


def option(item, selected=False):
    selected_text = "selected" if selected else ""
    return Markup(
        f'<option name="{item.name}" value="{item.id}" {selected_text}>{item.name}</option>'
    )


def options(objects, selected_item=None):
    html = "".join(
        option(item, selected=(item == selected_item)) for item in objects
    )


    return Markup(html)
