import datetime
from marshmallow import fields, ValidationError


class String_lower( fields.String ):
    """
    Este campo siempre regresa en minuscalas la cadena
    """

    def _deserialize( self, value, attr, data, **kw ):
        value = super()._deserialize( value, attr, data, **kw )
        return value.lower()


class Timestamp( fields.Field ):
    """
    transforma un timestamp a datetime
    """

    def _deserialize( self, value, attr, data, **kw ):
        return datetime.datetime.fromtimestamp( float( value ) )
