from rest_framework import serializers
from issues.models import IssueNode, Issue, IssueImage

class IssueImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueImage
        fields = ['id', 'image', 'order']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")
        if request and instance.image:
            data["image"] = request.build_absolute_uri(instance.image.url)
        return data

class IssueNodeSerializer(serializers.ModelSerializer):
    operator_name = serializers.CharField(source='operator.username', read_only=True)

    class Meta:
        model = IssueNode
        fields = ['id','node_title','node_status','description','image','operator_name','created_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")
        if request and instance.image:
            data["image"] = request.build_absolute_uri(instance.image.url)
        return data

class IssueDetailSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source="creator.username", read_only=True)
    creator_avatar = serializers.SerializerMethodField()
    issue_pic = IssueImageSerializer(many=True, read_only=True)
    nodes = IssueNodeSerializer(many=True, read_only=True)

    class Meta:
        model = Issue
        fields = [
            "id","title","description","status",
            "created_at","updated_at",
            "creator_name","creator_avatar",
            "issue_pic","nodes",
        ]

    def get_creator_avatar(self, obj):
        request = self.context.get("request")
        avatar = getattr(obj.creator, "avatar", None)
        if not avatar:
            return None
        try:
            return request.build_absolute_uri(avatar.url)
        except:
            return None

class IssueListSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source='creator.username', read_only=True)

    class Meta:
        model = Issue
        fields = ['id','title','status','creator_name','created_at']
