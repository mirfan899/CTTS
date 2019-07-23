# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from sppas.src.dependencies.grako.model import Node
from sppas.src.dependencies.grako.codegen import CodegenError
from sppas.src.dependencies.grako.rendering import render, Renderer, RenderingFormatter


class DelegatingRenderingFormatter(RenderingFormatter):
    def __init__(self, delegate):
        assert hasattr(delegate, 'render')
        super(DelegatingRenderingFormatter, self).__init__()
        self.delegate = delegate

    # override
    def render(self, item, join='', **fields):
        result = self.delegate.render(item, join=join, **fields)
        if result is None:
            result = super(DelegatingRenderingFormatter, self).render(item, join=join, **fields)
        return result

    def convert_field(self, value, conversion):
        if isinstance(value, Node):
            return self.render(value)
        else:
            return super(DelegatingRenderingFormatter, self).convert_field(value, conversion)


class ModelRenderer(Renderer):
    def __init__(self, codegen, node, template=None):
        super(ModelRenderer, self).__init__(template=template)
        self._codegen = codegen
        self._node = node

        self.formatter = codegen.formatter

        self.__postinit__()

    def __postinit__(self):
        pass

    def __getattr__(self, name):
        try:
            super(ModelRenderer, self).__getattr__(name)
        except AttributeError:
            if name.startswith('_'):
                raise
            return getattr(self.node, name)

    @property
    def node(self):
        return self._node

    @property
    def codegen(self):
        return self._codegen

    def get_renderer(self, item):
        return self.codegen.get_renderer(item)

    def render(self, template=None, **fields):
        if isinstance(self.node, Node):
            fields.update({k: v for k, v in vars(self.node).items() if not k.startswith('_')})
        else:
            fields.update(value=self.node)
        return super(ModelRenderer, self).render(template=template, **fields)


class NullModelRenderer(ModelRenderer):
    """A `ModelRenderer` that generates nothing.
    """
    template = ''


class CodeGenerator(object):
    """
    A **CodeGenerator** is an abstract class that finds a
    ``ModelRenderer`` class with the same name as each model's node and
    uses it to render the node.
    """
    def __init__(self, modules=None):
        self.formatter = DelegatingRenderingFormatter(self)
        self._renderers = []
        if modules is not None:
            self._renderers = self._find_module_renderers(modules)

    def _find_module_renderers(self, modules):
        result = dict()
        for module in modules:
            result.update(
                (name, dtype)
                for name, dtype in vars(module).items()
                if issubclass(dtype, ModelRenderer)
            )
        return result

    def _find_renderer_class(self, item):
        """
        This method is used to find a ``ModelRenderer`` for the given
        item. It can be overriden in descendat classes.
        """
        if not isinstance(item, Node):
            return None

        name = item.__class__.__name__
        try:
            return self._renderers[name]
        except KeyError:
            raise CodegenError('Renderer for %s not found' % name)

    def get_renderer(self, item):
        rendererClass = self._find_renderer_class(item)
        if rendererClass is None:
            return None
        try:
            assert issubclass(rendererClass, ModelRenderer)
            return rendererClass(self, item)
        except Exception as e:
            raise type(e)(str(e), rendererClass.__name__)

    def render(self, item, join='', **fields):
        renderer = self.get_renderer(item)
        if renderer is None:
            return render(item, join=join, **fields)
        return str(renderer.render(**fields))
