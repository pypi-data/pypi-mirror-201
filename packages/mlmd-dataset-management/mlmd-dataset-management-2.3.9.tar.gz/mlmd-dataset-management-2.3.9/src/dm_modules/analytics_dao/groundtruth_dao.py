from dm_modules.analytics_dao.db import get_connection, get_collection_name

db_client = get_connection()

def insert_groundtruth(groundtruth_data):
    collection_name = get_collection_name("groundtruth", None)
    from dm_modules.analytics_dao.groundtruth_scheme import parse_data
    document_id, decorated_data = parse_data(groundtruth_data)
    return db_client.collection(collection_name).document(document_id).set(decorated_data, merge=True)

def get_groundtruth_gen(dataset_id, model_id):
    collection_name = get_collection_name("groundtruth", None)
    if not collection_name:
        return None
    return db_client.collection(collection_name).where(u'dataset_id', u'==', dataset_id).where(u'model_id', u'==', model_id).stream()

# took from: https://stackoverflow.com/a/61663938/13375654
def get_groundtruth_gen_with_batches(dataset_id, batch_size=5000, cursor = None):
    """
    This function is used to get the groundtruth data using batch document retrievals.
    This can overcome the 503 timeout error from firestore when querying the large dataset.

    :param dataset_id: The dataset id
    :param batch_size: The batch size
    :param cursor: The cursor
    :return: The generator of groundtruth data. 
    """

    collection_name = get_collection_name("groundtruth", None)
    query = db_client.collection(collection_name).where(u'dataset_id', u'==', dataset_id).limit(batch_size)
    while True:
        docs = []  # Very important. This frees the memory incurred in the recursion algorithm.
        if cursor:
            docs = [snapshot for snapshot in
                    query.start_after(cursor).stream()]
        else:
            docs = [snapshot for snapshot in query.stream()]

        for doc in docs:
            yield doc

        if len(docs) == batch_size:
            cursor = docs[batch_size-1]
            continue
        break

# dataset_name = "test_moap_ir_hotspot_det_0"
# gen = get_groundtruth_gen(dataset_name)
# for item in gen:
#     print(item.to_dict())

# took from: https://stackoverflow.com/a/61663938/13375654
def get_groundtruth_gen_by_dataset_id_with_batches(dataset_id, batch_size=5000, cursor = None):
    """
    This function is used to get the groundtruth data using batch document retrievals.
    This can overcome the 503 timeout error from firestore when querying the large dataset.

    :param dataset_id: The dataset id
    :param batch_size: The batch size
    :param cursor: The cursor
    :return: The generator of groundtruth data. 
    """

    collection_name = get_collection_name("groundtruth", None)
    query = db_client.collection(collection_name).where(u'dataset_id', u'==', dataset_id).limit(batch_size)
    while True:
        docs = []  # Very important. This frees the memory incurred in the recursion algorithm.
        if cursor:
            docs = [snapshot for snapshot in
                    query.start_after(cursor).stream()]
        else:
            docs = [snapshot for snapshot in query.stream()]

        for doc in docs:
            yield doc

        if len(docs) == batch_size:
            cursor = docs[batch_size-1]
            continue
        break


def get_groundtruth_by_model_id(model_id):
    collection_name = get_collection_name("groundtruth", None)
    if not collection_name:
        return None
    return db_client.collection(collection_name).where(u'model_id', u'==', model_id).stream()

def get_groundtruth_by_dataset_id(dataset_id):
    collection_name = get_collection_name("groundtruth", None)
    if not collection_name:
        return None
    return db_client.collection(collection_name).where(u'dataset_id', u'==', dataset_id).stream()


def get_groundtruth_by_dataset_id(dataset_id):
    collection_name = get_collection_name("groundtruth", None)
    if not collection_name:
        return None
    return db_client.collection(collection_name).where(u'dataset_id', u'==', dataset_id).stream()

def get_groundtruth():
    collection_name = get_collection_name("groundtruth", None)
    if not collection_name:
        return None
    return db_client.collection(collection_name).stream()

def get_groundtruth_gen_with_batches(batch_size=5000, cursor = None):
    """
    This function is used to get the groundtruth data using batch document retrievals.
    This can overcome the 503 timeout error from firestore when querying the large dataset.

    :param batch_size: The batch size
    :param cursor: The cursor
    :return: The generator of groundtruth data. 
    """

    collection_name = get_collection_name("groundtruth", None)
    query = db_client.collection(collection_name).limit(batch_size)
    while True:
        docs = []  # Very important. This frees the memory incurred in the recursion algorithm.
        if cursor:
            docs = [snapshot for snapshot in
                    query.start_after(cursor).stream()]
        else:
            docs = [snapshot for snapshot in query.stream()]

        for doc in docs:
            yield doc

        if len(docs) == batch_size:
            cursor = docs[batch_size-1]
            continue
        break
