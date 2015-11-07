import datetime as py_datetime
import json
import math

import geopy
from dateutil import parser
from django.conf import settings
from geopy.distance import VincentyDistance
from motorengine import Q
from tornado import gen

from server.apps.passthrough.documents import Settings
from server.contrib.estoolbox.tornadoes_bulk import ESBulkConnection


es_connection = ESBulkConnection(
    settings.ELASTICSEARCH['HOST'],
    settings.ELASTICSEARCH['PORT']
)


def get_previous_query(user_id, datetime):
    return {
        'size': '1',
        'from': 0,
        'query': {
            'filtered': {
                'filter': {
                    'and': [
                        {
                            'bool': {
                                'must': {
                                    'term': {
                                        'user_id': user_id
                                    }
                                }
                            }
                        },
                        {
                            'range': {
                                'datetime': {
                                    'lte': datetime
                                }
                            }
                        }
                    ]
                }
            }
        },
        'sort': [
            {
                'datetime': {
                    'order': 'desc'
                }
            }
        ]
    }


def get_next_query(user_id, datetime):
    return {
        'size': '1',
        'from': 0,
        'query': {
            'filtered': {
                'filter': {
                    'and': [
                        {
                            'bool': {
                                'must': {
                                    'term': {
                                        'user_id': user_id
                                    }
                                }
                            }
                        },
                        {
                            'range': {
                                'datetime': {
                                    'gte': datetime
                                }
                            }
                        }
                    ]
                }
            }
        },
        'sort': [
            {
                'datetime': {
                    'order': 'asc'
                }
            }
        ]
    }


def distance_on_unit_sphere(lat1, long1, lat2, long2):
    # Convert latitude and longitude to
    # spherical coordinates in radians.
    degrees_to_radians = math.pi / 180.0
    # phi = 90 - latitude
    phi1 = (90.0 - lat1) * degrees_to_radians
    phi2 = (90.0 - lat2) * degrees_to_radians

    # theta = longitude
    theta1 = long1 * degrees_to_radians
    theta2 = long2 * degrees_to_radians

    # Compute spherical distance from spherical coordinates.

    # For two locations in spherical coordinates
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) =
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length

    cos = (math.sin(phi1) * math.sin(phi2) * math.cos(theta1 - theta2) +
           math.cos(phi1) * math.cos(phi2))
    arc = math.acos(cos)

    # Remember to multiply arc by the radius of the earth
    # in your favorite set of units to get length.
    return arc


@gen.coroutine
def estimate(user_id, datetime):
    """
    This function is called when an event does not have a location.
    It gets the user's location estimation method and calls the function that uses that method to estimate locations.

    :param user_id: The ID of the user whose event's location is being estimated
    :param datetime: The datetime of the event whose location is being estimated
    :return: An estimated location
    """

    # Get the user's location estimation method
    user_settings = yield Settings.objects.filter(Q({'user_id': user_id})).find_all()
    user_settings = user_settings[0]
    location_estimation_method = user_settings.location_estimation_method

    # TODO: Make this flexible
    index = 'core'
    doc_type = 'location'

    # Convert the datetime to the format in which it's stored in the DB
    # datetime = datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    # Call the function corresponding to the user's estimation method
    if location_estimation_method == 'Last':
        estimate_response = yield estimate_location_last(user_id, datetime, index, doc_type)
    elif location_estimation_method == 'Next':
        estimate_response = yield estimate_location_next(user_id, datetime, index, doc_type)
    elif location_estimation_method == 'Closest':
        estimate_response = yield estimate_location_closest(user_id, datetime, index, doc_type)
    elif location_estimation_method == 'Between':
        estimate_response = yield estimate_location_between(user_id, datetime, index, doc_type)

    return estimate_response


@gen.coroutine
def estimate_location_last(user_id, datetime, index, doc_type):
    """
    Finds the Location that most recently precedes the event being estimated

    :param user_id: The ID of the user whose event's location is being estimated
    :param datetime: The datetime of the event whose location is being estimated
    :param index: The ElasticSearch index where Locations are stored
    :param doc_type: The ElasticSearch doc_type for Locations, which will be 'location'
    :return: An estimated Location
    """

    # Construct the filter string
    query = get_previous_query(user_id, datetime)

    try:
        # Query ES and save the result
        search_result = yield es_connection.search(
            index=index,
            type=doc_type,
            source=query
        )

        # Store the hits from the DB; hopefully there is one
        hits = json.loads(search_result.body.decode('utf-8'))['hits']['hits']

        # If there is one hit, then get its coordinates and return them
        if len(hits) == 1:
            coordinates = hits[0]['_source']['geolocation']
            geolocation = {
                'estimated': True,
                'estimation_method': 'Last',
                'geo_format': 'lat_lng',
                'geolocation': coordinates
            }
        # If there isn't a hit, then the query was for a date before the oldest one for this user
        # In that case, search for the Location at the earliest available date and use that instead
        else:
            query = get_next_query(user_id, datetime)

            search_result = yield es_connection.search(
                index=index,
                type=doc_type,
                source=query
            )

            hits = json.loads(search_result.body.decode('utf-8'))['hits']['hits']

            if len(hits) == 1:
                coordinates = hits[0]['_source']['geolocation']
                geolocation = {
                    'estimated': True,
                    'estimation_method': 'Last',
                    'geo_format': 'lat_lng',
                    'geolocation': coordinates
                }
            # If there are no Locations on which to estimate, use a fallback point in the middle of the country.
            # At a later date, once there are some Locations associated with the user, the estimated location
            # will be updated with a more accurate result.
            else:
                # Construct a Location with the fallback coordinates
                coordinates = [-94.596750, 39.193406]
                geolocation = {
                    'estimated': True,
                    'estimation_method': 'Last',
                    'geo_format': 'lat_lng',
                    'geolocation': coordinates
                }

    # If there are no Locations on which to estimate, use a fallback point in the middle of the country.
    # At a later date, once there are some Locations associated with the user, the estimated location
    # will be updated with a more accurate result.
    except:
        # Construct a Location with the fallback coordinates
        coordinates = [-94.596750, 39.193406]
        geolocation = {
            'estimated': True,
            'estimation_method': 'Last',
            'geo_format': 'lat_lng',
            'geolocation': coordinates
        }

    return geolocation


@gen.coroutine
def estimate_location_next(user_id, datetime, index, doc_type):
    """
    Finds the Location that most closely follows the event being estimated

    :param user_id: The ID of the user whose event's location is being estimated
    :param datetime: The datetime of the event whose location is being estimated
    :param index: The ElasticSearch index where Locations are stored
    :param doc_type: The ElasticSearch doc_type for Locations, which will be 'location'
    :return: An estimated Location
    """
    # Construct the filter string
    query = get_next_query(user_id, datetime)

    try:
        # Query ES and save the result
        search_result = yield es_connection.search(
            index=index,
            type=doc_type,
            source=query
        )

        # Store the hits from the DB; hopefully there is one
        hits = json.loads(search_result.body.decode('utf-8'))['hits']['hits']

        # If there is one hit, then get its coordinates and return them
        if len(hits) == 1:
            coordinates = hits[0]['_source']['geolocation']
            geolocation = {
                'estimated': True,
                'estimation_method': 'Next',
                'geo_format': 'lat_lng',
                'geolocation': coordinates
            }
        # If there isn't a hit, then the query was for a date after the newest one for this user
        # In that case, search for the Location at the latest available date and use that instead
        else:
            query = get_previous_query(user_id, datetime)

            search_result = yield es_connection.search(
                index=index,
                type=doc_type,
                source=query
            )

            hits = json.loads(search_result.body.decode('utf-8'))['hits']['hits']

            if len(hits) == 1:
                coordinates = hits[0]['_source']['geolocation']
                geolocation = {
                    'estimated': True,
                    'estimation_method': 'Next',
                    'geo_format': 'lat_lng',
                    'geolocation': coordinates
                }
            # If there are no Locations on which to estimate, use a fallback point in the middle of the country.
            # At a later date, once there are some Locations associated with the user, the estimated location
            # will be updated with a more accurate result.
            else:
                # Construct a Location with the fallback coordinates
                coordinates = [-94.596750, 39.193406]
                geolocation = {
                    'estimated': True,
                    'estimation_method': 'Last',
                    'geo_format': 'lat_lng',
                    'geolocation': coordinates
                }

    # If there are no Locations on which to estimate, use a fallback point in the middle of the country.
    # At a later date, once there are some Locations associated with the user, the estimated location
    # will be updated with a more accurate result.
    except:
        # Construct a Location with the fallback coordinates
        coordinates = [-94.596750, 39.193406]
        geolocation = {
            'estimated': True,
            'estimation_method': 'Next',
            'geo_format': 'lat_lng',
            'geolocation': coordinates
        }

    return geolocation


@gen.coroutine
def estimate_location_closest(user_id, datetime, index, doc_type):
    """
    Finds the Location that most closely precedes and follows the event being estimated
    and returns the one that is closer in time

    :param user_id: The ID of the user whose event's location is being estimated
    :param datetime: The datetime of the event whose location is being estimated
    :param index: The ElasticSearch index where Locations are stored
    :param doc_type: The ElasticSearch doc_type for Locations, which will be 'location'
    :return: An estimated Location
    """
    query1 = get_previous_query(user_id, datetime)
    query2 = get_next_query(user_id, datetime)

    # Search both before and after the event
    es_connection.search(
        source=query1,
        index=index,
        type=doc_type,
        callback=(yield gen.Callback('search_result_previous'))
    )

    es_connection.search(
        source=query2,
        index=index,
        type=doc_type,
        callback=(yield gen.Callback('search_result_next'))
    )

    search_result_previous = yield gen.Wait('search_result_previous')
    search_result_next = yield gen.Wait('search_result_next')

    # Store the hits from the DB; hopefully there is one for each search
    hits1 = json.loads(search_result_previous.body.decode('utf-8'))['hits']['hits']
    hits2 = json.loads(search_result_next.body.decode('utf-8'))['hits']['hits']

    geolocation = ''

    # If there is a result both before and after, use the one closer in time
    if len(hits1) == 1 and len(hits2) == 1:
        geolocation1 = hits1[0]['_source']
        geolocation2 = hits2[0]['_source']
        date1 = parser.parse(geolocation1['datetime'])
        date2 = parser.parse(geolocation2['datetime'])

        if abs(parser.parse(datetime) - date1) < abs(parser.parse(datetime) - date2):
            coordinates = geolocation1['geolocation']
        else:
            coordinates = geolocation2['geolocation']

        geolocation = {
            'estimated': True,
            'estimation_method': 'Next',
            'geo_format': 'lat_lng',
            'geolocation': coordinates
        }
    # If there isn't a result before, use the one after
    elif len(hits1) == 0:
        coordinates = hits2[0]['_source']['geolocation']
        geolocation = {
            'estimated': True,
            'estimation_method': 'Closest',
            'geo_format': 'lat_lng',
            'geolocation': coordinates
        }
    # If there isn't a result after, use the one before
    elif len(hits2) == 0:
        coordinates = hits1[0]['_source']['geolocation']
        geolocation = {
            'estimated': True,
            'estimation_method': 'Closest',
            'geo_format': 'lat_lng',
            'geolocation': coordinates
        }
    # If there are no Locations on which to estimate, use a fallback point in the middle of the country.
    # At a later date, once there are some Locations associated with the user, the estimated location
    # will be updated with a more accurate result.
    else:
        # Construct a Location with the fallback coordinates
        coordinates = [-94.596750, 39.193406]
        geolocation = {
            'estimated': True,
            'estimation_method': 'Closest',
            'geo_format': 'lat_lng',
            'geolocation': coordinates
        }

    return geolocation


@gen.coroutine
def estimate_location_between(user_id, datetime, index, doc_type):
    """
    Finds the locations that most closely precede and follow the event being estimated
    and then constructs a point between them whose spatial separation from the surrounding points
    is in proportion to the chronological separation from them.
    E.g., if the time between the two surrounding Locations is 8 hours and the event occurred 6 hours
    after the first one (and therefore 2 hours before the second one), the coordinates would be
    75% of the straight-line distance from the first point to the second.

    :param user_id: The ID of the user whose event's location is being estimated
    :param datetime: The datetime of the event whose location is being estimated
    :param index: The ElasticSearch index where Locations are stored
    :param doc_type: The ElasticSearch doc_type for Locations, which will be 'location'
    :return: An estimated Location
    """
    query1 = get_previous_query(user_id, datetime)
    query2 = get_next_query(user_id, datetime)

    # Search both before and after the event
    es_connection.search(
        source=query1,
        index=index,
        type=doc_type,
        callback=(yield gen.Callback('search_result_previous'))
    )

    es_connection.search(
        source=query2,
        index=index,
        type=doc_type,
        callback=(yield gen.Callback('search_result_next'))
    )

    search_result_previous = yield gen.Wait('search_result_previous')
    search_result_next = yield gen.Wait('search_result_next')

    # Store the hits from the DB; hopefully there is one for each search
    hits1 = json.loads(search_result_previous.body.decode('utf-8'))['hits']['hits']
    hits2 = json.loads(search_result_next.body.decode('utf-8'))['hits']['hits']

    geolocation = ''

    # If there is a result both before and after, estimate a point in between them in proportion to
    # how far away each surrounding point is in time from the point being estimated
    if len(hits1) == 1 and len(hits2) == 1:
        geolocation1 = hits1[0]['_source']
        geolocation2 = hits2[0]['_source']

        lat1 = geolocation1['geolocation'][1]
        lon1 = geolocation1['geolocation'][0]
        lat2 = geolocation2['geolocation'][1]
        lon2 = geolocation2['geolocation'][0]
        date1 = parser.parse(geolocation1['datetime'])
        date2 = parser.parse(geolocation2['datetime'])

        # Calculate the total amount of time between the surrounding points.
        total_date_spread = abs(date1 - date2)

        # Calculate the time from the event being estimated to date1.
        datetime_to_date1 = abs(parser.parse(datetime) - date1)

        # Calculate what percentage of the total date spread is made up of the date difference from datetime to date1.
        percentage_from_date1 = datetime_to_date1 / total_date_spread

        # Get the distance between the surrounding points, in km
        distance = distance_on_unit_sphere(lat1, lon1, lat2, lon2) * 6373

        # Calculate the distance from date1 that the estimated location should be based on its percentage of the total distance.
        distance_from_date1 = distance * percentage_from_date1

        # Get the radian values of the latitudes for the surrounding points.
        radlat1 = math.radians(lat1)
        radlat2 = math.radians(lat2)

        # Get the difference in the longitudes for the surrounding points.
        diff_long = math.radians(lon2 - lon1)

        # Get the bearing from location1 to location2, in degrees.
        x = math.sin(diff_long) * math.cos(radlat2)
        y = math.cos(radlat1) * math.sin(radlat2) - (math.sin(radlat1) * math.cos(radlat2) * math.cos(diff_long))
        initial_bearing = math.degrees(math.atan2(x, y))

        origin = geopy.Point(lat1, lon1)

        # Get the estimated location of the event in question using location1 (origin), the distance from location1, and the bearing
        # between location1 and location2.
        destination = VincentyDistance(kilometers=distance_from_date1).destination(origin, initial_bearing)
        returnlat2, returnlon2 = destination.latitude, destination.longitude

        coordinates = [returnlon2, returnlat2]
        geolocation = {
            'estimated': True,
            'estimation_method': 'Between',
            'geo_format': 'lat_lng',
            'geolocation': coordinates
        }
    # If there isn't a result before, use the one after
    elif len(hits1) == 0 and len(hits2) == 1:
        coordinates = hits2[0]['_source']['geolocation']
        geolocation = {
            'estimated': True,
            'estimation_method': 'Between',
            'geo_format': 'lat_lng',
            'geolocation': coordinates
        }
    # If there isn't a result after, use the one before
    elif len(hits2) == 0 and len(hits1) == 1:
        coordinates = hits1[0]['_source']['geolocation']
        geolocation = {
            'estimated': True,
            'estimation_method': 'Between',
            'geo_format': 'lat_lng',
            'geolocation': coordinates
        }
    # If there are no Locations on which to estimate, use a fallback point in the middle of the country.
    # At a later date, once there are some Locations associated with the user, the estimated location
    # will be updated with a more accurate result.
    else:
        # Construct a Location with the fallback coordinates
        coordinates = [-94.596750, 39.193406]
        geolocation = {
            'estimated': True,
            'estimation_method': 'Between',
            'geo_format': 'lat_lng',
            'geolocation': coordinates
        }

    return geolocation


@gen.coroutine
def reestimate_all(user_id):
    """
    This function gets all of the events for a user that were estimated and checks if there is
    a different estimation for each one.  If so, it patches the event with the new estimation.
    Note that 'different' does not exactly mean 'better'.  If the user changed their estimation method
    since the previous estimation, the location for a given event may be farther off with the new method.
    The only way the estimation isn't changed is if the new location is the same as the old one.

    :param user_id: The ID of the user whose events' locations are being estimated
    :return: Nothing
    """

    search_end = False
    from_parameter = 0
    size_parameter = 1000
    events_with_estimated_locations = []

    # Get all of the events whose locations are estimated
    estimated_location_query = {
        'query': {
            'filtered': {
                'filter': {
                    'and': [
                        {
                            'bool': {
                                'must': {
                                    'term': {
                                        'location.estimated': True
                                    }
                                }
                            }
                        },
                        {
                            'bool': {
                                'must': {
                                    'term': {
                                        'user_id': user_id
                                    }
                                }
                            }
                        },
                    ]
                }
            }
        },
        'from': from_parameter,
        'size': size_parameter
    }

    while not search_end:
        estimated_location_query['from'] = from_parameter

        response = yield es_connection.search(
            index='core',
            type='event',
            source=estimated_location_query
        )

        decoded_result = json.loads(response.body.decode('utf-8'))['hits']['hits']
        events_with_estimated_locations += decoded_result

        if len(decoded_result) < size_parameter:
            search_end = True
        else:
            from_parameter += size_parameter

    # Get the user's settings, and from that get their location estimation method
    user_settings = yield Settings.objects.filter(Q({'user_id': user_id})).find_all()
    user_settings = user_settings[0]
    location_estimation_method = user_settings.location_estimation_method

    index = 'core'
    doc_type = 'location'

    # Iterate through the set of events
    for event_result in events_with_estimated_locations:
        event = event_result['_source']
        datetime = event['datetime']

        new_location = ''

        # Call the function corresponding to the user's estimation method
        if location_estimation_method == 'Last':
            new_location = yield estimate_location_last(user_id, datetime, index, doc_type)
        elif location_estimation_method == 'Next':
            new_location = yield estimate_location_next(user_id, datetime, index, doc_type)
        elif location_estimation_method == 'Closest':
            new_location = yield estimate_location_closest(user_id, datetime, index, doc_type)
        elif location_estimation_method == 'Between':
            new_location = yield estimate_location_between(user_id, datetime, index, doc_type)

        # To save on DB writes, only patch the event's location if it's different from what's currently there.
        if event['location']['geolocation'] != new_location['geolocation']:

            # Replace the event's location with the new one.
            event['location'] = new_location

            # Patch the event in the DB.
            es_connection.put(
                index='core',
                type='event',
                uid=event_result['_id'],
                contents=event
            )

    user_settings.last_estimate_all_locations = py_datetime.datetime.now()
    yield user_settings.save()
