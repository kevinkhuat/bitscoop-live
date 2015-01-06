from django.db.models import Q


class BaseApi(object):
    @classmethod
    def delete(cls, val):
        # TODO: DELETE all? Check the link for manual transactions.
        # http://stackoverflow.com/questions/1136106/what-is-an-efficent-way-of-inserting-thousands-of-records-into-an-sqlite-table-u
        try:
            if type(val) is Q:
                ret = cls.model.objects.get(val).delete()
            else:
                ret = cls.model.objects.filter(pk=val).delete()
        except cls.model.DoesNotExist:
            return False

        return True

    @classmethod
    def get(cls, val=None):
        if val is None:
            ret = cls.model.objects.all()
        else:
            if type(val) is Q:
                ret = cls.model.objects.get(val)
            else:
                ret = cls.model.objects.filter(pk=val)

        return ret

    @classmethod
    def patch(cls, val, data):
        if type(val) is Q:
            cls.model.objects.get(val).update(**data)
            inst = cls.models.objects.get(val)
        else:
            inst = cls.model.objects.filter(pk=val)
            for key, value in data.items():
                setattr(inst, key, value)
            inst.save()
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
