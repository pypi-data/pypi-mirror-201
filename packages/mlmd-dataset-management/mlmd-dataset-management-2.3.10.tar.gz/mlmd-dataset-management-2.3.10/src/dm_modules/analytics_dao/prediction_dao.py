from dm_modules.analytics_dao.db import get_connection, get_collection_name

db_client = get_connection()

def insert_prediction(collection_name, document_id, prediction_data):
    return db_client.collection(collection_name).document(document_id).set(prediction_data, merge=True)


def get_prediction_gen(execution_id, context="prediction"):
    """
    Get prediction generator for a given execution_id and context from firestore
    @param execution_id: execution_id
    @param context: prediction or test (default: prediction)
    @return: prediction generator
    """
    from dm_modules.analytics_dao.moap_execution_dao import get_moap_execution
    if "test" in execution_id or context == "test":
        collection_name = "test_predictions"
    else:
        moap_exe = get_moap_execution(execution_id)
        collection_name = get_collection_name(context, moap_exe.get("env"))
    if not collection_name:
        print("Collection name not found")
        return None
    return db_client.collection(collection_name).where(u'execution_id', u'==', execution_id).stream()
    
# gen = get_prediction_gen("0c98f489587448c789be2db7b95f8ab4")
# for doc in gen:
#     print(doc.to_dict())

# from dm_modules.analytics_dao.moap_execution_dao import get_moap_execution

# moap_exe = get_moap_execution("4c2c419b052844ae8e99169b8451a3d9")
# print(moap_exe)