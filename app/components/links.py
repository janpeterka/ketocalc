from flask import Markup


def _link_to_str(text, value, **kwargs):
    from flask import url_for

    return f"""
        <a data-turbo=\"false\" class=\"{kwargs.get('class')}\" href=\"{url_for(text)}\">{value}</a>"""


def link_to(obj_or_str, **kwargs):
    from flask import url_for

    if type(obj_or_str) == str:
        text = kwargs.get("text")
        if obj_or_str == "login":
            if text is None:
                text = "přihlaste se"
            return (
                f"<a href='{url_for('LoginView:show')}' data-turbo=\"false\">{text}</a>"
            )
        elif obj_or_str == "register":
            if text is None:
                text = "zaregistrujte se"
            return f"<a href='{url_for('RegisterView:show')}' data-turbo=\"false\">{text}</a>"
        else:
            raise NotImplementedError("This string has no associated link_to")

    if type(obj_or_str) == str:
        return Markup(_link_to_str(obj_or_str, **kwargs))
    try:
        return obj_or_str.link_to(**kwargs)
    except Exception:
        raise NotImplementedError(
            f"{obj_or_str}({obj_or_str.__class__}) doesn't have `link_to` implemented"
        )


def link_to_edit(obj, **kwargs):
    try:
        return obj.link_to_edit(**kwargs)
    except Exception:
        raise NotImplementedError(
            f"{obj}({obj.__class__}) doesn't have `link_to_edit` implemented"
        )


def button_link_to(obj_or_str, type="primary", **kwargs):
    class_ = kwargs.get("class", "") + f"btn btn-{type}"
    kwargs["class"] = class_

    return link_to(obj_or_str, **kwargs)


def button_link_to_edit(obj, type="primary", **kwargs):
    class_ = kwargs.get("class", "") + f"btn btn-{type}"
    kwargs["class"] = class_

    return link_to_edit(obj, **kwargs)


# def icon_link_to_edit(obj, **kwargs):
#     from app.components import simple_icon

#     return link_to_edit(obj, value=simple_icon("edit"), **kwargs)
