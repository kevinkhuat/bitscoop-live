from ografy.apps.obase.managers import BaseManager


class Entity(object):
    class Meta:
        collection_name = 'entities'
        manager_class = BaseManager

    # When defining the class, need to instantiate an instance of BaseManager stored in Entity.objects.
    # Figure out how metaclassing works in this scenario (check Django models).

    id = fields.IntegerField()


    @classmethod
    def parse(cls, data):
        # parsed should actualy transform data into a 1:1 dict representation of an entity.
        # This dict can then be unpacked into the Entity constructor.

        # e.g.
        #
        # parsed = {
        #   'id': 6
        # }

        parsed = data

        return cls(**parsed)


class Events(Entities):


    collection = DB['events']
    SPEC = EVENTS_SPEC
