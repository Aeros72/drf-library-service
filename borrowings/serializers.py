from datetime import date

from rest_framework import serializers

from books.serializers import BookSerializer
from borrowings.models import Borrowing


class BorrowingListSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
        )


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "expected_return_date",
        )

    def validate_book(self, value):
        if value.inventory < 1:
            raise serializers.ValidationError(
                "Book inventory must be greater than zero."
            )
        return value

    def create(self, validated_data):
        book = validated_data["book"]

        borrowing = Borrowing.objects.create(
            user=self.context["request"].user,
            borrow_date=date.today(),
            **validated_data
        )

        book.inventory -= 1
        book.save()

        return borrowing
