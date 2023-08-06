def parse_data(data):
    """
    data = {
        "dataset_id": <dataset_id>,
        "document_id": <document_id>,
        "model_id": <model_id>,
        "metadata": <metadata>
    }
    """
    from google.cloud import firestore

    key = data.get("model_id")
    if not key:
        raise Exception("Failed to parse data: model_id is missed")
    ret = {
        key: data.get("gt"),
        "created_at": firestore.SERVER_TIMESTAMP
    }
    required_fields = ["dataset_id", "document_id"]
    for field in required_fields:
        if data.get(field) is None:
            raise Exception("Missing require field {}".format(field))
        ret[field] = data[field]
    
    document_id = get_metadata_document_id(data["dataset_id"] , data["document_id"])
    return document_id, ret

def get_metadata_document_id(dataset_id, image_name):
    import hashlib
    document_id = "{}_{}".format(dataset_id, image_name).encode("utf-8")
    return hashlib.md5(document_id).hexdigest()

