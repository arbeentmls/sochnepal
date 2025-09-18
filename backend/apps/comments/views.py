import json

import requests
from apps.permissions import IsCommentOwnerOrReadOnly, IsVerifiedUserOrReadOnly
from apps.reports.models import Report
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Comment
from .serializers import CommentSerializer


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsCommentOwnerOrReadOnly,
        IsVerifiedUserOrReadOnly,
    ]

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(report=self.kwargs["report_pk"])
            .select_related("report", "user")
            .order_by("-created_at")
        )

    def list(self, request, *args, **kwargs):
        get_object_or_404(Report, pk=self.kwargs["report_pk"])
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        if len(queryset) > 0:
            response = requests.post(
                "http://ai-service:8001/predict-toxicity",

                json.dumps(
                    [
                        {"id": value["id"], "comment": value["content"]}
                        for value in queryset.values()
                    ]
                ),
            )
            results_by_id = {r["id"]: r for r in response.json()["results"]}
            data = []

            for comment in serializer.data:
                result = results_by_id.get(comment["id"])
                if result:
                    comment["is_toxic"] = result["is_toxic"]
                    comment["confidence"] = result["confidence"]
                data.append(comment)

            return Response(data)
        else:
            return Response(serializer.data)
        # return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
