from rest_framework import serializers
from .models import Review
from django.contrib.auth import get_user_model

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(
        source='reviewer.username',
        read_only=True,
        help_text="The username of the reviewer"
    )
    reviewee_name = serializers.CharField(
        source='reviewee.username',
        read_only=True,
        help_text="The username of the reviewee"
    )

    class Meta:
        model = Review
        fields = [
            'id',
            'contract',
            'reviewer',
            'reviewee',
            'reviewer_name',
            'reviewee_name',
            'rating',
            'feedback',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        """Custom validation for the Review model."""
        reviewer = data.get('reviewer')
        reviewee = data.get('reviewee')
        contract = data.get('contract')

        # Check that reviewer and reviewee are not the same user
        if reviewer == reviewee:
            raise serializers.ValidationError(
                "A user cannot review themselves.")

        # Check that both users are participants in the given contract
        if contract.job.user != reviewer and contract.proposal.user != reviewer:
            raise serializers.ValidationError(
                "The reviewer is not a participant in the contract.")
        if contract.job.user != reviewee and contract.proposal.user != reviewee:
            raise serializers.ValidationError(
                "The reviewee is not a participant in the contract.")

        return data

    def create(self, validated_data):
        """Custom creation logic for the Review."""
        return Review.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Custom update logic for the Review."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
