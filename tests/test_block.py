from django.core.exceptions import ValidationError
from django.test import TestCase
from wagtail import VERSION as WAGTAIL_VERSION

from wagtail_color_panel.blocks import NativeColorBlock
from wagtail_color_panel.widgets import ColorInputWidget

if WAGTAIL_VERSION >= (3, 0):
    from wagtail.test.utils import WagtailTestUtils
else:
    from wagtail.tests.utils import WagtailTestUtils


class BlockTest(TestCase, WagtailTestUtils):
    def test_color_block_render(self):
        block = NativeColorBlock()
        html = block.render("#333333")

        self.assertEqual("#333333", html)

    def test_form_uses_proper_input_type(self):
        block = NativeColorBlock()
        html = block.field.widget.render_html(name="cat", value="#333333", attrs={})

        self.assertEqual(block.field.widget.__class__, ColorInputWidget)
        self.assertIn('type="color"', html)

    def test_that_hex_colors_are_validated(self):
        block = NativeColorBlock()
        with self.assertRaises(ValidationError) as ctx:
            block.clean("Invalid")

        self.assertTrue("Enter a valid color hash" in str(ctx.exception))

    def test_color_block_supports_default_value(self):
        default_value = NativeColorBlock(default="#333333").get_default()
        self.assertEqual("#333333", default_value)

    def test_color_block_supports_preset_colors(self):
        default_value = NativeColorBlock(preset_colors=["#333333", "#000000"]).preset_colors
        self.assertEqual(["#333333", "#000000"], default_value)

    def test_form_includes_preset_colors(self):
        block = NativeColorBlock(preset_colors=["#333333", "#000000"])
        html = block.field.widget.render_html(name="cat", value="#333333", attrs={
            'preset_colors': ["#333333", "#000000"]
            })
        
        self.assertIn('<datalist id="preset_colors">', html)
        self.assertIn('<option>#000000</option>', html)
