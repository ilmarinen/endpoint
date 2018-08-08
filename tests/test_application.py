import urllib2
from flask_testing import LiveServerTestCase

from endpoint import main


class MyTest(LiveServerTestCase):

    def create_app(self):
        main.init()
        return main.app

    def test_main_route(self):
        # Test that the main route of the app that serves
        # up the index page works.

        response = urllib2.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)

    def test_event_routes(self):
        # Test that the routes added for fielding the browsewr
        # generated web events work as expected.

        test_slug = "test-slug"

        response = urllib2.urlopen(
            "{}/{}/{}".format(self.get_server_url(), 'api/v1/event/initial', 'test-slug'))
        self.assertEqual(response.code, 200)
        self.assertEqual('"{}"'.format(test_slug), response.readline())

        response = urllib2.urlopen(
            "{}/{}/{}".format(self.get_server_url(), 'api/v1/event', 'test-slug'))
        self.assertEqual(response.code, 200)
        self.assertEqual('"{}"'.format(test_slug), response.readline())

        response = urllib2.urlopen(
            "{}/{}/{}".format(
                self.get_server_url(), 'api/v1/event/informative', 'test-slug'))
        self.assertEqual(response.code, 200)
        self.assertEqual('"{}"'.format(test_slug), response.readline())
