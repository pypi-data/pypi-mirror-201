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
from manage_fields.mixins import MFViewMixin

class MyView(MFViewMixin, ...):
    serializer_class = MySerializer
    ....
```

**serializers.py**
```pycon
from manage_fields.mixins import MFSerializer

class MySerializer(MFSerializer, ...):
    ...
```

**Request**
```text
https://abcd.com/?allow_fields={id,name}
```