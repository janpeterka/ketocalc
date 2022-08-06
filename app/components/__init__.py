from .links import link_to, link_to_edit, button_link_to, button_link_to_edit
from .dates import human_format_date
from .forms import option, options

__all__ = [
    "link_to",
    "link_to_edit",
    "button_link_to",
    "button_link_to_edit",
    "human_format_date",
    "option",
    "options",
]


def register_all_components(application):
    # links
    application.add_template_global(link_to)
    application.add_template_global(link_to_edit)
    application.add_template_global(button_link_to)
    application.add_template_global(button_link_to_edit)

    # dates
    application.add_template_global(human_format_date)

    # forms
    application.add_template_global(option)
    application.add_template_global(options)
