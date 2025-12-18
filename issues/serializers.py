from rest_framework import serializers
from .models import Issue,IssueNode

#节点序列化器
class IssueNodeSerializer(serializers.ModelSerializer):
    operator_name = serializers.CharField(
        source='operator.username',
        read_only=True
    )

    image = serializers.ImageField(required=False) #返回图片地址

    class Meta:
        model = IssueNode
        fields = [
            'id',
            'node_title',
            'node_status',
            'description',
            'image',
            'operator_name',
            'created_at'
        ]

#问题追踪详情序列化器(按照时间先后排序)
class IssueDetailSerializer(serializers.ModelSerializer):
    nodes = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = [
            'id',
            'title',
            'description',
            'status',
            'nodes'
        ]

    def get_nodes(self, obj):
        nodes = obj.nodes.order_by('created_at')
        return IssueNodeSerializer(nodes, many=True).data


#Issue列表序列化器
class IssueListSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(
        source='creator.username',
        read_only=True
    )

    class Meta:
        model = Issue
        fields = [
            'id',
            'title',
            'status',
            'creator_name',
            'created_at'
        ]
