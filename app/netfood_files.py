
import shutil
from netfood_logging import log_debug, log_info, log_error, log_fatal
def move_file(src, dest):
    log_debug("move file "+src+" to "+dest)
    try:
        shutil.move(src, dest)
        log_info("moved file "+src+" to "+dest)
    except shutil.SameFileError as e:
        log_error("Same file "+str(e))
    except FileNotFoundError as e:
        log_error("File not found " + src)
    except IOError as e:
        log_error("IO Error "+e)
if __name__ == "__main__" : 
    from netfood_config import getConf
    confData = getConf('config.json')
    move_file( confData[ 'filesIN']+'/index.html', confData[ 'filesPROD']  )