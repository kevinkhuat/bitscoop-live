from ografy.util import update


class BaseApi(object):
    @classmethod
    def delete(cls, val):
        # TODO: DELETE all? Check the link for manual transactions.
        # http://stackoverflow.com/questions/1136106/what-is-an-efficent-way-of-inserting-thousands-of-records-into-an-sqlite-table-u
        try:
            cls.model.objects.get(pk=val).delete()
        except TypeError:
            cls.model.objects.filter(val).delete()
        except cls.model.DoesNotExist:
            return False

        return True

    @classmethod
    def get(cls, val=None):
        if val is None:
            ret = list(cls.model.objects.all())
        else:
            try:
                ret = list(cls.model.objects.get(pk=val))
            except TypeError:
                ret = list(cls.model.objects.filter(val))

        return ret

    @classmethod
    def patch(cls, val, data):
        # TODO: Strip out pk and foreign keys from data so it doesn't silent bombfuck with malicious data.
        try:
            inst = list(cls.model.objects.get(pk=val))
            update(inst, data)
            inst.save()
        except TypeError:
            # TODO: Transform Q expression `val` into something that peppers in permissions so you can't blindly update things that don't belong to you.
            cls.model.objects.filter(val).update(**data)
            inst = list(cls.models.objects.filter(val))

        return inst

    @classmethod
    def post(cls, data):
        # TODO: POST all? Check the link for manual transactions.
        # http://stackoverflow.com/questions/1136106/what-is-an-efficent-way-of-inserting-thousands-of-records-into-an-sqlite-table-u
        if isinstance(data, cls.model):
            inst = data.save()
        else:
            inst = cls.model(**data)
            inst.save()

        return inst

    @classmethod
    def put(cls, pk, data):
        # TODO: Support multiple objects? There doesn't seem to be an easy way to batch PUT with transactions.
        # Should we add in all the fields that aren't included and set them to their nullable values and then batch PATCH?
        if isinstance(data, cls.model):
            data.pk = pk
            inst = data.save()
        else:
            inst = cls.model(**data)
            inst.pk = pk
            inst.save()

        return inst
