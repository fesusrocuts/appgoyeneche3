from appbase import app
from appbase import *
from appfirebase import *
from formFromUrl import *
from appextra import *
from apptemplates import *
from mailhtml import *
from appexcel import *


################################################################
########################## load service ########################
################################################################
if __name__ == '__main__':
    app.run(debug=debug, threaded=True, host=host, port=port)
################################################################
########################## load service end ####################
################################################################
