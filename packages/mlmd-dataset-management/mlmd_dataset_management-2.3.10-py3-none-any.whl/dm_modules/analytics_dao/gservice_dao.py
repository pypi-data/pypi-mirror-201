
import json
from google.auth.transport.requests import Request
from google.cloud import secretmanager
import google.auth
import os

def get_secret(secret_name, secret_version=None, project_id="mlops-315607", json_decode=True):
    if secret_version is None:
        secret_version = os.environ.get("SECRET_VERSION")
    if secret_version is None:
        # print("Configuration version is not defined (by using env var SECRET_VERSION) and is set to default value 1")
        secret_version = 1

    cred, project = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    if not cred.valid or cred.expired:
        cred.refresh(Request())	
    client = secretmanager.SecretManagerServiceClient(credentials=cred)
    name = f"projects/{project_id}/secrets/{secret_name}/versions/{secret_version}"
    res = client.access_secret_version(request={"name":name})
    if json_decode:
        return json.loads(res.payload.data.decode("UTF-8"))
    return res.payload.data.decode("UTF-8")

def get_user_info():
    from googleapiclient.discovery import build
    try:
        cred, _ = google.auth.default(scopes=['https://www.googleapis.com/auth/cloud-platform'])
        cred._quota_project_id = None
        userinfo_service = build('oauth2', 'v2', credentials=cred)
        return userinfo_service.userinfo().get().execute()
    except Exception:
        return {
            "email": "analytics-build-account@mlops-315607.iam.gserviceaccount.com"
        }