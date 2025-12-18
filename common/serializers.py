from rest_framework import serializers


class UnifiedPostSerializer(serializers.Serializer):
    target = serializers.ChoiceField(
        choices=['study', 'life', 'issue']
    )

    # Post 通用字段
    title = serializers.CharField(required=False)
    content = serializers.CharField(required=False)

    # 生活区
    life_category = serializers.ChoiceField(
        choices=['return_school', 'campus_life'],
        required=False
    )

    # Issue 专用字段
    description = serializers.CharField(required=False)
    location = serializers.CharField(required=False)

    def validate(self, data):
        target = data.get('target')

        if target in ['study', 'life']:
            if not data.get('title') or not data.get('content'):
                raise serializers.ValidationError(
                    'title and content are required for study/life post'
                )

            if target == 'life' and not data.get('life_category'):
                raise serializers.ValidationError(
                    'life_category is required for life post'
                )

        if target == 'issue':
            if not data.get('title') or not data.get('description') or not data.get('location'):
                raise serializers.ValidationError(
                    'title, description and location are required for issue'
                )

        return data
