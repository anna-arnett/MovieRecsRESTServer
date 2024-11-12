import cherrypy
from movies import MovieController
from reset import ResetController
from _mdb import Database
from users import UserController
from ratings import RatingsController
from recommendations import RecommendationsController

def start_service():
    dispatcher = cherrypy.dispatch.RoutesDispatcher()
    mdb = Database()
    
    # set controllers
    movie_controller = MovieController(mdb)
    reset_controller = ResetController(mdb)
    user_controller = UserController(mdb)
    rating_controller = RatingsController(mdb)
    recommendation_controller = RecommendationsController(mdb)
    #print("DEBUG: movies passed to MovieController:", mdb.movies)

    # set routes
    
    # movies
    dispatcher.connect('get_movie', '/movies/:movie_id', controller=movie_controller, action='GET_ITEM', conditions=dict(method=['GET']))
    dispatcher.connect('get_all', '/movies/', controller=movie_controller, action='GET_ALL', conditions=dict(method=['GET']))
    dispatcher.connect('put_movie', '/movies/:movie_id', controller=movie_controller, action='PUT_ITEM', conditions=dict(method=['PUT']))
    dispatcher.connect('post', '/movies/', controller=movie_controller, action='POST', conditions=dict(method=['POST']))
    dispatcher.connect('delete_all', '/movies/', controller=movie_controller, action='DELETE_ALL', conditions=dict(method=['DELETE']))
    dispatcher.connect('delete_item', '/movies/:movie_id', controller=movie_controller, action='DELETE_ITEM', conditions=dict(method=['DELETE']))

    # reset
    dispatcher.connect('reset_all', '/reset/', controller=reset_controller, action='PUT', conditions=dict(method=['PUT']))
    dispatcher.connect('reset_movie', '/reset/:movie_id', controller=reset_controller, action='PUT_MOVIE', conditions=dict(method=['PUT']))

    # users
    dispatcher.connect('get_all_users', '/users/', controller=user_controller, action='GET_ALL', conditions=dict(method=['GET']))
    dispatcher.connect('post_users', '/users/', controller=user_controller, action='POST', conditions=dict(method=['POST']))  
    dispatcher.connect('delete_all_users', '/users/', controller=user_controller, action='DELETE_ALL', conditions=dict(method=['DELETE'])) 
    dispatcher.connect('get_user', '/users/:user_id', controller=user_controller, action='GET_ITEM', conditions=dict(method=['GET']))
    dispatcher.connect('put_user', '/users/:user_id', controller=user_controller, action='PUT_ITEM', conditions=dict(method=['PUT']))
    dispatcher.connect('delete_user', '/users/:user_id', controller=user_controller, action='DELETE_ITEM', conditions=dict(method=['DELETE']))
 
    # ratings
    dispatcher.connect('get_rating', '/ratings/:movie_id', controller=rating_controller, action='GET_ITEM', conditions=dict(method=['GET']))

    # recommendations
    dispatcher.connect('get_recommendation', '/recommendations/:user_id', controller=recommendation_controller, action='GET_ITEM', conditions=dict(method=['GET']))
    dispatcher.connect('put_recommendation', '/recommendations/:user_id', controller=recommendation_controller, action='PUT_ITEM', conditions=dict(method=['PUT']))
    dispatcher.connect('delete_recommendations', '/recommendations/', controller=recommendation_controller, action='DELETE', conditions=dict(method=['DELETE']))
        
    conf = { 'global' : {'server.socket_host': 'student05.cse.nd.edu',
                         'server.socket_port': 52004},
             '/'      : {'request.dispatch': dispatcher} }
    cherrypy.config.update(conf)
    app = cherrypy.tree.mount(None, config=conf)
    cherrypy.quickstart(app)

if __name__ == '__main__':
    start_service()
    

