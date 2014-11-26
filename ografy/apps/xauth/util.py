def put_address(user, ip):
    """
    Add an address and pass on any database constraint exceptions.
    """
    address = user.address_set.filter(ip__exact=ip).first()

    if address is None:
        user.address_set.create(ip=ip)
    else:
        # Update the `last_access` field.
        address.save()
