# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class TouchableComponent(Component):
    """A TouchableComponent component.


Keyword arguments:

- children (a list of or a singular dash component, string or number; optional)

- id (string; optional)

- className (string; optional)

- direction (string; optional)

- end_timestamp (number; optional)

- long_swipe (number; optional)

- long_tap (number; optional)

- long_tap_end (number; optional)

- start_timestamp (number; optional)

- touches (list of dicts; optional)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'thinks_dash_components'
    _type = 'TouchableComponent'
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, className=Component.UNDEFINED, touches=Component.UNDEFINED, direction=Component.UNDEFINED, long_tap=Component.UNDEFINED, long_tap_end=Component.UNDEFINED, long_swipe=Component.UNDEFINED, start_timestamp=Component.UNDEFINED, end_timestamp=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'direction', 'end_timestamp', 'long_swipe', 'long_tap', 'long_tap_end', 'start_timestamp', 'touches']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'direction', 'end_timestamp', 'long_swipe', 'long_tap', 'long_tap_end', 'start_timestamp', 'touches']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(TouchableComponent, self).__init__(children=children, **args)
