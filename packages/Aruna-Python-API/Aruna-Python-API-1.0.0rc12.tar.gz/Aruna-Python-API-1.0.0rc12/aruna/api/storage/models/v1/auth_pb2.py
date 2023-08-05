# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: aruna/api/storage/models/v1/auth.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&aruna/api/storage/models/v1/auth.proto\x12\x1b\x61runa.api.storage.models.v1\x1a\x1fgoogle/protobuf/timestamp.proto\"\xd1\x01\n\x07Project\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x12\n\x04name\x18\x02 \x01(\tR\x04name\x12Y\n\x10user_permissions\x18\x03 \x03(\x0b\x32..aruna.api.storage.models.v1.ProjectPermissionR\x0fuserPermissions\x12%\n\x0e\x63ollection_ids\x18\x04 \x03(\tR\rcollectionIds\x12 \n\x0b\x64\x65scription\x18\x05 \x01(\tR\x0b\x64\x65scription\"\x99\x01\n\x0fProjectOverview\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x12\n\x04name\x18\x02 \x01(\tR\x04name\x12 \n\x0b\x64\x65scription\x18\x03 \x01(\tR\x0b\x64\x65scription\x12%\n\x0e\x63ollection_ids\x18\x04 \x03(\tR\rcollectionIds\x12\x19\n\x08user_ids\x18\x05 \x03(\tR\x07userIds\"\xbb\x01\n\x04User\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x1f\n\x0b\x65xternal_id\x18\x02 \x01(\tR\nexternalId\x12!\n\x0c\x64isplay_name\x18\x03 \x01(\tR\x0b\x64isplayName\x12\x16\n\x06\x61\x63tive\x18\x04 \x01(\x08R\x06\x61\x63tive\x12\x19\n\x08is_admin\x18\x05 \x01(\x08R\x07isAdmin\x12,\n\x12is_service_account\x18\x06 \x01(\x08R\x10isServiceAccount\"\xc9\x03\n\x05Token\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x12\n\x04name\x18\x02 \x01(\tR\x04name\x12\x45\n\ntoken_type\x18\x04 \x01(\x0e\x32&.aruna.api.storage.models.v1.TokenTypeR\ttokenType\x12\x39\n\ncreated_at\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tcreatedAt\x12\x39\n\nexpires_at\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\texpiresAt\x12#\n\rcollection_id\x18\x07 \x01(\tR\x0c\x63ollectionId\x12\x1d\n\nproject_id\x18\x08 \x01(\tR\tprojectId\x12G\n\npermission\x18\t \x01(\x0e\x32\'.aruna.api.storage.models.v1.PermissionR\npermission\x12\x1d\n\nis_session\x18\n \x01(\x08R\tisSession\x12\x33\n\x07used_at\x18\x0b \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x06usedAt\"\xbd\x01\n\x11ProjectPermission\x12\x17\n\x07user_id\x18\x01 \x01(\tR\x06userId\x12\x1d\n\nproject_id\x18\x02 \x01(\tR\tprojectId\x12G\n\npermission\x18\x03 \x01(\x0e\x32\'.aruna.api.storage.models.v1.PermissionR\npermission\x12\'\n\x0fservice_account\x18\x04 \x01(\x08R\x0eserviceAccount\"\xc2\x01\n\x1cProjectPermissionDisplayName\x12\x17\n\x07user_id\x18\x01 \x01(\tR\x06userId\x12\x1d\n\nproject_id\x18\x02 \x01(\tR\tprojectId\x12G\n\npermission\x18\x03 \x01(\x0e\x32\'.aruna.api.storage.models.v1.PermissionR\npermission\x12!\n\x0c\x64isplay_name\x18\x04 \x01(\tR\x0b\x64isplayName*\x96\x01\n\nPermission\x12\x1a\n\x16PERMISSION_UNSPECIFIED\x10\x00\x12\x13\n\x0fPERMISSION_NONE\x10\x01\x12\x13\n\x0fPERMISSION_READ\x10\x02\x12\x15\n\x11PERMISSION_APPEND\x10\x03\x12\x15\n\x11PERMISSION_MODIFY\x10\x04\x12\x14\n\x10PERMISSION_ADMIN\x10\x05*g\n\x08PermType\x12\x19\n\x15PERM_TYPE_UNSPECIFIED\x10\x00\x12\x12\n\x0ePERM_TYPE_USER\x10\x01\x12\x17\n\x13PERM_TYPE_ANONYMOUS\x10\x02\x12\x13\n\x0fPERM_TYPE_TOKEN\x10\x03*W\n\tTokenType\x12\x1a\n\x16TOKEN_TYPE_UNSPECIFIED\x10\x00\x12\x17\n\x13TOKEN_TYPE_PERSONAL\x10\x01\x12\x15\n\x11TOKEN_TYPE_SCOPED\x10\x02\x42<Z:github.com/ArunaStorage/go-api/aruna/api/storage/models/v1b\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'aruna.api.storage.models.v1.auth_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z:github.com/ArunaStorage/go-api/aruna/api/storage/models/v1'
  _PERMISSION._serialized_start=1512
  _PERMISSION._serialized_end=1662
  _PERMTYPE._serialized_start=1664
  _PERMTYPE._serialized_end=1767
  _TOKENTYPE._serialized_start=1769
  _TOKENTYPE._serialized_end=1856
  _PROJECT._serialized_start=105
  _PROJECT._serialized_end=314
  _PROJECTOVERVIEW._serialized_start=317
  _PROJECTOVERVIEW._serialized_end=470
  _USER._serialized_start=473
  _USER._serialized_end=660
  _TOKEN._serialized_start=663
  _TOKEN._serialized_end=1120
  _PROJECTPERMISSION._serialized_start=1123
  _PROJECTPERMISSION._serialized_end=1312
  _PROJECTPERMISSIONDISPLAYNAME._serialized_start=1315
  _PROJECTPERMISSIONDISPLAYNAME._serialized_end=1509
# @@protoc_insertion_point(module_scope)
