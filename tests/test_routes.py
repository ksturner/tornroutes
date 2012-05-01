
# make sure we get our local tornroutes before anything else
import sys, os.path
sys.path = [os.path.abspath(os.path.dirname(__file__))] + sys.path

import unittest
import tornado.web

from tornroutes import route, route_redirect

# NOTE - right now, the route_redirect function is not tested.

class RouteTests(unittest.TestCase):

    def setUp(self):
        @route('/xyz')
        class XyzFake(object):
            pass

        route_redirect('/redir_elsewhere', '/abc')

        @route('/abc', name='abc')
        class AbcFake(object):
            pass

        route_redirect('/other_redir', '/abc', name='other')

    def tearDown(self):
        r = route.get_routes()
        r.clear()

    def test_num_routes(self):
        self.assertEqual(len(route.get_routes()['']),4) # 2 routes + 2 redir

    def test_routes_ordering(self):
        # our third handler's url route should be '/abc'
        self.assertTrue( route.get_routes()[''][2].reverse() == '/abc' )

    def test_routes_name(self):
        # our first handler's url route should be '/xyz'
        host_routes = route.get_routes()
        t = tornado.web.Application([], {})
        for host, routes in host_routes.iteritems():
            t.add_handlers(host, routes)

        self.assertTrue( t.reverse_url('abc') )
        self.assertTrue( t.reverse_url('other') )

    def test_hosts(self):
        host_routes = route.get_routes()
        self.assertEqual( len(host_routes.keys()), 1 )

        h = 'blah.somewhere.com'

        @route('/abc', host=h)
        class AbcFake2(object):
            pass
        host_routes = route.get_routes()
        self.assertEqual( len(host_routes.keys()), 2 )
        self.assertTrue( h in host_routes.keys() )

        t = tornado.web.Application([], {})
        for host, routes in host_routes.iteritems():
            t.add_handlers(host, routes)

