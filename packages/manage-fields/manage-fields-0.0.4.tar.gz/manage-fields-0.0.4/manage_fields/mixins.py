class MFViewMixin:
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()

        kwargs['context'] = self.get_serializer_context()

        # Allowed fields
        allowed_fields = self.request.query_params.get('allow_fields')
        if allowed_fields:
            allowed_fields = allowed_fields.strip('{}').split(',')
            kwargs['allowed_fields'] = allowed_fields

        # Disallowed fields
        disallowed_fields = self.request.query_params.get('disallow_fields')
        if disallowed_fields:
            disallowed_fields = disallowed_fields.strip('{}').split(',')
            kwargs['disallowed_fields'] = disallowed_fields

        return serializer_class(*args, **kwargs)


class MFSerializerMixin:
    def __init__(self, instance=None, data=None, **kwargs):
        allowed_fields = kwargs.pop('allowed_fields', None)
        disallowed_fields = kwargs.pop('disallowed_fields', None)
        super().__init__(instance=instance, data=data, **kwargs)

        if disallowed_fields:
            disallowed_fields = set(disallowed_fields)
            for field_name in disallowed_fields:
                self.fields.pop(field_name, None)

        if allowed_fields:
            allowed_fields = set(allowed_fields)
            existing_fields = set(self.fields.keys())
            for field_name in existing_fields - allowed_fields:
                self.fields.pop(field_name, None)
