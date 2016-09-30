from paver.tasks import task
from paver.tasks import needs
from paver.easy import sh

""" 
    Particular tasks
"""

@task
def unit_tests_vs():
    sh('nosetests -vs tests/unit')
@task
def doc_tests_vs():    
    sh('nosetests --with-doctest -vs quantarhei/core')

@task
def unit_tests_v():
    sh('nosetests -v tests/unit')
    
@task
def doc_tests_v():    
    sh('nosetests --with-doctest -vs quantarhei/core quantarhei/qm/corfunctions')
    
@task
def aloe_tests_vs():
    sh("aloe -vs -a !in_development tests/bdd")

@task
def aloe_tests_v():
    sh('aloe -v -a !in_development tests/bdd')
    

"""
    Optional tasks
"""  
class Runner:  
    
    def __init__(self,path):
        self.path = path
        
    def set_path(self,path):
        self.path = path
        
    def un(self,file):
        rcfile = 'tests/pylint/pylintrc'
        sh('pylint --rcfile='+rcfile+' '+self.path+'/'+file)
    
@task
def pylint():

    path = 'quantarhei/core/'
    r = Runner(path)
#    r.un('valueaxis.py')
#    r.un('time.py')
#    r.un('frequency.py')

    path = 'quantarhei/qm/corfunctions'
    r.set_path(path)
#    r.un('correlationfunctions.py')
    r.un('spectraldensities.py')  
    
    
"""
    Default 
"""

@needs('unit_tests_v','doc_tests_v','aloe_tests_v')
@task
def default():
    pass

@needs('unit_tests_vs','doc_tests_vs','aloe_tests_vs')
@task
def vs():
    pass

@needs('unit_tests_v','aloe_tests_v')
@task
def nodoc():
    pass

@needs('unit_tests_vs','aloe_tests_vs')
@task
def nodoc_vs():
    pass

@needs('unit_tests')
@task
def windows():
    """ On windows, aloe tool does not work. We do only unit tests"""
    pass

