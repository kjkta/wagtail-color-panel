from django import forms
from django.utils.functional import cached_property
from wagtail import VERSION as WAGTAIL_VERSION

from wagtail_color_panel.validators import hex_triplet_validator
from wagtail_color_panel.widgets import ColorInputWidget

if WAGTAIL_VERSION >= (3, 0):
    from wagtail.blocks import FieldBlock
else:
    from wagtail.core.blocks import FieldBlock


class NativeColorBlock(FieldBlock):
    def __init__(self, required=True, help_text=None, validators=(), **kwargs):
        self.field_options = {
            "required": required,
            "help_text": help_text,
            "max_length": 7,
            "min_length": 7,
            "validators": [hex_triplet_validator],
        }
        self.preset_colors = kwargs.get('preset_colors', None)
        super().__init__(**kwargs)

    @cached_property
    def field(self):
        field_kwargs = {"widget": ColorInputWidget(attrs={
            'preset_colors': self.preset_colors
            })}
        field_kwargs.update(self.field_options)
        return forms.CharField(**field_kwargs)

    class Meta:
        icon = "radio-full"
