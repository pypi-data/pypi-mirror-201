from IDMConnector import ConnectorClass
import time, json, logging, mysql.connector
from datetime import timedelta

logger = logging.getLogger()

#######################
#  Initialize_IDM_DB  #
#######################
class Initialize_IDM_DB(object):
    # To initiate a database connection
    # Creating a variable to call the connection object
    def __init__(self, db_local):
        logger.debug("--inside:Initialize_IDM_DB() init--")
        self.db_local = db_local
        self.db_conn = None
        self.db_cursor = None

    # This ensure, whenever an object is created using "with"
    # this magic method is called, where you can create the connection.
    def __enter__(self):        
        self.db_conn = mysql.connector.connect(**self.db_local)
        self.db_cursor = self.db_conn.cursor(dictionary=True)
        return self

    # once the with block is over, the __exit__ method would be called
    # with that, you close the connnection
    def __exit__(self, exception_type, exception_val, trace):        
        try:
           self.db_cursor.close()
           self.db_conn.close()
        except AttributeError: # isn't closable           
           return True # exception handled successfully
        
    # To perform operations such as create, update, delete etc. 
    # To retrieve all reconcilation data from IDM database.    
    def retrieve_reconciliation_data(self, mappingid, log_level):  
        logger.setLevel(log_level)     
        logger.debug("inside:Initialize_IDM_DB() , reconciliation_for_operation() func:")    
        self.db_cursor.execute("SELECT * FROM reconcile_sync_data WHERE mapping_id=%s"%(mappingid))
        self.result = self.db_cursor.fetchall()
        return self.result
    
    # To update reconciliation statistics whether success of the operation causes a mid-operation error.
    # Passing the statics message and update the message for each reconcilation operations.
    def update_reconciliation_statistics(self, mappingid, json_data, actions, data):
        logger.debug("inside:Initialize_IDM_DB() , update_reconciliation_statistics() func:")        
        update_query = "UPDATE reconcile_sync_data SET statistics=%s WHERE mapping_id = %s AND reconcile_data = %s AND actions = %s"
        values = (       
            data,          
            mappingid,
            json_data,
            actions
        )
        self.db_cursor.execute(update_query, values)
        self.db_conn.commit()
        
#######################
#  IDMOperationClass  #
#######################
class IDMOperationClass(object):

    # This initialization is used to create an object for the IDMConnector to call the inside of the class methods.
    def __init__(self, configobject):
        self.idm_operation_obj = ConnectorClass(configobject)
    
    # This method tries several times to get the connection back from the server.
    # 'True' is returned. If connection is back.
    # 'None' is returned. If the connection is not connected after several attempts
    def retry_attempt(self, config_param=None, max_attempt=None, delay=5):
        i = 0
        for attempt in range(1, max_attempt+1):
            i = i+1
            try:
                result = self.idm_operation_obj.testConfig(config_param)
                logger.info(f"retry_attempt() func: try attempt-{i}")
                if(result["status"]):
                    logger.info(f"retry_attempt() func: succeed-{i}")
                    logger.debug(result)
                    self.__init__(config_param)
                    return result["status"]
            except Exception as e:
                if attempt < max_attempt:
                    time.sleep(delay)
                    logger.info(f"retry_attempt() func: exception attempt-{i}")
                    logger.error(str(e))
        return None

    # sync method used to perform create, update, delete operations.
    # Update success/exception for each reconcilation.
    # When the connection is disconnected from the server side during mid-operation, retry the connection.
    # Calculating the reconcilation time is how long it takes to complete all the tasks.
    # Finally return the reconcilation total duration and sync status.    
    def sync(self, mappingid, config_data, log_level, db_config, secret_key) -> dict:                
        logger.setLevel(log_level)
        logger.debug("inside:ConnectorClass() , sync() func:")
        # Get a secret from vault server           
        db_config["passwd"] = secret_key    
        start_time = time.time()      
        msg = "success"
        current_obj_id = 0        
        # Processed Operation records
        processed_operation = set()
        # DB Sync operation call
        with Initialize_IDM_DB(db_config) as obj:
            response = obj.retrieve_reconciliation_data(mappingid, log_level)
            while current_obj_id < len(response):
                obj = response[current_obj_id]
                logger.debug(f"response obj:{obj['id']}")
                logger.debug(f"Processed Operation:{processed_operation}")
                try:
                    logger.debug(f"obj{obj['id']}_currentObj{current_obj_id}")
                    if(obj['actions'] == "create"):
                        json_create_data = obj['reconcile_data']
                        logger.debug("inside:ConnectorClass() , sync() func if create try:")
                        createOp_response = self.idm_operation_obj.create(json.loads(obj['reconcile_data']))
                        with Initialize_IDM_DB(db_config) as dbObj:
                            dbObj.update_reconciliation_statistics(mappingid, json_create_data, obj['actions'], msg)
                    elif(obj['actions'] == "update"):
                        json_update_data = obj['reconcile_data']
                        logger.debug("inside:ConnectorClass() , sync() func elif update try:")
                        updateOp_response = self.idm_operation_obj.update(json.loads(obj['reconcile_data']))
                        with Initialize_IDM_DB(db_config) as dbObj:
                            dbObj.update_reconciliation_statistics(mappingid, json_update_data, obj['actions'], msg)
                    elif(obj['actions'] == "delete"):
                        json_delete_data = obj['reconcile_data']
                        logger.debug("inside:ConnectorClass() , sync() func elif delete try:")
                        deleteOp_response = self.idm_operation_obj.delete(json.loads(obj['reconcile_data']))
                        with Initialize_IDM_DB(db_config) as dbObj:
                            dbObj.update_reconciliation_statistics(mappingid, json_delete_data, obj['actions'], msg)
                    processed_operation.add(obj['id'])
                    current_obj_id += 1
                except Exception as e:
                    logger.debug("inside:ConnectorClass() , sync() except Exception:")
                    logger.warning(str(e))
                    with Initialize_IDM_DB(db_config) as dbObj:
                        dbObj.update_reconciliation_statistics(mappingid, obj['reconcile_data'], obj['actions'], str(e))
                    try:
                        # Check the connection if any exception occurs
                        conn_test_res = self.idm_operation_obj.testConfig(config_data)
                        if conn_test_res["status"]:
                            logger.debug(f"connection is available,try response_obj_operation:{obj['id']}")
                            self.idm_operation_obj.__init__(config_data)
                            current_obj_id += 1
                    except Exception as e:
                        # if testConfig() is false try again
                        logger.info(f"Re-attempt before check, response_obj_operation:{obj['id']}")
                        conn_attempt_resp = self.retry_attempt(config_param=config_data, max_attempt=int(config_data['retry']))
                        if(conn_attempt_resp and conn_attempt_resp is not None):
                            logger.info(f"Re-attempt if conn true, response_obj_operation:{obj['id']}")
                            current_obj_id -= 1
                        else:
                            logger.info(f"Many re-attempt connectivity failed, response_obj_operation:{obj['id']}")
                            return {"error": "Please check the target application server connectivity. Many attempt could not connected!."}

        end_time = time.time()
        duration = end_time - start_time
        duration_str = str(timedelta(seconds=duration))
        return {"total_duration":duration_str, "status": "sync done!"}