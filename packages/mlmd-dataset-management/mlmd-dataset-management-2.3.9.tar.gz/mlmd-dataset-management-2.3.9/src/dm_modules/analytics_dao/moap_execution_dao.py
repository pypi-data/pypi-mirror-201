import os
import uuid
import json
from dm_modules.analytics_dao.dbms import execute_query, execute_select_query

def create_moap_execution(mission_id, invoked_by, tenant_key):
    env = os.environ.get("ENV_NAME")
    moap_version = None # try to read moap_version from source
    if not moap_version:
        moap_version = 1
    assert env is not None
    assert moap_version is not None
    
    moap_execution_id = uuid.uuid4().hex
    raw_execution_id = execute_query("INSERT INTO moap_execution(execution_id, mission_id, invoked_by, moap_version) values (%s,%s,%s,%s)", 
        [(
            moap_execution_id,
            mission_id,
            invoked_by,
            moap_version,
    )])

    if raw_execution_id is None or not raw_execution_id:
        print("Failed to insert execution to db")
        return False
    
    print("Created moap_execution={}, mission={}, invoker={}, moap_version={}".format(moap_execution_id, mission_id, invoked_by, moap_version))
    return moap_execution_id

def update_moap_execution(moap_execution_id, moap_status, execution_metrics):
    # execution_metrics: dict type represent the json fields to be updated
    query = "UPDATE moap_execution set moap_status=%s, execution_metrics=JSON_MERGE_PATCH(COALESCE(`execution_metrics`, '{}'), %s) WHERE execution_id=%s"
    return execute_query(query, [(moap_status, json.dumps(execution_metrics),moap_execution_id,)])

def get_moap_execution(moap_execution_id):
    query = "SELECT execution_id, moap_status, execution_metrics FROM moap_execution WHERE execution_id=%(execution_id)s"
    r = execute_select_query(query, {"execution_id": moap_execution_id})
    if not r or len(r) <= 0:
        return None
    r = r[0]
    if r:
        return {
            "status": r[1],
            **json.loads(r[2])
        }

# print(get_moap_execution("579ffa8194eb4e4ea70e030fd95d0d59"))