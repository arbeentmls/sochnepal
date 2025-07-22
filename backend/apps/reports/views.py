import json

import requests
from django.db.models import Count, Exists, OuterRef
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.flags.models import Flag
from apps.permissions import IsVerifiedUserOrReadOnly

from .filters import ReportFilter
from .models import Category, Report, UpVote
from .pagination import ReportPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import CategoryListSerializer, ReportSerializer, UpVoteSerializer


class ReportViewSet(ModelViewSet):
    serializer_class = ReportSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
        IsVerifiedUserOrReadOnly,
    ]
    queryset = (
        Report.objects.select_related(
            "category",
            "created_by",
        )
        .prefetch_related(
            "upvotes",
            "flags",
            "upvotes__user",
            "flags__flagged_by",
        )
        .all()
        .order_by("-created_at")
    )
    parser_classes = [JSONParser, MultiPartParser]
    pagination_class = ReportPagination
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ReportFilter

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.annotate(total_upvotes=Count("upvotes", distinct=True))

        if self.request.user.is_authenticated:
            queryset = queryset.annotate(
                user_upvoted=Exists(
                    UpVote.objects.filter(
                        report=OuterRef("pk"), user=self.request.user
                    ),
                )
            )
            queryset = queryset.annotate(
                user_flagged=Exists(
                    Flag.objects.filter(
                        report=OuterRef("pk"), flagged_by=self.request.user
                    )
                )
            )

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response = requests.post(
            "http://ai-service:8001/emotions",
            json.dumps(
                [
                    {
                        "id": serializer.data["id"],
                        "content": serializer.data["description"],
                    }
                ]
            ),
        )
        data_with_emotion = {**serializer.data}
        data_with_emotion["emotions"] = response.json()["emotions"]
        print(data_with_emotion)
        return Response(data_with_emotion)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def my(self, request):
        queryset = self.filter_queryset(
            self.get_queryset().filter(created_by=request.user)
        )
        serializer = self.serializer_class(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)


class CategoryView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class UpVoteView(GenericAPIView):
    serializer_class = UpVoteSerializer
    queryset = UpVote.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsVerifiedUserOrReadOnly]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
