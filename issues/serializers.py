from rest_framework import serializers
from issues.models import IssueNode, Issue, IssueImage

DEFAULT_NICKNAME = "A_Guest"
DEFAULT_AVATAR_URL = "/media/default/default_avatar.jpg"


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
    operator_name = serializers.CharField(source='operator.nickname', read_only=True)

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
    nickname = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    issue_pic = IssueImageSerializer(many=True, read_only=True)
    nodes = IssueNodeSerializer(many=True, read_only=True)
    createTime = serializers.DateTimeField(source='created_at', format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Issue
        fields = [
            "id","title","description","status",
            "createTime","updated_at",
            "nickname","avatar",
            "issue_pic","nodes",
        ]

    def get_nickname(self, obj):
        nickname = getattr(obj.creator, "nickname", None)
        if not nickname or nickname.strip() == "":
            return DEFAULT_NICKNAME
        return nickname

    def get_avatar(self, obj):
        request = self.context.get("request")
        avatar = getattr(obj.creator, "avatar", None)

        if avatar:
            try:
                return request.build_absolute_uri(avatar.url)
            except:
                pass

        # 默认头像返回完整 URL（继续支持构造外链）
        if request:
            return request.build_absolute_uri(DEFAULT_AVATAR_URL)
        return DEFAULT_AVATAR_URL


class IssueListSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    creator_id = serializers.IntegerField(source="creator.id", read_only=True)

    class Meta:
        model = Issue
        fields = [
            'id',
            'title',
            'status',
            'nickname',
            'avatar',
            'creator_id',
            'created_at'
        ]

    def get_nickname(self, obj):
        nickname = getattr(obj.creator, "nickname", None)
        if not nickname or nickname.strip() == "":
            return DEFAULT_NICKNAME
        return nickname

    def get_avatar(self, obj):
        request = self.context.get("request")
        avatar = getattr(obj.creator, "avatar", None)

        if avatar:
            try:
                return request.build_absolute_uri(avatar.url)
            except:
                pass

        if request:
            return request.build_absolute_uri(DEFAULT_AVATAR_URL)
        return DEFAULT_AVATAR_URL
