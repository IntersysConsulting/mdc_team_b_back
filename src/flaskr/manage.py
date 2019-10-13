from jwtholder import *
from flask_script import Manager

from time import sleep
import threading

manager = Manager(app)

@manager.command
def run():
    """Like a 'runserver' command but shorter, lol."""
    print(str(app))
    app.run()


@manager.command
def run_tests():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def travis_test():
    pass
    #threading.Thread(target=app.run)
    


@manager.command
def debug_fix():
    """
    I have trouble with hitting breakpoints in flask-RESTful class methods.
    This method help me.
    """
    app.config['DEBUG'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.run(debug=False)


@manager.command
def db_init():
    #db.create_all()
    pass


if __name__ == '__main__':
    manager.run()