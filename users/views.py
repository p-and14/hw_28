import json

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from users.models import User, Location
from hw_28.settings import TOTAL_ON_PAGE


@method_decorator(csrf_exempt, name="dispatch")
class UserListView(ListView):
    model = User
    queryset = User.objects.select_related('location').annotate(total_ads=Count("ad", filter=Q(ad__is_published=True)))

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        paginator = Paginator(self.object_list, TOTAL_ON_PAGE)
        page_obj = paginator.get_page(request.GET.get("page"))

        users = []
        for user in page_obj:
            users.append({
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "age": user.age,
                "location": user.location.name,
                "total_ads": user.total_ads,
            })

        response = {
            "items": users,
            "total": paginator.count,
            "num_pages": paginator.num_pages,
        }

        return JsonResponse(response)


class UserDetailView(DetailView):
    model = User
    queryset = User.objects.select_related('location')

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        response = {
            "id": self.object.id,
            "username": self.object.username,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "role": self.object.role,
            "age": self.object.age,
            "location": self.object.location.name,
        }

        return JsonResponse(response)


@method_decorator(csrf_exempt, name="dispatch")
class UserCreateView(CreateView):
    model = User
    fields = ["username", "password", "first_name", "last_name", "role", "age", "location"]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        user_data = json.loads(request.body)

        user = User()
        user.username = user_data["username"]
        user.password = user_data["password"]
        user.first_name = user_data["first_name"]
        user.last_name = user_data["last_name"]
        user.role = user_data["role"]
        user.age = user_data["age"]
        user.location, _ = Location.objects.get_or_create(name=user_data["location"])

        try:
            user.full_clean()
        except ValidationError as e:
            return JsonResponse(e.error_dict, status=422)

        user.save()

        return JsonResponse({
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "age": user.age,
            "location": user.location.name,
        })


@method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(UpdateView):
    model = User
    fields = ["username", "password", "first_name", "last_name", "role", "age", "location"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user_data = json.loads(request.body)
        self.object.username = user_data["username"]
        self.object.password = user_data["password"]
        self.object.first_name = user_data["first_name"]
        self.object.last_name = user_data["last_name"]
        self.object.age = user_data["age"]
        self.object.location, _ = Location.objects.get_or_create(name=user_data["location"])

        try:
            self.object.full_clean()
        except ValidationError as e:
            return JsonResponse(e.error_dict, status=422)

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "username": self.object.username,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "role": self.object.role,
            "age": self.object.age,
            "location": self.object.location.name,
        })


@method_decorator(csrf_exempt, name="dispatch")
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)
