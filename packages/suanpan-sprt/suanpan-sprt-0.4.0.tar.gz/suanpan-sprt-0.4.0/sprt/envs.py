import os

userId = os.environ.get('SP_USER_ID')
appId = os.environ.get('SP_APP_ID')
nodeId = None

# Api
host = os.environ.get('SP_HOST')
accessSecret = os.environ.get('SP_ACCESS_SECRET')
userIdHeaderField = os.environ.get('SP_USER_ID_HEADER_FIELD', 'x-sp-user-id')
userSignatureHeaderField = os.environ.get('SP_USER_SIGNATURE_HEADER_FIELD', 'x-sp-signature')
userSignVersionHeaderField = os.environ.get('SP_USER_SIGN_VERSION_HEADER_FIELD', 'x-sp-sign-version')

# Logkit
logkitUri = os.environ.get('SP_LOGKIT_URI', '')
logkitNamespace = os.environ.get('SP_LOGKIT_NAMESPACE', '/logkit')
logkitPath = os.environ.get('SP_LOGKIT_PATH', '')
logkitEventsAppend = os.environ.get('SP_LOGKIT_EVENTS_APPEND', 'append')
logkitLogsLevel = os.environ.get('SP_LOGKIT_LOGS_LEVEL', 'warning')

# storage
storageType = os.environ.get('SP_STORAGE_TYPE', '')
storageEndpoint = os.environ.get('SP_STORAGE_ENDPOINT', '')
storageBucket = os.environ.get('SP_STORAGE_BUCKET', '')
storageAccessId = os.environ.get('SP_STORAGE_ACCESS_ID', '')
storageAccessSecret = os.environ.get('SP_STORAGE_ACCESS_SECRET', '')
storageRootPath = os.environ.get('SP_STORAGE_ROOT_PATH', '/')
storageTempStore = os.environ.get('SP_STORAGE_TEMP_STORE', '')
storageGlobalStore = os.environ.get('SP_STORAGE_GLOBAL_STORE', '')
