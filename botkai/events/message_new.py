from .. import classes 


connection = classes.connections()

def message_new():

    
    return "ok"



def IsRegistred(id):
    sql = ("SELECT groupreal FROM users WHERE id_vk = {}".format(id))
    #connection.cursor

    