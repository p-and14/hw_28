import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from rest_framework import generics
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from ads.models import Ad, Category, Selection
from ads import serializers
from ads.permissions import SelectionPermissions, AdPermissions


def index(request):
    return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class AdListView(generics.ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = serializers.AdListSerializer


class AdDetailView(RetrieveAPIView):
    model = Ad
    queryset = Ad.objects.all()
    serializer_class = serializers.AdDetailSerializer
    permission_classes = [IsAuthenticated]


@method_decorator(csrf_exempt, name="dispatch")
class AdCreateView(generics.CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = serializers.AdCreateSerializer


class AdUpdateView(generics.UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = serializers.AdUpdateSerializer
    permission_classes = [IsAuthenticated, AdPermissions]


class AdDeleteView(generics.DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = serializers.AdDeleteSerializer
    permission_classes = [IsAuthenticated, AdPermissions]


@method_decorator(csrf_exempt, name="dispatch")
class AdImageUploadView(UpdateView):
    model = Ad
    fields = ["image"]
    queryset = Ad.objects.select_related("author", "category")

    def post(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object.image = request.FILES["image"]
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "author": self.object.author.first_name,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
            "image": self.object.image.url if self.object.image else None,
        })


@method_decorator(csrf_exempt, name="dispatch")
class CategoriesListView(ListView):
    model = Category
    queryset = Category.objects.all().order_by("name")

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        response = []
        for category in self.object_list:
            response.append({
                "id": category.id,
                "name": category.name,
            })

        return JsonResponse(response, safe=False)


class CategoryDetailView(DetailView):
    model = Category
    queryset = Category.objects.filter()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        response = {
            "id": self.object.id,
            "name": self.object.name,
        }

        return JsonResponse(response)


class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategoryCreateSerializer


@method_decorator(csrf_exempt, name="dispatch")
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ["name"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        category_data = json.loads(request.body)
        self.object.name = category_data["name"]

        try:
            self.object.full_clean()
        except ValidationError as e:
            return JsonResponse(e.error_dict, status=422)

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
        })


@method_decorator(csrf_exempt, name="dispatch")
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


class SelectionListView(generics.ListAPIView):
    queryset = Selection.objects.all()
    serializer_class = serializers.SelectionListSerializer


class SelectionDetailView(generics.RetrieveAPIView):
    queryset = Selection.objects.all()
    serializer_class = serializers.SelectionDetailSerializer


class SelectionCreateView(generics.CreateAPIView):
    queryset = Selection.objects.all()
    serializer_class = serializers.SelectionCreateSerializer
    permission_classes = [IsAuthenticated]


class SelectionUpdateView(generics.UpdateAPIView):
    queryset = Selection.objects.all()
    serializer_class = serializers.SelectionUpdateSerializer
    permission_classes = [IsAuthenticated, SelectionPermissions]


class SelectionDeleteView(generics.DestroyAPIView):
    queryset = Selection.objects.all()
    serializer_class = serializers.SelectionDeleteSerializer
    permission_classes = [IsAuthenticated, SelectionPermissions]
