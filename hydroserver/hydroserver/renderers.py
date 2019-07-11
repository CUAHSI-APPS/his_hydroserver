from rest_framework import renderers


class WaterMLRenderer(renderers.BaseRenderer):
    media_type = "application/wml+xml"
    format = "wml"

    def render(self, data, media_type=None, renderer_context=None):
        return str(data).encode(self.charset)


class WaterJSONRenderer(renderers.BaseRenderer):
    media_type = "application/water+json"
    format = "waterjson"

    def render(self, data, media_type=None, renderer_context=None):
        return str(data).encode(self.charset)


class ReftsRenderer(renderers.BaseRenderer):
    media_type = "application/refts+json"
    format = "refts.json"

    def render(self, data, media_type=None, renderer_context=None):
        return str(data).encode(self.charset)


class GeoJSONRenderer(renderers.BaseRenderer):
    media_type = "application/geo+json"
    format = "geojson"

    def render(self, data, media_type=None, renderer_context=None):
        return str(data).encode(self.charset)
