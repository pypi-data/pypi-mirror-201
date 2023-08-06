# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Rotate(Component):
    """A Rotate component.


Keyword arguments:

- id (string; optional)

- delay (number; default 10)

- message (a list of or a singular dash component, string or number; optional)

- orientation (string; optional)

- reload (boolean; default True)

- timing (string; default 'all')"""
    _children_props = ['message']
    _base_nodes = ['message', 'children']
    _namespace = 'thinks_dash_components'
    _type = 'Rotate'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, orientation=Component.UNDEFINED, message=Component.UNDEFINED, reload=Component.UNDEFINED, timing=Component.UNDEFINED, delay=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'delay', 'message', 'orientation', 'reload', 'timing']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'delay', 'message', 'orientation', 'reload', 'timing']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Rotate, self).__init__(**args)
