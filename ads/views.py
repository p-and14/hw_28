import json

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework import generics
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from ads.models import Ad, Category, Selection
from ads import serializers
from ads.permissions import SelectionPermissions, AdPermissions
from users.models import User
from hw_28.settings import TOTAL_ON_PAGE


def index(request):
    return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class AdListView(ListView):
    model = Ad
    queryset = Ad.objects.order_by("-price").select_related('author', 'category')

    def get(self, request, *args, **kwargs):
        if category := request.GET.get("cat", None):
            self.queryset = self.queryset.filter(Q(category__id=category))

        if text := request.GET.get("text", None):
            self.queryset = self.queryset.filter(Q(name__icontains=text))

        if location := request.GET.get("location", None):
            self.queryset = self.queryset.filter((Q(author__location__name__icontains=location)))

        price_from = request.GET.get("price_from", None)
        price_to = request.GET.get("price_to", None)
        if price_from and price_to:
            self.queryset = self.queryset.filter(Q(price__range=(price_from, price_to)))
        elif price_from:
            self.queryset = self.queryset.filter(Q(price__gte=price_from))
        elif price_to:
            self.queryset = self.queryset.filter(Q(price__lte=price_to))

        super().get(request, *args, **kwargs)

        paginator = Paginator(self.object_list, TOTAL_ON_PAGE)
        page_obj = paginator.get_page(request.GET.get("page"))

        ads = []
        for ad in page_obj:
            ads.append({
                "id": ad.id,
                "name": ad.name,
                "author_id": ad.author_id,
                "author": ad.author.first_name,
                "price": ad.price,
                "description": ad.description,
                "is_published": ad.is_published,
                "category_id": ad.category_id,
                "image": ad.image.url,
            })

        response = {
            "items": ads,
            "total": paginator.count,
            "num_pages": paginator.num_pages,
        }

        return JsonResponse(response)


class AdDetailView(RetrieveAPIView):
    model = Ad
    queryset = Ad.objects.all()
    serializer_class = serializers.AdDetailSerializer
    permission_classes = [IsAuthenticated]


@method_decorator(csrf_exempt, name="dispatch")
class AdCreateView(CreateView):
    model = Ad
    fields = ["name", "author", "price", "description", "is_published", "category"]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ad_data = json.loads(request.body)

        ad = Ad()
        ad.name = ad_data["name"]
        ad.author, _ = User.objects.get_or_create(id=ad_data["author_id"])
        ad.price = ad_data["price"]
        ad.description = ad_data["description"]
        ad.is_published = ad_data["is_published"]
        ad.category, _ = Category.objects.get_or_create(id=ad_data["category_id"])

        ad.save()
        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author_id": ad.author_id,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "category_id": ad.category_id,
        })


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


@method_decorator(csrf_exempt, name="dispatch")
class CategoryCreateView(CreateView):
    model = Category
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)

        category = Category.objects.create(
            name=category_data["name"]
        )

        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })


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
    permission_classes = [IsAuthenticated, SelectionPermissions]


class SelectionUpdateView(generics.UpdateAPIView):
    queryset = Selection.objects.all()
    serializer_class = serializers.SelectionUpdateSerializer
    permission_classes = [IsAuthenticated, SelectionPermissions]


class SelectionDeleteView(generics.DestroyAPIView):
    queryset = Selection.objects.all()
    serializer_class = serializers.SelectionDeleteSerializer
    permission_classes = [IsAuthenticated, SelectionPermissions]
