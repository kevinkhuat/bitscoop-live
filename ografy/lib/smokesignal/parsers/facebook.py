from __future__ import unicode_literals

from smokesignal.parsers import Parser


class facebook(Parser):

    # GET me/
    # https://graph.facebook.com/me
    def get_me(self, json):
        pass

    # GET me/friends
    # https://graph.facebook.com/me/friends

    # GET me/inbox
    # https://graph.facebook.com/me/inbox

    # GET me/outbox
    # https://graph.facebook.com/me/outbox
