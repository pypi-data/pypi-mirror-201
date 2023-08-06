# Manage fields

**settings.py**
```pycon
INSTALLED_APPS = [
    ...,
    'manage_fields'
]
```

**views.py**
```pycon
class MyView(MFViewMixin, ...):
    serializer_class = MySerializer
    ....
```

**serializers.py**
```pycon
class MySerializer(MFSerializer, ...):
    ...
```

**Request**
```text
https://abcd.com/?allow_fields={id,name}
```