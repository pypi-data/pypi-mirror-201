from google.cloud import firestore

def get_connection(project_id="mlops-315607"):
    db = firestore.Client(project=project_id)
    return db

def get_collection_name(context, env_name):
    if context == "prediction":
        if not env_name:
            return None
        return "{}_ds_predictions".format(env_name)
    if context == "groundtruth":
        return "ds_groundtruth"
    if context == "metadata":
        return "ds_metadata"
    return None