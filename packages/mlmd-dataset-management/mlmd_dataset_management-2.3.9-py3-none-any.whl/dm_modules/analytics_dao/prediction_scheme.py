
def parse_from_message(message, consumer_name):
    from google.cloud import firestore
    import datetime

    key = "{}_output".format(consumer_name)
    ret = {
        key:message[key],
        "created_at": firestore.SERVER_TIMESTAMP,
        "expire_at": str(datetime.datetime.now() + datetime.timedelta(days=120))
    }
    required_fields = ["execution_id", "mission_id", "document_id"]
    for field in required_fields:
        if message.get(field) is None:
            raise Exception("Missing require field {}".format(field))
        ret[field] = message[field]
    
    optional_fields = ["document_hash"]
    for optional_field in optional_fields:
        if message.get(optional_field) is not None:
            ret[optional_field] = message[optional_field]

    document_id = get_db_document_id(message["execution_id"], message["document_id"])
    return document_id, ret

def from_raw_prediction(model_id, raw_prediction, execution_id, dataset_name, image_name):
    from google.cloud import firestore
    import datetime
    import json
    ret = {
        "{}_output".format(model_id): json.dumps(raw_prediction),
        "execution_id": execution_id,
        "mission_id": dataset_name,
        "document_id": image_name,
        "created_at": firestore.SERVER_TIMESTAMP,
        "expire_at": str(datetime.datetime.now() + datetime.timedelta(days=120))
    }
    document_id = get_db_document_id(execution_id, image_name)
    return document_id, ret


def get_db_document_id(execution_id, image_name):
    import hashlib
    document_id = "{}_{}".format(execution_id, image_name).encode("utf-8")
    return hashlib.md5(document_id).hexdigest()
