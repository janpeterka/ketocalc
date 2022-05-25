import inspect
import re

from flask import abort
from flask import render_template as template

from flask_classful import FlaskView

from app.models import *  # noqa: F401, F403, F406
from app.controllers.forms import *  # noqa: F401, F403, F406


class BaseView(FlaskView):
    def validate_edit(self, instance):
        self.validate_operation(instance, "edit")

    def validate_show(self, instance):
        self.validate_operation(instance, "show")

    def validate_create(self, klass):
        self.validate_operation(klass, "create")

    def validate_delete(self, instance):
        self.validate_operation(instance, "delete")

    # TODO: Use this only internally, use specific validation in controllers
    def validate_operation(self, instance_or_klass, operation_type="show"):
        # if object_id is not None and instance is None:
        if instance_or_klass is None:
            abort(404)

        if operation_type == "show":
            if not instance_or_klass.can_current_user_view:
                abort(403)

        elif operation_type == "create":
            # instance_or_klass is class in this case
            if not instance_or_klass.can_current_user_create():
                abort(403)

        elif operation_type == "edit":
            if not instance_or_klass.can_current_user_edit:
                abort(403)

        elif operation_type == "delete":
            if not instance_or_klass.can_current_user_delete:
                abort(403)

        else:
            raise AttributeError("unknown 'operation_type'")

    def template(self, template_name=None, *args, **kwargs):
        """
        Smart templates:
        - will guess template name and location (if not stated in template_name)
            - if you want to use other filename than name of method, you pass it to `template_name` like `some_name`
            - if you want to specify your own location, you must state whole path - e.g.: `some_folder/some_file.html.j2`
        - will pass public (not starting with _) attributes from `self` to template

        :param      template_name:  The template name
        :type       template_name:  { type_description }
        :param      args:           The arguments
        :type       args:           list
        :param      kwargs:         The keywords arguments
        :type       kwargs:         dictionary
        """

        # Template name is given from view and method names if not provided
        calling_method = inspect.stack()[1].function

        if template_name is None:
            template_name = f"{self._template_folder}/{calling_method}.html.j2"
        # WARNING - if you only state complete filename without folder (e.g.: `template_name="something.html.j2"`), it will fail to find this file
        elif "/" in template_name or ".html.j2" in template_name:
            template_name = template_name
        else:
            template_name = f"{self._template_folder}/{template_name}.html.j2"

        # All public variables of the view are passed to template
        class_attributes = self.__class__.__dict__
        view_attributes = self.__dict__
        all_attributes = class_attributes | view_attributes
        public_attributes = {
            k: all_attributes[k] for k in all_attributes if not k.startswith("_")
        }

        # kwargs has higher priority, therefore rewrites public attributes
        merged_values = {**public_attributes, **kwargs}

        return template(template_name, **merged_values)

    @property
    def _model_name(self):
        """
        e.g. string "User"
        """
        if type(self).__name__.endswith("View"):
            model_name = type(self).__name__.replace("View", "")
        else:
            raise AttributeError("Controller name not ending with 'View'")

        return model_name

    @property
    def _model_klass(self):
        """
        e.g. class <User>
        """
        try:
            model_klass = globals()[self._model_name]
        except KeyError:
            model_klass = None

        return model_klass

    @property
    def _form_klass(self):
        """
        e.g. class <UserForm>
        """
        try:
            form_klass = globals()[self._form_name]
        except KeyError:
            form_klass = None

        return form_klass

    @property
    def _attribute_name(self):
        """
        e.g. class <UserForm>
        """
        model_name = self._model_name
        snake_model_name = re.sub("(?!^)([A-Z]+)", r"_\1", model_name).lower()
        return snake_model_name

    @property
    def _form_name(self):
        """
        e.g. string "UserForm"
        """
        form_name = f"{self._model_name}Form"
        return form_name

    @property
    def _template_folder(self):
        """
        e.g. string "users"
        """
        if hasattr(self, "template_folder"):
            return self.template_folder
        else:
            return f"{self._attribute_name}s"
