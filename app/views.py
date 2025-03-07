from rest_framework import generics
from .models import *
from .serializers import RoleSerializer, UserSerializer, ViloyatSerializer, MCHJSerializer,DocumentSerializer, XodimlarSerializer, MCHJUserSerializer, HolatSerializer, InstrumentSerializer,TypeSerializer,MessageSerializer,NotificationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import BadHeaderError
from django.http import HttpResponse
from django.conf import settings
from .utils import send_email_to_users
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
@csrf_exempt
def send_email_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            viloyat = data.get("viloyat")
            company = data.get("company")
            phonenumber = data.get("phonenumber")
            ism = data.get("ism")
            familiya = data.get("familiya")
            email = data.get("email")
            xabar = data.get("xabar")
            
            if not all([ viloyat, company, phonenumber, ism, familiya, email, xabar]):
                return JsonResponse({"error": "Barcha maydonlar to'ldirilishi kerak"}, status=400)
            
            success = send_email_to_users(viloyat, company, phonenumber, ism, familiya, email, xabar)
            if success:
                return JsonResponse({"message": "Email muvaffaqiyatli jo'natildi"})
            else:
                return JsonResponse({"error": "Email jo'natishda xatolik yoki email mavjud emas"}, status=500)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Noto'g'ri JSON formati"}, status=400)
    return JsonResponse({"error": "Faqat POST so'rovlari qabul qilinadi"}, status=405) 
class RoleListCreateView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
class RoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
class DocumentListCreateView(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class DocumentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class UserDocumentListView(generics.ListAPIView):
    serializer_class = DocumentSerializer
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Document.objects.filter(user_id=user_id)
    
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ViloyatListCreateView(generics.ListCreateAPIView):
    queryset = viloyat.objects.all()
    serializer_class = ViloyatSerializer

class ViloyatDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = viloyat.objects.all()
    serializer_class = ViloyatSerializer

class MCHJListCreateView(generics.ListCreateAPIView):
    queryset = MCHJ.objects.all()
    serializer_class = MCHJSerializer

class MCHJDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MCHJ.objects.all()
    serializer_class = MCHJSerializer

class XodimlarListCreateView(generics.ListCreateAPIView):
    queryset = Xodimlar.objects.all()
    serializer_class = XodimlarSerializer

class XodimlarDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Xodimlar.objects.all()
    serializer_class = XodimlarSerializer

class MCHJUserListCreateView(generics.ListCreateAPIView):
    queryset = MCHJUser.objects.all()
    serializer_class = MCHJUserSerializer

class MCHJUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MCHJUser.objects.all()
    serializer_class = MCHJUserSerializer

class TypeListCreateView(generics.ListCreateAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

class TypeDetailView(generics.RetrieveUpdateDestroyAPIView):
     queryset = Type.objects.all()
     serializer_class = TypeSerializer

class HolatListCreateView(generics.ListCreateAPIView):
    queryset = Holat.objects.all()
    serializer_class = HolatSerializer

class HolatDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Holat.objects.all()
    serializer_class = HolatSerializer

class InstrumentListCreateView(generics.ListCreateAPIView):
    queryset = Instrument.objects.all()
    serializer_class = InstrumentSerializer

class InstrumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Instrument.objects.all()
    serializer_class = InstrumentSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Message, User
from .serializers import MessageSerializer

class MessageListCreateAPIView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        # Get the sender and receiver from the request data
        sender_id = request.data.get('sender')
        mchj_id=request.data.get('mchj')
        receiver_id = User.objects.filter(mchj_id=mchj_id).values_list('id', flat=True)
        # Fetch the sender and receiver objects
        try:
            sender = User.objects.get(id=sender_id)
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            raise ValidationError("Sender or Receiver does not exist.")

    # Check the role IDs
        if sender.role_id == 1 and receiver.role_id != 3:
            raise ValidationError("Sender with role_id 1 can only send to receiver with role_id 3.")
        elif sender.role_id == 3 and receiver.role_id != 1:
             raise ValidationError("Sender with role_id 3 can only send to receiver with role_id 1.")
        elif sender.role_id == 2 and receiver.role_id != 2:
             raise ValidationError("Sender with role_id 2 can only send to receiver with role_id 2.")

        # If validation passes, proceed with creating the message
        return super().create(request, *args, **kwargs)

class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class MessageDetailView1(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_object(self):
        # Retrieve the object using the parent class's method
        obj = super().get_object()
        
        # Get the role_id from the URL kwargs
        role_id = self.kwargs.get('role_id')
        
        # Check if the role_id matches the sender's role_id or any other condition
        if obj.sender.role_id != role_id:
            raise PermissionDenied("You do not have permission to modify this message.")
        
        return obj
class NotificationListCreateView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class Get_Instruments_Based_On_MCHJ(generics.ListAPIView):
    serializer_class = InstrumentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ('type__id',)  # Filter by the 'name' field of the related 'Type' model
    search_fields = [
        'texnika_turi__istartswith',  # Search by texnika_turi starting with a given letter
        'rusumi__istartswith',        # Search by rusumi starting with a given letter
        'zavod_raqami__istartswith',  # Search by zavod_raqami starting with a given letter
        'davlat_raqami__istartswith', # Search by davlat_raqami starting with a given letter
        'sana__istartswith',          # Search by sana starting with a given letter
        'soni__istartswith',          # Search by soni starting with a given letter
        'mchj__name__istartswith',    # Search by MCHJ name starting with a given letter (if MCHJ has a 'name' field)
        'type__name__istartswith',    # Search by Type name starting with a given letter (if Type has a 'name' field)
        'texnik_holati__name__istartswith',  # Search by Texnik holati name starting with a given letter (if Holat has a 'name' field)
    ]

    def get_queryset(self):
         serializer_class = InstrumentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ('type__id',)  # Filter by the 'name' field of the related 'Type' model
    search_fields = [
        'texnika_turi__istartswith',  # Search by texnika_turi starting with a given letter
        'rusumi__istartswith',        # Search by rusumi starting with a given letter
        'zavod_raqami__istartswith',  # Search by zavod_raqami starting with a given letter
        'davlat_raqami__istartswith', # Search by davlat_raqami starting with a given letter
        'sana__istartswith',          # Search by sana starting with a given letter
        'soni__istartswith',          # Search by soni starting with a given letter
        'mchj__name__istartswith',    # Search by MCHJ name starting with a given letter (if MCHJ has a 'name' field)
        'type__name__istartswith',    # Search by Type name starting with a given letter (if Type has a 'name' field)
        'texnik_holati__name__istartswith',  # Search by Texnik holati name starting with a given letter (if Holat has a 'name' field)
    ]

    def get_queryset(self):
        mchj_id = self.kwargs['mchj_id']
        queryset = Instrument.objects.filter(mchj_id=mchj_id)
        
        # Apply additional filtering based on query parameters
        type_id = self.request.query_params.get('type__id', None)
        if type_id:
            queryset = queryset.filter(type__id=type_id)
        
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                texnika_turi__istartswith=search
            ) | queryset.filter(
                rusumi__istartswith=search
            ) | queryset.filter(
                zavod_raqami__istartswith=search
            ) | queryset.filter(
                davlat_raqami__istartswith=search
            ) | queryset.filter(
                sana__istartswith=search
            ) | queryset.filter(
                soni__istartswith=search
            ) | queryset.filter(
                mchj__name__istartswith=search
            ) | queryset.filter(
                type__name__istartswith=search
            ) | queryset.filter(
                texnik_holati__name__istartswith=search
            )
        
        return queryset
class Get_MCHJ_based_on_viloyat(generics.ListAPIView):
    serializer_class = MCHJSerializer
    def get_queryset(self):
        viloyat_id = self.kwargs['viloyat_id']
        return MCHJ.objects.filter(viloyat=viloyat_id)

class Get_MCHJ_count_and_instruments_count_and_Xodimlar_count_based_on_viloyat(APIView):
    def get(self, request, viloyat_id):
        mchj_count = MCHJ.objects.filter(viloyat_id=viloyat_id).count()
        instruments_count = Instrument.objects.filter(mchj__viloyat_id=viloyat_id).count()
        xodimlar_count = Xodimlar.objects.filter(mchj__viloyat_id=viloyat_id).count()

        response_data = [
             {"name":"Tashkilotlar soni","value":mchj_count},
             {"name":"Barcha texnikalar soni","value":instruments_count},
             {"name":"Ishchilar soni","value":xodimlar_count}
        ]
        return Response(response_data, status=200)

class Get_MCHJ_and_counts_based_on_viloyat(APIView):
    def get(self, request, viloyat_id):
        mchjs = MCHJ.objects.filter(viloyat_id=viloyat_id)
        data = []

        for mchj in mchjs:
            instruments_count = Instrument.objects.filter(mchj=mchj).count()
            xodimlar_count = Xodimlar.objects.filter(mchj=mchj).count()
            mchj_count= MCHJ.objects.filter(viloyat_id=viloyat_id).count()
            data.append({
                'mchj_id': mchj.id,
                'mchj_name': mchj.name,
                'mchj_count': mchj_count,   
                'instruments_count': instruments_count,
                'xodimlar_count': xodimlar_count
            })

        return Response(data, status=200)

class GetCountsBasedOnMCHJ(APIView):
    def get(self, request, mchj_id):
        instruments_count = Instrument.objects.filter(mchj_id=mchj_id).count()
        xodimlar_count = Xodimlar.objects.filter(mchj_id=mchj_id).count()

        response_data = {
            'mchj_id': mchj_id,
            'instruments_count': instruments_count,
            'xodimlar_count': xodimlar_count
        }
        return Response(response_data, status=200)
    
class GetAllCountsbasedMCHJ(APIView):
    def get(self, request):
        viloyats = viloyat.objects.all()
        data = []

        for v in viloyats:
            mchj_count = MCHJ.objects.filter(viloyat=v).count()
            instruments_count = Instrument.objects.filter(mchj__viloyat=v).count()
            xodimlar_count = Xodimlar.objects.filter(mchj__viloyat=v).count()
            data.append({
                'viloyat_id': v.id,
                'viloyat_name': v.name,
                'mchj_count': mchj_count or 0,
                'instruments_count': instruments_count or 0,
                'xodimlar_count': xodimlar_count or 0
            })

        return Response(data, status=200)

class GetAllCounts(APIView):
    def get(self, request):
        total_mchj_count = MCHJ.objects.count()
        total_instruments_count = Instrument.objects.count()
        total_xodimlar_count = Xodimlar.objects.count()

        response_data = [ total_mchj_count, total_instruments_count, total_xodimlar_count]
        

        return Response(response_data, status=200)
class MarkNotificationAsRead(APIView):
    def post(self, request, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.is_read = True
            notification.save()
            return Response({'status': 'Notification marked as read'}, status=200)
        except Notification.DoesNotExist:
            return Response({'error': 'Notification not found'}, status=404)


from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Message, User, MCHJUser
from .serializers import MessageSerializer

class AdminSendMessageToMCHJView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        # Static admin user (replace with the actual admin user ID)
        admin_user_id = 1  # Replace with the actual admin user ID
        try:
            sender = User.objects.get(id=admin_user_id)
        except User.DoesNotExist:
            raise ValidationError("Admin user does not exist.")

        # Get the receiver's MCHJ ID from the URL
        mchj_id = self.kwargs['mchj_id']

        # Get the receiver from the MCHJ ID
        try:
            mchj_user = MCHJUser.objects.get(mchj_id=mchj_id)
            receiver = mchj_user.user
        except MCHJUser.DoesNotExist:
            raise ValidationError("Receiver with the specified MCHJ ID does not exist.")

        # Create the message
        message_data = {
            'sender': sender.id,
            'receiver': receiver.id,
            'content': request.data.get('content')
        }
        serializer = self.get_serializer(data=message_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Message, User, MCHJUser
from .serializers import MessageSerializer

class MCHJSendMessageToAdminView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        # Static admin user (replace with the actual admin user ID)
        admin_user_id = 1  # Replace with the actual admin user ID
        try:
            receiver = User.objects.get(id=admin_user_id)
        except User.DoesNotExist:
            raise ValidationError("Admin user does not exist.")

        # Get the sender's MCHJ ID from the URL
        mchj_id = self.kwargs['mchj_id']

        # Get the sender from the MCHJ ID
        try:
            mchj_user = MCHJUser.objects.get(mchj_id=mchj_id)
            sender = mchj_user.user
        except MCHJUser.DoesNotExist:
            raise ValidationError("Sender with the specified MCHJ ID does not exist.")

        # Create the message
        message_data = {
            'sender': sender.id,
            'receiver': receiver.id,
            'content': request.data.get('content')
        }
        serializer = self.get_serializer(data=message_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Mark all notifications as read for the user bound to the mchj_id

        return Response(serializer.data, status=201)

    
class GetMessagesBetweenAdminAndMCHJ(APIView):
    def get(self, request, *args, **kwargs):
        # Static admin user (replace with the actual admin user ID)
        admin_user_id = 1  # Replace with the actual admin user ID

        # Get the receiver's MCHJ ID from the URL
        mchj_id = self.kwargs['mchj_id']

        # Retrieve messages between the admin and the user bound to the mchj_id
        messages = Message.objects.filter(
            sender_id=admin_user_id, receiver__mchjuser__mchj_id=mchj_id
        ) | Message.objects.filter(
            sender__mchjuser__mchj_id=mchj_id, receiver_id=admin_user_id
        ).order_by('timestamp')
        messages1 = Message.objects.filter(sender__mchjuser__mchj_id=mchj_id)
        messages1.update(is_read=True)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=200)

class GetMessagesBetweenAdminAndMCHJ2(APIView):
    def get(self, request, *args, **kwargs):
        # Static admin user (replace with the actual admin user ID)
        admin_user_id = 1  # Replace with the actual admin user ID

        # Get the receiver's MCHJ ID from the URL
        mchj_id = self.kwargs['mchj_id']

        # Retrieve messages between the admin and the user bound to the mchj_id
        messages = Message.objects.filter(
            sender_id=admin_user_id, receiver__mchjuser__mchj_id=mchj_id
        ) | Message.objects.filter(
            sender__mchjuser__mchj_id=mchj_id, receiver_id=admin_user_id
        ).order_by('timestamp')
        messages1 = Message.objects.filter(receiver__mchjuser__mchj_id=mchj_id)
        messages1.update(is_read=True)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=200)
    
class CountUnreadMessagesForAdminView(APIView):
    def get(self, request):
        # Assuming the admin user has a specific ID (e.g., 1)
        admin_user_id = 1  # Replace with the actual admin user ID

        # Count unread messages for the admin
        unread_count = Message.objects.filter(receiver_id=admin_user_id, is_read=False).count()

        return Response({"unread_message_count": unread_count}, status=200)

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Message, MCHJUser

class CountUnreadMessagesForMCHJView(APIView):
    def get(self, request, mchj_id):
        # Get the MCHJUser associated with the given mchj_id
        try:
            mchj_user = MCHJUser.objects.get(mchj_id=mchj_id)
        except MCHJUser.DoesNotExist:
            return Response({"error": "MCHJUser not found for the given MCHJ ID"}, status=404)

        # Get the user_id associated with the MCHJUser
        user_id = mchj_user.user_id

        # Count unread messages for this user
        unread_count = Message.objects.filter(receiver_id=user_id, is_read=False).count()

        return Response({"unread_message_count": unread_count}, status=200)
    
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Message, MCHJUser

class UnreadMessagesForMCHJView(APIView):
    def get(self, request):
        admin_id = 1  # Assuming admin ID is 1

        # Get all unread messages where the receiver is the admin
        unread_messages = Message.objects.filter(receiver_id=admin_id, is_read=False)

        # Prepare response data with only message_id and mchj_id
        response_data = []
        for message in unread_messages:
            mchj_user = MCHJUser.objects.filter(user_id=message.sender_id).first()
            mchj_id = mchj_user.mchj_id if mchj_user else None

            # Count unread messages from this MCHJ
            counts = Message.objects.filter(
                sender_id=message.sender_id,
                receiver_id=admin_id,
                is_read=False
            ).count()

            response_data.append({
                "message_count_for_mchj_that_is_not_readed": counts,
                "mchj_id": mchj_id
            })

        return Response(response_data, status=200)
class MCHJUserListView(generics.ListAPIView):
    serializer_class = MCHJUserSerializer

    def get_queryset(self):
        # Filter MCHJUser objects where the user's role ID is 34
        queryset = MCHJUser.objects.filter(user__role_id=3).select_related('mchj__viloyat', 'user')
        return queryset 


class LoginView(APIView):
     def post(self, request):
         # Get login and password from the request data
         login = request.data.get('login')
         password = request.data.get('password')

         # Check if either login or password is not provided
         if not login or not password:
             return Response({'error': 'Login va parol kiritish majburiy'}, status=400)

         # Try to find the user with the provided login and password
         user = User.objects.filter(login=login, password=password).first()

         # If user is not found, return an error message
         if not user:
             return Response({'error': 'Login yoki parol xato'}, status=400)

         # Check if the user has a special role (e.g., user.id == 1 or user.id == 2)
         if user.id == 1 or user.id == 2:
             response_data = {
                 'user_id': user.id,
                 'role_id': user.role.id,
                 'mchj_id': 0  # Special users might not be associated with an MCHJ
             }
         else:
             # For regular users, get the associated MCHJUser and include the MCHJ ID
             mchj_user = MCHJUser.objects.filter(user=user).first()
             if not mchj_user:
                 return Response({'error': 'MCHJUser topilmadi'}, status=400)

             response_data = {
                 'user_id': user.id,
                 'role_id': user.role.id,
                 'mchj_id': mchj_user.mchj.id
             }

         # Return the response data with a 200 status code
         return Response(response_data, status=200)
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         # Token ichiga qo‘shimcha ma’lumotlar qo‘shish
#         token['user_id'] = user.id
#         token['role_id'] = user.role.id if user.role else None

#         # Agar foydalanuvchi MCHJUser bo‘lsa, `mchj_id` ni olish
#         mchj_user = MCHJUser.objects.filter(user=user).first()
#         token['mchj_id'] = mchj_user.mchj.id if mchj_user else None

#         return token

# from rest_framework.permissions import AllowAny
# from rest_framework_simplejwt.tokens import RefreshToken


# class LoginView(APIView):
#     permission_classes = [AllowAny]  # Har qanday foydalanuvchi login qila oladi

#     def post(self, request):
#         login = request.data.get('login')
#         password = request.data.get('password')

#         if not login or not password:
#             return Response({'error': 'Login va parol kiritish majburiy'}, status=400)

#         user = User.objects.filter(login=login).first()

#         if not user or user.password != password:
#             return Response({'error': 'Login yoki parol noto‘g‘ri'}, status=400)

#         # JWT token yaratish
#         refresh = RefreshToken.for_user(user)

#         # Token ichiga qo‘shimcha ma’lumotlar qo‘shish
#         refresh['user_id'] = user.id
#         refresh['role_id'] = user.role.id if user.role else None

#         mchj_user = MCHJUser.objects.filter(user=user).first()
#         refresh['mchj_id'] = mchj_user.mchj.id if mchj_user else None

#         access_token = str(refresh.access_token)

#         return Response({
#             'refresh': str(refresh),
#             'access': access_token
#         }, status=200)

