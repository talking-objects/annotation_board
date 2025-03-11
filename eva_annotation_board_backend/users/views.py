from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import PrivateUserSerializer
from rest_framework.exceptions import ParseError
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import User
from videos.models import Video
from annotations.models import Reference, Category, Event, Place, Tag, Data, Narration
from toa_key.models import KeyModel


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(PrivateUserSerializer(user).data)

    # def put(self, request):
    #     user = request.user
    #     serializer = PrivateUserSerializer(user, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         updated_user = serializer.save()
    #         return Response(PrivateUserSerializer(updated_user).data)
    #     else:
    #         return Response(serializer.errors)


class LogInView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            raise ParseError("Useranem or Password not found")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return Response({"ok": "Welcome!"})
        else:
            raise ParseError("Wrong password")


class LogOutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"Ok": "Bye!"})


class UserView(APIView):

    def post(self, request):
        toa_key = request.data.get("key")
        print(toa_key)
        if not toa_key:
            raise ParseError("You should send key")
        try:
            KeyModel.objects.get(key=toa_key)
        except KeyModel.DoesNotExist:
            raise ParseError("Wrong Key")

        user = PrivateUserSerializer(data=request.data)

        password = request.data.get("password")
        if not password:
            raise ParseError("You should send password")
        if user.is_valid():
            new_user = user.save()
            new_user.set_password(password)

            new_user.is_staff = True

            """
                Permission
            """
            # User
            user_content_type = ContentType.objects.get_for_model(User)
            user_view_permission = Permission.objects.get(
                content_type=user_content_type, codename="view_user"
            )
            user_change_permission = Permission.objects.get(
                content_type=user_content_type, codename="change_user"
            )
            user_delete_permission = Permission.objects.get(
                content_type=user_content_type, codename="delete_user"
            )

            # Video
            video_content_type = ContentType.objects.get_for_model(Video)
            video_permissions = Permission.objects.filter(
                content_type=video_content_type
            )

            # Annotations
            # 1. Reference
            reference_content_type = ContentType.objects.get_for_model(Reference)
            reference_permissions = Permission.objects.filter(
                content_type=reference_content_type
            )

            # 2. Tag
            tag_content_type = ContentType.objects.get_for_model(Tag)
            tag_permissions = Permission.objects.filter(content_type=tag_content_type)

            # 3. Narration
            narration_content_type = ContentType.objects.get_for_model(Narration)
            narration_permissions = Permission.objects.filter(
                content_type=narration_content_type
            )

            # 4. Category
            category_content_type = ContentType.objects.get_for_model(Category)
            category_permissions = Permission.objects.filter(
                content_type=category_content_type
            )

            # 5. Event
            event_content_type = ContentType.objects.get_for_model(Event)
            event_permissions = Permission.objects.filter(
                content_type=event_content_type
            )

            # 6. Place
            place_content_type = ContentType.objects.get_for_model(Place)
            place_permissions = Permission.objects.filter(
                content_type=place_content_type
            )

            # 7. Data
            data_content_type = ContentType.objects.get_for_model(Data)
            data_permissions = Permission.objects.filter(content_type=data_content_type)

            new_user.user_permissions.add(
                user_view_permission,
                user_change_permission,
                user_delete_permission,
                *video_permissions,
                *reference_permissions,
                *tag_permissions,
                *narration_permissions,
                *category_permissions,
                *event_permissions,
                *place_permissions,
                *data_permissions
            )
            new_user.save()
            return Response(PrivateUserSerializer(new_user).data)
        else:
            raise Response(user.errors)
