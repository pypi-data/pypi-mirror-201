from dm_modules.analytics_dao.db import get_connection, get_collection_name

db_client = get_connection()

def insert_metadata(metadata):
    collection_name = get_collection_name("metadata", None)
    from dm_modules.analytics_dao.metadata_scheme import parse_data
    document_id, decorated_data = parse_data(metadata)
    return db_client.collection(collection_name).document(document_id).set(decorated_data, merge=True)

def get_metadata_gen(dataset_id):
    collection_name = get_collection_name("metadata", None)
    if not collection_name:
        return None
    return db_client.collection(collection_name).where(u'dataset_id', u'==', dataset_id).stream()