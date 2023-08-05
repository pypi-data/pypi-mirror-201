# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from ydb._grpc.v4.protos import ydb_topic_pb2 as protos_dot_ydb__topic__pb2


class TopicServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.StreamWrite = channel.stream_stream(
                '/Ydb.Topic.V1.TopicService/StreamWrite',
                request_serializer=protos_dot_ydb__topic__pb2.StreamWriteMessage.FromClient.SerializeToString,
                response_deserializer=protos_dot_ydb__topic__pb2.StreamWriteMessage.FromServer.FromString,
                )
        self.StreamRead = channel.stream_stream(
                '/Ydb.Topic.V1.TopicService/StreamRead',
                request_serializer=protos_dot_ydb__topic__pb2.StreamReadMessage.FromClient.SerializeToString,
                response_deserializer=protos_dot_ydb__topic__pb2.StreamReadMessage.FromServer.FromString,
                )
        self.CreateTopic = channel.unary_unary(
                '/Ydb.Topic.V1.TopicService/CreateTopic',
                request_serializer=protos_dot_ydb__topic__pb2.CreateTopicRequest.SerializeToString,
                response_deserializer=protos_dot_ydb__topic__pb2.CreateTopicResponse.FromString,
                )
        self.DescribeTopic = channel.unary_unary(
                '/Ydb.Topic.V1.TopicService/DescribeTopic',
                request_serializer=protos_dot_ydb__topic__pb2.DescribeTopicRequest.SerializeToString,
                response_deserializer=protos_dot_ydb__topic__pb2.DescribeTopicResponse.FromString,
                )
        self.DescribeConsumer = channel.unary_unary(
                '/Ydb.Topic.V1.TopicService/DescribeConsumer',
                request_serializer=protos_dot_ydb__topic__pb2.DescribeConsumerRequest.SerializeToString,
                response_deserializer=protos_dot_ydb__topic__pb2.DescribeConsumerResponse.FromString,
                )
        self.AlterTopic = channel.unary_unary(
                '/Ydb.Topic.V1.TopicService/AlterTopic',
                request_serializer=protos_dot_ydb__topic__pb2.AlterTopicRequest.SerializeToString,
                response_deserializer=protos_dot_ydb__topic__pb2.AlterTopicResponse.FromString,
                )
        self.DropTopic = channel.unary_unary(
                '/Ydb.Topic.V1.TopicService/DropTopic',
                request_serializer=protos_dot_ydb__topic__pb2.DropTopicRequest.SerializeToString,
                response_deserializer=protos_dot_ydb__topic__pb2.DropTopicResponse.FromString,
                )


class TopicServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def StreamWrite(self, request_iterator, context):
        """Create Write Session
        Pipeline example:
        client                  server
        InitRequest(Topic, MessageGroupID, ...)
        ---------------->
        InitResponse(Partition, MaxSeqNo, ...)
        <----------------
        WriteRequest(data1, seqNo1)
        ---------------->
        WriteRequest(data2, seqNo2)
        ---------------->
        WriteResponse(seqNo1, offset1, ...)
        <----------------
        WriteRequest(data3, seqNo3)
        ---------------->
        WriteResponse(seqNo2, offset2, ...)
        <----------------
        [something went wrong] (status != SUCCESS, issues not empty)
        <----------------
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StreamRead(self, request_iterator, context):
        """Create Read Session
        Pipeline:
        client                  server
        InitRequest(Topics, ClientId, ...)
        ---------------->
        InitResponse(SessionId)
        <----------------
        ReadRequest
        ---------------->
        ReadRequest
        ---------------->
        StartPartitionSessionRequest(Topic1, Partition1, PartitionSessionID1, ...)
        <----------------
        StartPartitionSessionRequest(Topic2, Partition2, PartitionSessionID2, ...)
        <----------------
        StartPartitionSessionResponse(PartitionSessionID1, ...)
        client must respond with this message to actually start recieving data messages from this partition
        ---------------->
        StopPartitionSessionRequest(PartitionSessionID1, ...)
        <----------------
        StopPartitionSessionResponse(PartitionSessionID1, ...)
        only after this response server will give this parittion to other session.
        ---------------->
        StartPartitionSessionResponse(PartitionSession2, ...)
        ---------------->
        ReadResponse(data, ...)
        <----------------
        CommitRequest(PartitionCommit1, ...)
        ---------------->
        CommitResponse(PartitionCommitAck1, ...)
        <----------------
        [something went wrong] (status != SUCCESS, issues not empty)
        <----------------
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateTopic(self, request, context):
        """Create topic command.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DescribeTopic(self, request, context):
        """Describe topic command.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DescribeConsumer(self, request, context):
        """Describe topic's consumer command.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AlterTopic(self, request, context):
        """Alter topic command.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DropTopic(self, request, context):
        """Drop topic command.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TopicServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'StreamWrite': grpc.stream_stream_rpc_method_handler(
                    servicer.StreamWrite,
                    request_deserializer=protos_dot_ydb__topic__pb2.StreamWriteMessage.FromClient.FromString,
                    response_serializer=protos_dot_ydb__topic__pb2.StreamWriteMessage.FromServer.SerializeToString,
            ),
            'StreamRead': grpc.stream_stream_rpc_method_handler(
                    servicer.StreamRead,
                    request_deserializer=protos_dot_ydb__topic__pb2.StreamReadMessage.FromClient.FromString,
                    response_serializer=protos_dot_ydb__topic__pb2.StreamReadMessage.FromServer.SerializeToString,
            ),
            'CreateTopic': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateTopic,
                    request_deserializer=protos_dot_ydb__topic__pb2.CreateTopicRequest.FromString,
                    response_serializer=protos_dot_ydb__topic__pb2.CreateTopicResponse.SerializeToString,
            ),
            'DescribeTopic': grpc.unary_unary_rpc_method_handler(
                    servicer.DescribeTopic,
                    request_deserializer=protos_dot_ydb__topic__pb2.DescribeTopicRequest.FromString,
                    response_serializer=protos_dot_ydb__topic__pb2.DescribeTopicResponse.SerializeToString,
            ),
            'DescribeConsumer': grpc.unary_unary_rpc_method_handler(
                    servicer.DescribeConsumer,
                    request_deserializer=protos_dot_ydb__topic__pb2.DescribeConsumerRequest.FromString,
                    response_serializer=protos_dot_ydb__topic__pb2.DescribeConsumerResponse.SerializeToString,
            ),
            'AlterTopic': grpc.unary_unary_rpc_method_handler(
                    servicer.AlterTopic,
                    request_deserializer=protos_dot_ydb__topic__pb2.AlterTopicRequest.FromString,
                    response_serializer=protos_dot_ydb__topic__pb2.AlterTopicResponse.SerializeToString,
            ),
            'DropTopic': grpc.unary_unary_rpc_method_handler(
                    servicer.DropTopic,
                    request_deserializer=protos_dot_ydb__topic__pb2.DropTopicRequest.FromString,
                    response_serializer=protos_dot_ydb__topic__pb2.DropTopicResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Ydb.Topic.V1.TopicService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class TopicService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def StreamWrite(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/Ydb.Topic.V1.TopicService/StreamWrite',
            protos_dot_ydb__topic__pb2.StreamWriteMessage.FromClient.SerializeToString,
            protos_dot_ydb__topic__pb2.StreamWriteMessage.FromServer.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StreamRead(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/Ydb.Topic.V1.TopicService/StreamRead',
            protos_dot_ydb__topic__pb2.StreamReadMessage.FromClient.SerializeToString,
            protos_dot_ydb__topic__pb2.StreamReadMessage.FromServer.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateTopic(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Ydb.Topic.V1.TopicService/CreateTopic',
            protos_dot_ydb__topic__pb2.CreateTopicRequest.SerializeToString,
            protos_dot_ydb__topic__pb2.CreateTopicResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DescribeTopic(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Ydb.Topic.V1.TopicService/DescribeTopic',
            protos_dot_ydb__topic__pb2.DescribeTopicRequest.SerializeToString,
            protos_dot_ydb__topic__pb2.DescribeTopicResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DescribeConsumer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Ydb.Topic.V1.TopicService/DescribeConsumer',
            protos_dot_ydb__topic__pb2.DescribeConsumerRequest.SerializeToString,
            protos_dot_ydb__topic__pb2.DescribeConsumerResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AlterTopic(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Ydb.Topic.V1.TopicService/AlterTopic',
            protos_dot_ydb__topic__pb2.AlterTopicRequest.SerializeToString,
            protos_dot_ydb__topic__pb2.AlterTopicResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DropTopic(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Ydb.Topic.V1.TopicService/DropTopic',
            protos_dot_ydb__topic__pb2.DropTopicRequest.SerializeToString,
            protos_dot_ydb__topic__pb2.DropTopicResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
