from data_access_connections import data_access_factory
from enums import *
data_access = data_access_factory(ServerConfig.data_access_type)

study_id = 967;
result = data_access.deleteAllAnalysis(study_id)
if result:
        print result

