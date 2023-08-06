class MFViewMixin:
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()

        allowed_fields = self.request.query_params.get('allow_fields')
        if allowed_fields:
            allowed_fields = allowed_fields.strip('{}').split(',')
            kwargs['allowed_fields'] = allowed_fields

        return serializer_class(*args, **kwargs)


class MFSerializerMixin:
    def __init__(self, instance=None, data=None, **kwargs):
        allowed_fields = kwargs.pop('allowed_fields', None)
        super().__init__(instance=instance, data=data, **kwargs)
        if allowed_fields:
            allowed_fields = set(allowed_fields)
            existing_fields = set(self.fields.keys())
            for field_name in existing_fields - allowed_fields:
                self.fields.pop(field_name)
