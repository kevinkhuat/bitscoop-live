# Author: Liam Broza


########
# AUTH #  https://docs.djangoproject.com/en/1.7/ref/settings/#auth
########

# TODO: move back to main and remove social backends
AUTHENTICATION_BACKENDS = (
    'social.backends.amazon.AmazonOAuth2',
    'social.backends.angel.AngelOAuth2',
    'social.backends.aol.AOLOpenId',
    'social.backends.appsfuel.AppsfuelOAuth2',
    'social.backends.beats.BeatsOAuth2',
    'social.backends.behance.BehanceOAuth2',
    'social.backends.belgiumeid.BelgiumEIDOpenId',
    'social.backends.bitbucket.BitbucketOAuth',
    'social.backends.box.BoxOAuth2',
    'social.backends.clef.ClefOAuth2',
    'social.backends.coinbase.CoinbaseOAuth2',
    'social.backends.dailymotion.DailymotionOAuth2',
    'social.backends.disqus.DisqusOAuth2',
    'social.backends.douban.DoubanOAuth2',
    'social.backends.dropbox.DropboxOAuth',
    'social.backends.dropbox.DropboxOAuth2',
    'social.backends.evernote.EvernoteSandboxOAuth',
    'social.backends.facebook.FacebookAppOAuth2',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.fedora.FedoraOpenId',
    'social.backends.fitbit.FitbitOAuth',
    'social.backends.flickr.FlickrOAuth',
    'social.backends.foursquare.FoursquareOAuth2',
    'social.backends.github.GithubOAuth2',
    'social.backends.google.GoogleOAuth',
    'social.backends.google.GoogleOAuth2',
    'social.backends.google.GoogleOpenId',
    'social.backends.google.GooglePlusAuth',
    'social.backends.google.GoogleOpenIdConnect',
    'social.backends.instagram.InstagramOAuth2',
    'social.backends.jawbone.JawboneOAuth2',
    'social.backends.linkedin.LinkedinOAuth',
    'social.backends.linkedin.LinkedinOAuth2',
    'social.backends.live.LiveOAuth2',
    'social.backends.livejournal.LiveJournalOpenId',
    'social.backends.mailru.MailruOAuth2',
    'social.backends.mendeley.MendeleyOAuth',
    'social.backends.mendeley.MendeleyOAuth2',
    'social.backends.mixcloud.MixcloudOAuth2',
    'social.backends.odnoklassniki.OdnoklassnikiOAuth2',
    'social.backends.open_id.OpenIdAuth',
    'social.backends.openstreetmap.OpenStreetMapOAuth',
    'social.backends.persona.PersonaAuth',
    'social.backends.podio.PodioOAuth2',
    'social.backends.rdio.RdioOAuth1',
    'social.backends.rdio.RdioOAuth2',
    'social.backends.readability.ReadabilityOAuth',
    'social.backends.reddit.RedditOAuth2',
    'social.backends.runkeeper.RunKeeperOAuth2',
    'social.backends.skyrock.SkyrockOAuth',
    'social.backends.soundcloud.SoundcloudOAuth2',
    'social.backends.spotify.SpotifyOAuth2',
    'social.backends.stackoverflow.StackoverflowOAuth2',
    'social.backends.steam.SteamOpenId',
    'social.backends.stocktwits.StocktwitsOAuth2',
    'social.backends.stripe.StripeOAuth2',
    'social.backends.suse.OpenSUSEOpenId',
    'social.backends.thisismyjam.ThisIsMyJamOAuth1',
    'social.backends.trello.TrelloOAuth',
    'social.backends.tripit.TripItOAuth',
    'social.backends.tumblr.TumblrOAuth',
    'social.backends.twilio.TwilioAuth',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.vk.VKOAuth2',
    'social.backends.weibo.WeiboOAuth2',
    'social.backends.xing.XingOAuth',
    'social.backends.yahoo.YahooOAuth',
    'social.backends.yahoo.YahooOpenId',
    'social.backends.yammer.YammerOAuth2',
    'social.backends.yandex.YandexOAuth2',
    'social.backends.vimeo.VimeoOAuth1',
    'social.backends.lastfm.LastFmAuth',
    'social.backends.moves.MovesOAuth2',
    'social.backends.email.EmailAuth',
    'social.backends.username.UsernameAuth',
    'django.contrib.auth.backends.ModelBackend',
    'ografy.apps.xauth.backends.IdentifierBackend',
    'ografy.apps.xauth.backends.DummyTokenBackend',
)

# Python Social Auth Configuration

# Backend documentation details:
# http://python-social-xauth.readthedocs.org/en/latest/backends/index.html

SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'

# SOCIAL_AUTH_EMAIL_FORM_URL = '/signup-email'
SOCIAL_AUTH_EMAIL_FORM_HTML = 'email_signup.html'
SOCIAL_AUTH_EMAIL_VALIDATION_FUNCTION = 'ografy.apps.xauth.mail.send_validation'
SOCIAL_AUTH_EMAIL_VALIDATION_URL = '/email-sent/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/authorize'
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/connect'

# SOCIAL_AUTH_USERNAME_FORM_URL = '/signup-username'
SOCIAL_AUTH_USERNAME_FORM_HTML = 'username_signup.html'

# SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['first_name', 'last_name', 'email', 'username']
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.mail.mail_validation',
    # 'social.pipeline.user.create_user',
    # 'social.pipeline.social_auth.associate_user',
    'ografy.apps.xauth.pipeline.associate_user_and_signal',
    # 'social.pipeline.debug.debug',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
)

# Python Social Auth Backend Configuration

# Amazon

# Backend Documentation URL:    http://python-social-xauth.readthedocs.org/en/latest/backends/amazon.html
# Signal API Management URL:    https://sellercentral.amazon.com/gp/homepage.html?ie=UTF8&*Version*=1&*entries*=0
# App ID:                       amzn1.application.58fd3472c8904397997d60895c08371d
# Access Token URL:             https://api.amazon.com/xauth/o2/tokeninfo?access_token=' . urlencode($_REQUEST['access_token']));
SOCIAL_AUTH_AMAZON_KEY = 'amzn1.application-oa2-client.eeb66ec1dc3c47529c28f85ed979ec02'
SOCIAL_AUTH_AMAZON_SECRET = 'db192c908e6d7df30af44aceb41f3521056975cd52810db066e70a204b9ddac9'

# Dropbox

# Backend Documentation URL:    http://python-social-xauth.readthedocs.org/en/latest/backends/dropbox.html#oauth2
# Signal API Management URL:    https://www.dropbox.com/developers/apps/info/89dmvfe194u7nfl
# Authorize URL:                https://www.dropbox.com/1/oauth2/authorize?client_id=<app key>&response_type=code&redirect_uri=<redirect URI>&state=<CSRF token>
# Token URL:                    https://api.dropbox.com/1/oauth2/token -d code=<authorization code> -d grant_type=authorization_code -d redirect_uri=<redirect URI> -u <app key>:<app secret>
SOCIAL_AUTH_DROPBOX_OAUTH2_KEY = '89dmvfe194u7nfl'
SOCIAL_AUTH_DROPBOX_OAUTH2_SECRET = 'ix3u2xryo4bs8b9'

# Facebook App Graph API Auth

# Backend Documentation URL:    http://python-social-xauth.readthedocs.org/en/latest/backends/facebook.html#oauth2
# Signal API Management URL:    https://developers.facebook.com/apps/296338707043090/dashboard/
# App redirect URL:             https://apps.facebook.com/YOUR_APP_NAMESPACE
SOCIAL_AUTH_FACEBOOK_KEY = '296338707043090'
SOCIAL_AUTH_FACEBOOK_SECRET = '358004e6e35ed720761aaff7b487375d'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'read_friendlists']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {}

# Faceook Auth

# Backend Documentation URL:    http://python-social-xauth.readthedocs.org/en/latest/backends/facebook.html#graph-2-0
# Signal API Management URL:    https://developers.facebook.com/apps/296338707043090/dashboard/
SOCIAL_AUTH_FACEBOOK_APP_KEY = '296338707043090'
SOCIAL_AUTH_FACEBOOK_APP_SECRET = '358004e6e35ed720761aaff7b487375d'
SOCIAL_AUTH_FACEBOOK_APP_NAMESPACE = ''

# FitBit

# Backend Documentation URL:    http://python-social-xauth.readthedocs.org/en/latest/backends/fitbit.html
# Signal API Management URL:    https://dev.fitbit.com/apps/details/229BN3
# Request Token URL:            https://api.fitbit.com/oauth/request_token
# Access Token URL:             https://api.fitbit.com/oauth/access_token
# Authorize URL:                https://www.fitbit.com/oauth/authorize
SOCIAL_AUTH_FITBIT_KEY = '72007be9664f4f13ac481335b001c520'
SOCIAL_AUTH_FITBIT_SECRET = 'a5aed45ae0f440c29f19eb4e9c2e0493'

# Foursquare

# Backend Documentation URL:    http://python-social-xauth.readthedocs.org/en/latest/backends/foursquare.html
# Signal API Management URL:    https://foursquare.com/developers/app/PSHPVDWN0NCQCUUIPUC3CQBZCDMOY4B3AYOAHGAAW1Y0V0DT
# Access Token URL              https://foursquare.com/oauth2/access_token
# Authorize URL                 https://foursquare.com/oauth2/authorize
SOCIAL_AUTH_FOURSQUARE_KEY = 'PSHPVDWN0NCQCUUIPUC3CQBZCDMOY4B3AYOAHGAAW1Y0V0DT'
SOCIAL_AUTH_FOURSQUARE_SECRET = 'EGTRPVVFLDKA4QNLN5ACS43V2B5KLSD0FSUOPYTKX3FFPA21'

# Github Auth

# Backend Documentation URL:    http://python-social-xauth.readthedocs.org/en/latest/backends/github.html
# Signal API Management URL:    https://github.com/settings/applications/139587
# Redirect URL:                 https://github.com/login/oauth/authorize?scope=user:email&client_id=<%= client_id %>
# Access token URL:             'https://github.com/login/oauth/access_token',
#                                     {:client_id => CLIENT_ID,
#                                     :client_secret => CLIENT_SECRET,
#                                     :code => session_code},
#                                     :accept => :json
SOCIAL_AUTH_GITHUB_KEY = 'af9f6b46f5b02049d4f4'
SOCIAL_AUTH_GITHUB_SECRET = '794ea7c3067051aab7f9470fdfe099703047b071'
SOCIAL_AUTH_GITHUB_SCOPE = []

# Google

# Backend Documentation URL:    http://python-social-xauth.readthedocs.org/en/latest/backends/google.html#google-oauth2
# Signal API Management URL:    https://console.developers.google.com/project/1047735864420/
# Email Aaddress:               1047735864420-j7nr84qtkag5o2pno2v19c8uv00utsq0@developer.gserviceaccount.com
# Redirect URL:                 https://accounts.google.com/o/oauth2/xauth?
#                                     scope=https://www.googleapis.com/xauth/drive.file&
#                                     state=security_token%3D138r5719ru3e1%26url%3Dhttps://oa2cb.example.com/myHome&
#                                     redirect_uri=https%3A%2F%2Fmyapp.example.com%2Fcallback&
#                                     response_type=code&
#                                     client_id=8127352506391.apps.googleusercontent.com&
#                                     approval_prompt=force&
#                                     include_granted_scopes=true
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '1047735864420-j7nr84qtkag5o2pno2v19c8uv00utsq0.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'kEnHSEacGJqX7JQOk1BQj1gR'
SOCIAL_AUTH_GOOGLE_OAUTH_SCOPE = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/userinfo.profile'
]

# Instagram

# Backend Documentation URL:    http://python-social-xauth.readthedocs.org/en/latest/backends/instagram.html
# Signal API Management URL:    http://instagram.com/developer/clients/manage/?registered=Ografy
SOCIAL_AUTH_INSTAGRAM_KEY = 'cc0103f57968493f87139269e452df61'
SOCIAL_AUTH_INSTAGRAM_SECRET = 'ce402cb985c24f5a818207316f806f50'
SOCIAL_AUTH_INSTAGRAM_AUTH_EXTRA_ARGUMENTS = {'scope': 'likes comments relationships'}

# LinkedIn

# Backend Documentation URL:    http://python-social-xauth.readthedocs.org/en/latest/backends/linkedin.html#oauth2
# Signal API Management URL:    https://www.linkedin.com/secure/developer
# Access Token URL:             POST https://www.linkedin.com/uas/oauth2/accessToken?grant_type=authorization_code
#                                     &code=AUTHORIZATION_CODE
#                                     &redirect_uri=YOUR_REDIRECT_URI
#                                     &client_id=YOUR_API_KEY
#                                     &client_secret=YOUR_SECRET_KEY
# Redirect URL:                 https://www.linkedin.com/uas/oauth2/authorization?response_type=code
#                                     &client_id=YOUR_API_KEY
#                                     &scope=SCOPE
#                                     &state=STATE
#                                     &redirect_uri=YOUR_REDIRECT_URI
# API Key:                      755c6aq5wo070o
# Secret Key:                   ZQS9Gsgw0snBotYB
SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = '588631a0-1be8-4570-9413-7be28a2aefa0'
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = '0f4b82e3-1aa8-4375-b5cf-21be8b30b0eb'
SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE = ['r_basicprofile', 'r_emailaddress']
SOCIAL_AUTH_LINKEDIN_OAUTH2_FIELD_SELECTORS = ['email-address', 'headline', 'industry']
SOCIAL_AUTH_LINKEDIN_OAUTH2_EXTRA_DATA = [('id', 'id'), ('firstName', 'first_name'), ('lastName', 'last_name'), ('emailAddress', 'email_address'), ('headline', 'headline'), ('industry', 'industry')]

# Reddit

# Backend Documentation URL:    http://python-social-xauth.readthedocs.org/en/latest/backends/reddit.html
# Signal API Management URL:    https://ssl.reddit.com/prefs/apps/
# Authorize URL:                https://ssl.reddit.com/api/v1/authorize
# developers                    hegemonbill
SOCIAL_AUTH_REDDIT_KEY = 'yVmBYysV38qrHQ'
SOCIAL_AUTH_REDDIT_SECRET = 'kPQGNdbEQyS8hsDUk21GRGosKko'
SOCIAL_AUTH_REDDIT_AUTH_EXTRA_ARGUMENTS = {'duration': 'permanent'}

# Spotify

# Backend Documentation URL:    https://developer.spotify.com/my-applications/#!/applications/1495263d3fbe4fc59f69a9a9af9f9281
# Signal API Management URL:    http://python-social-xauth.readthedocs.org/en/latest/backends/spotify.html#
# Authorize URL:                GET https://accounts.spotify.com/authorize
# Redirect URIs:                https://ografy.io/xauth
SOCIAL_AUTH_SPOTIFY_OAUTH2_KEY = '1495263d3fbe4fc59f69a9a9af9f9281'
SOCIAL_AUTH_SPOTIFY_OAUTH2_SECRET = '0aacb16969eb43a2a3a019bb2ae091d2'

# StackOverflow

# Backend Documentation URL:    http://python-social-xauth.readthedocs.org/en/latest/backends/stackoverflow.html
# Signal API Management URL:    https://stackapps.com/apps/oauth/view/3718
# Authorize URL:                https://stackexchange.com/oauth/login_success
# Redirect URL:                 https://stackexchange.com/oauth/redirect_uri
SOCIAL_AUTH_STACKOVERFLOW_KEY = 'FNiAzOP9EO2RXrfl)ttOXA(('
SOCIAL_AUTH_STACKOVERFLOW_SECRET = 'TduWUXJnEZlr6YpGnxy7CA(('
SOCIAL_AUTH_STACKOVERFLOW_API_KEY = '3718'
SOCIAL_AUTH_STACKOVERFLOW_SCOPE = []

# Steam

# Backend Documentation URL:    http://python-social-xauth.readthedocs.org/en/latest/backends/steam.html
# Signal API Management URL:    http://steamcommunity.com/dev/apikey
SOCIAL_AUTH_STEAM_API_KEY = 'F807EEE21B2D47BB0AF8AB92483F3CCC'
SOCIAL_AUTH_STEAM_EXTRA_DATA = ['player']

# Tumblr

# Backend Documentation URL:    http://python-social-xauth.readthedocs.org/en/latest/backends/tumblr.html
# Signal API Management URL:    https://www.tumblr.com/oauth/apps
# Request-token URL:            POST http://www.tumblr.com/oauth/request_token
# Authorize URL:                http://www.tumblr.com/oauth/authorize
# Access-token URL:             POST http://www.tumblr.com/oauth/access_tokenx
# Auth access-token URL:        POST https://www.tumblr.com/oauth/access_token
SOCIAL_AUTH_TUMBLR_KEY = 'aTWEANrCihZmUyfVnIlcCGSNSJEc4pQcGC3WHFQGK9DSY9CYya'
SOCIAL_AUTH_TUMBLR_SECRET = 'Uzpi2JvCdS1Gtr5GhGkHIIyXcaE6ylyU4HhuCJhyG7tKJvq7jy'

# Twitter

# Backend Documentation URL:    http://python-social-xauth.readthedocs.org/en/latest/backends/twitter.html
# Signal API Management URL:    https://apps.twitter.com/app/6086700/show
# Callback URL:                 https://oauth.io/xauth
# App-only authentication:      https://api.twitter.com/oauth2/token
# Request token URL:            https://api.twitter.com/oauth/request_token
# Authorize URL:                https://api.twitter.com/oauth/authorize
# Access token URL:             https://api.twitter.com/oauth/access_token
# Access Level:                 Read, write, and direct messages (modify app permissions)
# Owner:                        hegemonbill
# Owner ID:                     158017896
SOCIAL_AUTH_TWITTER_KEY = 'HmrZvp1vaHU1Fb7sIg7KCL0Rs'
SOCIAL_AUTH_TWITTER_SECRET = 'UnyUntGyjnGUcqpZBIpZWNsPEzG0YezaGbIhgKEWQn7n54N3dr'

# Vimeo

# Backend Documentation URL:    http://python-social-xauth.readthedocs.org/en/latest/backends/vimeo.html
# Signal API Management URL:    https://developer.vimeo.com/apps/45068
# Request Token URL:            https://api.vimeo.com/oauth/request_token
# Authorize URL                 https://api.vimeo.com/oauth/authorize
# Access Token URL:             https://api.vimeo.com/oauth/access_token
# Unauthenticated authorization header:
#                               Authorization : Basic ZmM1MDE1MDBhMDg0Y2FmMTI5NTA3OTY1NDU4OWNkYjQ4NzllZDIxYjo0YTAxYzk2YzFhZjgyNWNlMTdhZjIyYTIzN2E4NjI0YzgxNTlmMzEx
SOCIAL_AUTH_VIMEO_KEY = 'fc501500a084caf1295079654589cdb4879ed21b'
SOCIAL_AUTH_VIMEO_SECRET = '4a01c96c1af825ce17af22a237a8624c8159f311'
SOCIAL_AUTH_VIMEO_SCOPE = []
