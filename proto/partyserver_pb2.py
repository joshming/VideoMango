# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/partyserver.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17proto/partyserver.proto\x12\x05party\x1a\x1bgoogle/protobuf/empty.proto\"?\n\x0cWatchRequest\x12\x10\n\x08\x63lientId\x18\x01 \x01(\t\x12\x0f\n\x07videoId\x18\x02 \x01(\t\x12\x0c\n\x04time\x18\x03 \x01(\x03\"\x13\n\x11WatchPartyRequest\"\x0c\n\nWatchParty\"\x0f\n\rPartyResponse\"&\n\tVideoInfo\x12\n\n\x02id\x18\x01 \x01(\x05\x12\r\n\x05title\x18\x02 \x01(\t2\xa1\x02\n\x0bPartyServer\x12\x34\n\x05watch\x12\x13.party.WatchRequest\x1a\x16.google.protobuf.Empty\x12;\n\tjoinParty\x12\x18.party.WatchPartyRequest\x1a\x14.party.PartyResponse\x12\x35\n\npauseParty\x12\x11.party.WatchParty\x1a\x14.party.PartyResponse\x12\x34\n\tplayParty\x12\x11.party.WatchParty\x1a\x14.party.PartyResponse\x12\x32\n\x07\x65ndPart\x12\x11.party.WatchParty\x1a\x14.party.PartyResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'proto.partyserver_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_WATCHREQUEST']._serialized_start=63
  _globals['_WATCHREQUEST']._serialized_end=126
  _globals['_WATCHPARTYREQUEST']._serialized_start=128
  _globals['_WATCHPARTYREQUEST']._serialized_end=147
  _globals['_WATCHPARTY']._serialized_start=149
  _globals['_WATCHPARTY']._serialized_end=161
  _globals['_PARTYRESPONSE']._serialized_start=163
  _globals['_PARTYRESPONSE']._serialized_end=178
  _globals['_VIDEOINFO']._serialized_start=180
  _globals['_VIDEOINFO']._serialized_end=218
  _globals['_PARTYSERVER']._serialized_start=221
  _globals['_PARTYSERVER']._serialized_end=510
# @@protoc_insertion_point(module_scope)
