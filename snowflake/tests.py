import uuid
from django.test.testcases import TestCase

from snowflake.models import Snowflake


class FakeModel():

    def __init__(self):
        self.pk = uuid.uuid4()
        self.id = self.pk


class TestSnowflake(TestCase):

    def test_add_lookup_saves_snowflake(self):
        fm = FakeModel()
        Snowflake.add_lookup(fm)
        flake = Snowflake.objects.filter(id=fm.id)[0]
        self.assertEqual(flake.id, fm.id)
        self.assertEqual(flake.model_class, "%s.%s" % (fm.__class__.__module__, fm.__class__.__name__))

    def test_add_lookup_raises_no_pk(self):
        fm = FakeModel()
        del fm.pk
        self.assertRaises(TypeError, Snowflake.add_lookup, fm)

    def test_add_lookup_raises_pk_not_uuid(self):
        fm = FakeModel()
        fm.pk = 'fjdksfjdksjf'
        self.assertRaises(TypeError, Snowflake.add_lookup, fm)
