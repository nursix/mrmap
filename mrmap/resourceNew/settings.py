from resourceNew.enums.service import OGCOperationEnum

SECURE_ABLE_WMS_OPERATIONS = [OGCOperationEnum.GET_MAP.value,
                              OGCOperationEnum.GET_FEATURE_INFO.value]
SECURE_ABLE_WFS_OPERATIONS = [OGCOperationEnum.GET_FEATURE.value,
                              OGCOperationEnum.TRANSACTION.value]
SECURE_ABLE_OPERATIONS = SECURE_ABLE_WMS_OPERATIONS + SECURE_ABLE_WFS_OPERATIONS
SECURE_ABLE_OPERATIONS_LOWER = [operation.lower() for operation in SECURE_ABLE_OPERATIONS]
