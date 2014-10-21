from social.backends.oauth import BaseOAuth2


# TODO: Fix custom scope to work here
# Todo: Remove to other library.
class CustomOScopeAuth2(BaseOAuth2):
    def get_scope(self, scope):
        scope = super(BaseOAuth2, self).get_scope()

        if self.data.get('extrascope'):
            scope = scope

        return scope
