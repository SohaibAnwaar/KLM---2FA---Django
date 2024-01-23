from django_neomodel import DjangoNode
from neomodel import StringProperty, RelationshipTo, DateTimeProperty, FloatProperty


class Region(DjangoNode):
    code = StringProperty()
    name = StringProperty()
    type = StringProperty()


class VioScoreTotal(DjangoNode):
    value = StringProperty()
    region = RelationshipTo('Region', 'HAS_VIOSCORE')


class Dimension(DjangoNode):
    value = StringProperty()
    vio_score_total = RelationshipTo('VioScoreTotal', 'HAS_DIMENSION')


class Alert(DjangoNode):
    timestamp = DateTimeProperty()
    change_magnitude = FloatProperty()
    title = StringProperty()


class Country(DjangoNode):
    name = StringProperty()

