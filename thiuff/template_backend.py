import sys
import jinja2
from jinja2.ext import Extension, nodes

from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.template import TemplateDoesNotExist, TemplateSyntaxError
from django.template.backends import jinja2 as jinja2backend
from django.template.backends.utils import csrf_input_lazy, csrf_token_lazy
from django.template.defaultfilters import pluralize
from django.utils import six
from django.utils.module_loading import import_string

from .shortcuts import get_flashes


def environment(**options):
    env = jinja2.Environment(**options)
    env.globals.update({
        'settings': settings,
        'get_flashes': get_flashes,
    })
    env.filters["pluralize"] = pluralize
    return env


class Jinja2(jinja2backend.Jinja2):
    def __init__(self, params):
        self.context_processors = [
            import_string(p)
            for p in params['OPTIONS'].pop('context_processors', [])
        ]
        super(Jinja2, self).__init__(params)

    def from_string(self, template_code):
        return Template(
            self.env.from_string(template_code), self.context_processors)

    def get_template(self, template_name):
        try:
            return Template(
                self.env.get_template(template_name), self.context_processors)
        except jinja2.TemplateNotFound as exc:
            six.reraise(TemplateDoesNotExist, TemplateDoesNotExist(exc.args),
                        sys.exc_info()[2])
        except jinja2.TemplateSyntaxError as exc:
            six.reraise(TemplateSyntaxError, TemplateSyntaxError(exc.args),
                        sys.exc_info()[2])


class Template(jinja2backend.Template):

    def __init__(self, template, context_processors):
        self.template = template
        self.context_processors = context_processors

    def render(self, context=None, request=None):
        if context is None:
            context = {}
        if request is not None:
            context['request'] = request
            lazy_csrf_input = csrf_input_lazy(request)
            context['csrf'] = lambda: lazy_csrf_input
            context['csrf_input'] = lazy_csrf_input
            context['csrf_token'] = csrf_token_lazy(request)
            for cp in self.context_processors:
                context.update(cp(request))
        return self.template.render(context)
