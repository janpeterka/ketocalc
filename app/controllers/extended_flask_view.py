import inspect
import re

from flask import render_template as template
from flask import g

from app.helpers.form import create_form

from flask_classful import FlaskView

from app.controllers.forms import *  # noqa: F401, F403, F406
from app.models import *  # noqa: F401, F403, F406


class ExtendedFlaskView(FlaskView):
    """docstring for ExtendedFlaskView"""

    def before_request(self, name, id=None, *args, **kwargs):
        # form_name = model_name + "sForm"

        # e.g. User
        # model_name = model_name

        # e.g. user
        self.attribute_name = self._attribute_name()

        # e.g. class <User>
        try:
            model_klass = globals()[self._model_name()]
        except KeyError:
            model_klass = None
        # e.g. class <UsersForm>
        # try:
        #     form_klass = globals()[form_name]
        # except KeyError:
        #     form_klass = None
        g.request_item_type = self.attribute_name

        if id is not None and model_klass is not None:
            g.request_item_id = id
            instance = model_klass().load(id)
            # e.g. self.user, or None
            setattr(self, self.attribute_name, instance)
        else:
            setattr(self, self.attribute_name, None)

    def template(self, template_name=None, **kwargs):
        # Template name is given from view and method names if not provided
        calling_method = inspect.stack()[1].function
        if template_name is None:
            template_name = self._attribute_name() + "s/" + calling_method + ".html.j2"

        # All public variables of the view are passed to template
        view_attributes = self.__dict__
        public_attributes = {
            k: view_attributes[k] for k in view_attributes if not k.startswith("_")
        }

        # kwargs has higher priority, therefore rewrites public attributes
        merged_values = {**public_attributes, **kwargs}

        return template(template_name, **merged_values)

    def _model_name(self):
        if type(self).__name__.endswith("sView"):
            model_name = type(self).__name__.replace("sView", "")
        elif type(self).__name__.endswith("View"):
            model_name = type(self).__name__.replace("View", "")
        else:
            raise AttributeError("Controller name not ending with 'View'")

        return model_name

    def _attribute_name(self):
        model_name = self._model_name()
        snake_model_name = re.sub("(?!^)([A-Z]+)", r"_\1", model_name).lower()
        return snake_model_name

    def _template_folder(self):
        if hasattr(self, "template_folder"):
            return self.template_folder
        else:
            self.template_folder = self._attribute_name() + "s"

    def index(self):
        return self.template("{}/index.html.j2".format(self._template_folder()))

    def show(self, id):
        kwargs_dict = {}
        kwargs_dict[self.attribute_name] = self.object
        return self.template(
            "{}/show.html.j2".format(self._template_folder()), **kwargs_dict
        )

    def new(self):
        self.form = create_form(self.form_klass)
        return self.template("{}/new.html.j2".format(self._template_folder()))

    # def post(self):
    #     form = self.form_klass(request.form)
    #     if not form.validate_on_submit():
    #         save_form_to_session(request.form)
    #         return redirect(url_for("{}sView:new".format(self.model_name)))

    #     class_object = self.model_klass()
    #     form.populate_obj(class_object)
    #     if not class_object.save():
    #         # if save fails
    #         abort(500)

    #     return redirect(
    #         url_for("{}sView:show".format(self.model_name), id=class_object.id)
    #     )

    # @route("<id>/edit", methods=["POST"])
    # def post_edit(self, id):
    #     form = self.form_klass(request.form)
    #     if not form.validate_on_submit():
    #         save_form_to_session(request.form)
    #         return redirect(url_for("{}sView:edit".format(self.model_name)))

    #     form.populate_obj(self.object)
    #     self.object.edit()

    #     return redirect(
    #         url_for("{}sView:show".format(self.model_name), id=self.object.id,)
    #     )

    # def edit(self, id):
    #     form = create_form(self.form_klass, obj=self.object)
    #     return template(
    #         "{}s/edit.html.j2".format(self.attribute_name),
    #         form=form,
    #         id=self.object.id,
    #     )
