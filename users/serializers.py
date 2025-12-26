from rest_framework import serializers
from .models import User


class MeSerializer(serializers.ModelSerializer):
    # 只用于写（接收 wx.uploadFile）
    avatar = serializers.ImageField(required=False, write_only=True)

    # 只用于读（给前端展示）
    avatar_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'avatar',        # 写
            'avatar_url',    # 读
            'nickname',
            'username',
        ]

    def get_avatar_url(self, obj):
        if obj.avatar:
            request = self.context.get('request')
            url = obj.avatar.url
            if request:
                return request.build_absolute_uri(url)
            return url
        return None
