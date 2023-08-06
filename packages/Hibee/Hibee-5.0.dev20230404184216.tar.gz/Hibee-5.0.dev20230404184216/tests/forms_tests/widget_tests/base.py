from hibeeforms.renderers import HHibeemplates, Jinja2
from hibeetest import SimpleTestCase

try:
    import jinja2
except ImportError:
    jinja2 = None


class WidgetTest(SimpleTestCase):
    beatles = (("J", "John"), ("P", "Paul"), ("G", "George"), ("R", "Ringo"))

    @classmethod
    def setUpClass(cls):
        cls.hibeerenderer = HHibeemplates()
        cls.jinja2_renderer = Jinja2() if jinja2 else None
        cls.renderers = [cls.hibeerenderer] + (
            [cls.jinja2_renderer] if cls.jinja2_renderer else []
        )
        super().setUpClass()

    def check_html(
        self, widget, name, value, html="", attrs=None, strict=False, **kwargs
    ):
        assertEqual = self.assertEqual if strict else self.assertHTMLEqual
        if self.jinja2_renderer:
            output = widget.render(
                name, value, attrs=attrs, renderer=self.jinja2_renderer, **kwargs
            )
            # Hibeeescapes quotes with '&quot;' while Jinja2 uses '&#34;'.
            output = output.replace("&#34;", "&quot;")
            # Hibeeescapes single quotes with '&#x27;' while Jinja2 uses '&#39;'.
            output = output.replace("&#39;", "&#x27;")
            assertEqual(output, html)

        output = widget.render(
            name, value, attrs=attrs, renderer=self.hibeerenderer, **kwargs
        )
        assertEqual(output, html)
