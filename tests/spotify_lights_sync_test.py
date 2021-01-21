from appdaemontestframework import automation_fixture
import secrets
from apps.spotify_lights_sync.spotify_lights_sync import SpotifyLightsSync


@automation_fixture(SpotifyLightsSync)
def spotify_lights_sync(given_that):
    given_that.passed_arg('client_id').is_set_to(secrets.CLIENT_ID)
    given_that.passed_arg('client_secret').is_set_to(secrets.CLIENT_SECRET)
    given_that.passed_arg('media_player').is_set_to('media_player.spotify_test')
    given_that.passed_arg('light').is_set_to('light.test_light')

    given_that.passed_arg('color_profile').is_set_to('custom')
    given_that.passed_arg('custom_profile').is_set_to([
        {'point': [0, 0], 'color': [0, 0, 255]},
        {'point': [1, 0], 'color': [0, 255, 0]},
        {'point': [0, 1], 'color': [255, 0, 0]},
        {'point': [1, 1], 'color': [255, 255, 0]},
    ])


def test_callbacks_are_set(given_that, spotify_lights_sync: SpotifyLightsSync, assert_that):
    assert_that(spotify_lights_sync).\
        listens_to.state('media_player.spotify_test', attribute="media_content_id").\
        with_callback(spotify_lights_sync.sync_lights)


def test_custom_color_profile(given_that, spotify_lights_sync: SpotifyLightsSync, assert_that):
    spotify_lights_sync.sync_lights_debug((0, 0))

    assert_that('light.test_light').was.turned_on(rgb_color=[0, 0, 255])
