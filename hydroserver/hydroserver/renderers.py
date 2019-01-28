from rest_framework import renderers


class HydroServerRenderer(renderers.BaseRenderer):
    media_type = '*/*'
    format = 'txt'

    def render(self, data, media_type=None, renderer_context=None):
        return str(data).encode(self.charset)
