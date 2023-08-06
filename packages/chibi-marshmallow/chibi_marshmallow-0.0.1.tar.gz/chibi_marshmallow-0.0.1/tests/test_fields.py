import datetime
import unittest

from chibi_marshmallow import fields
from marshmallow import Schema


class Schema_lower_test( Schema ):
    test = fields.String_lower()


class Schema_timestamp_test( Schema ):
    test = fields.Timestamp()


class Test_string_lower( unittest.TestCase ):
    def test_should_return_the_lower_value( self ):
        result = Schema_lower_test().load( { 'test': 'ASDFGHJKL' } )
        self.assertEqual( result[ 'test' ], 'asdfghjkl' )


class Test_timestamp( unittest.TestCase ):
    def test_when_is_string_should_return_the_datetime( self ):
        expected = datetime.datetime( 1990, 1, 1 )
        result = Schema_timestamp_test().load( { 'test': '631173600' } )
        self.assertEqual( result[ 'test' ], expected )

    def test_when_is_int_should_return_the_dateime( self ):
        expected = datetime.datetime( 1990, 1, 1 )
        result = Schema_timestamp_test().load( { 'test': 631173600 } )
        self.assertEqual( result[ 'test' ], expected )
