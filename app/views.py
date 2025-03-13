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
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, MCHJUser

class RoleListCreateView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes=[IsAuthenticated]
class RoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    # permission_classes=[IsAuthenticated]
class DocumentListCreateView(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    # permission_classes=[IsAuthenticated]

class DocumentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    # permission_classes=[IsAuthenticated]

class UserDocumentListView(generics.ListAPIView):
    serializer_class = DocumentSerializer
    # permission_classes=[IsAuthenticated]
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Document.objects.filter(user_id=user_id)
    
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes=[IsAuthenticated]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes=[IsAuthenticated]

class ViloyatListCreateView(generics.ListCreateAPIView):
    queryset = Viloyat.objects.all()
    serializer_class = ViloyatSerializer
    # permission_classes=[IsAuthenticated]

class ViloyatDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Viloyat.objects.all()
    serializer_class = ViloyatSerializer
    permission_classes=[IsAuthenticated]

class MCHJListCreateView(generics.ListCreateAPIView):
    queryset = MCHJ.objects.all()
    serializer_class = MCHJSerializer
    # permission_classes=[IsAuthenticated]

class MCHJDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MCHJ.objects.all()
    serializer_class = MCHJSerializer
    # permission_classes=[IsAuthenticated]

class XodimlarListCreateView(generics.ListCreateAPIView):
    queryset = Xodimlar.objects.all()
    serializer_class = XodimlarSerializer
    # permission_classes=[IsAuthenticated]

class XodimlarDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Xodimlar.objects.all()
    serializer_class = XodimlarSerializer
    # permission_classes=[IsAuthenticated]

class MCHJUserListCreateView(generics.ListCreateAPIView):
    queryset = MCHJUser.objects.all()
    serializer_class = MCHJUserSerializer
    # permission_classes=[IsAuthenticated]

class MCHJUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MCHJUser.objects.all()
    serializer_class = MCHJUserSerializer
    # permission_classes=[IsAuthenticated]

class TypeListCreateView(generics.ListCreateAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    # permission_classes=[IsAuthenticated]

class TypeDetailView(generics.RetrieveUpdateDestroyAPIView):
     queryset = Type.objects.all()
     serializer_class = TypeSerializer
    #  permission_classes=[IsAuthenticated]

class HolatListCreateView(generics.ListCreateAPIView):
    queryset = Holat.objects.all()
    serializer_class = HolatSerializer
    # permission_classes=[IsAuthenticated]

class HolatDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Holat.objects.all()
    serializer_class = HolatSerializer
    # permission_classes=[IsAuthenticated]

class InstrumentListCreateView(generics.ListCreateAPIView):
    queryset = Instrument.objects.all()
    serializer_class = InstrumentSerializer
    # permission_classes=[IsAuthenticated]

class InstrumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Instrument.objects.all()
    serializer_class = InstrumentSerializer
    # permission_classes=[IsAuthenticated]

class MessageListCreateAPIView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    # permission_classes=[IsAuthenticated]

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
    # permission_classes=[IsAuthenticated]

class MessageDetailView1(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    # permission_classes=[IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        role_id = self.kwargs.get('role_id')
        if obj.sender.role_id != role_id:
            raise PermissionDenied("You do not have permission to modify this message.")
        return obj
class NotificationListCreateView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    # permission_classes=[IsAuthenticated]


class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    # permission_classes=[IsAuthenticated]

class Get_Instruments_Based_On_MCHJ(generics.ListAPIView):
    serializer_class = InstrumentSerializer
    # permission_classes=[IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ('type__id',)  
    search_fields = [
        'texnika_turi__istartswith',  
        'rusumi__istartswith',        
        'zavod_raqami__istartswith',  
        'davlat_raqami__istartswith', 
        'sana__istartswith',          
        'soni__istartswith',          
        'mchj__name__istartswith',    
        'type__name__istartswith',    
        'texnik_holati__name__istartswith',  
    ]

    def get_queryset(self):
         serializer_class = InstrumentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ('type__id',)  
    search_fields = [
        'texnika_turi__istartswith',  
        'rusumi__istartswith',        
        'zavod_raqami__istartswith',  
        'davlat_raqami__istartswith', 
        'sana__istartswith',          
        'soni__istartswith',          
        'mchj__name__istartswith',    
        'type__name__istartswith',    
        'texnik_holati__name__istartswith',  
    ]

    def get_queryset(self):
        mchj_id = self.kwargs['mchj_id']
        queryset = Instrument.objects.filter(mchj_id=mchj_id)
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
    # permission_classes=[IsAuthenticated]
    def get_queryset(self):
        viloyat_id = self.kwargs['viloyat_id']
        return MCHJ.objects.filter(viloyat=viloyat_id)

class Get_MCHJ_count_and_instruments_count_and_Xodimlar_count_based_on_viloyat(APIView):
    # permission_classes=[IsAuthenticated]
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
    # permission_classes=[IsAuthenticated]
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
    # permission_classes=[IsAuthenticated]
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
    # permission_classes=[IsAuthenticated]
    def get(self, request):
        viloyats = Viloyat.objects.all()
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
    # permission_classes=[IsAuthenticated]
    def get(self, request):
        total_mchj_count = MCHJ.objects.count()
        total_instruments_count = Instrument.objects.count()
        total_xodimlar_count = Xodimlar.objects.count()

        response_data = [ total_mchj_count, total_instruments_count, total_xodimlar_count]
        

        return Response(response_data, status=200)
class MarkNotificationAsRead(APIView):
    # permission_classes=[IsAuthenticated]
    def post(self, request, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.is_read = True
            notification.save()
            return Response({'status': 'Notification marked as read'}, status=200)
        except Notification.DoesNotExist:
            return Response({'error': 'Notification not found'}, status=404)


class AdminSendMessageToMCHJView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    # permission_classes=[IsAuthenticated]
    def create(self, request, *args, **kwargs):
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

class MCHJSendMessageToAdminView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    # permission_classes=[IsAuthenticated]
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
    # permission_classes=[IsAuthenticated]
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
    # permission_classes=[IsAuthenticated]
    def get(self, request, *args, **kwargs):
        admin_user_id = 1 
        mchj_id = self.kwargs['mchj_id']
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
    # permission_classes=[IsAuthenticated]
    def get(self, request):
        admin_user_id = 1  
        unread_count = Message.objects.filter(receiver_id=admin_user_id, is_read=False).count()

        return Response({"unread_message_count": unread_count}, status=200)


class CountUnreadMessagesForMCHJView(APIView):
    # permission_classes=[IsAuthenticated]
    def get(self, request, mchj_id):
        try:
            mchj_user = MCHJUser.objects.get(mchj_id=mchj_id)
        except MCHJUser.DoesNotExist:
            return Response({"error": "MCHJUser not found for the given MCHJ ID"}, status=404)
        user_id = mchj_user.user_id
        unread_count = Message.objects.filter(receiver_id=user_id, is_read=False).count()

        return Response({"unread_message_count": unread_count}, status=200)

class UnreadMessagesForMCHJView(APIView):
    # permission_classes=[IsAuthenticated]
    def get(self, request):
        admin_id = 1 
        unread_messages = Message.objects.filter(receiver_id=admin_id, is_read=False)
        response_data = []
        for message in unread_messages:
            mchj_user = MCHJUser.objects.filter(user_id=message.sender_id).first()
            mchj_id = mchj_user.mchj_id if mchj_user else None
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
    # permission_classes=[IsAuthenticated]
    serializer_class = MCHJUserSerializer

    def get_queryset(self):
        queryset = MCHJUser.objects.filter(user__role_id=3).select_related('mchj__viloyat', 'user')
        return queryset 

class InstrumentCountByConditionView(APIView):
    def get(self, request, *args, **kwargs):
        mchj_id = kwargs.get('mchj_id')
        
        if not mchj_id:
            return Response({"error": "MCHJ ID is required"}, status=400)
        
        try:
            mchj = MCHJ.objects.get(id=mchj_id)
        except MCHJ.DoesNotExist:
            return Response({"error": "MCHJ not found"}, status=404)
        
        types = Type.objects.all()
        holats = Holat.objects.all()
        
        result = []
        
        for type_obj in types:
            type_data = {
                "id": type_obj.id,
                "name": type_obj.name,
                "total_count": 0,
                "holat_counts": {holat.name: 0 for holat in holats}  # Use holat.name instead of holat.id
            }
            
            instruments = Instrument.objects.filter(mchj=mchj, type=type_obj)
            type_data["total_count"] = instruments.count()
            
            for instrument in instruments:
                type_data["holat_counts"][instrument.texnik_holati.name] += 1  # Use holat.name instead of holat.id
            
            result.append(type_data)
        
        return Response(result, status=200)

class LoginView(APIView):
    permission_classes = [AllowAny]  # Kirish uchun ruxsat berish

    def post(self, request):
        login = request.data.get('login')
        password = request.data.get('password')

        if not login or not password:
            return Response({'error': 'Login va parol kiritish majburiy'}, status=400)

        user = authenticate(login=login, password=password)
        if not user:
            return Response({'error': 'Login yoki parol noto‘g‘ri'}, status=401)

        if not user.is_active:
            return Response({'error': 'Foydalanuvchi bloklangan'}, status=403)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Role 1 yoki 2 bo'lsa, mchj_id = 0
        mchj_id = 0
        if user.id not in [1, 2]:  
            mchj_user = MCHJUser.objects.filter(user=user).first()
            if not mchj_user:
                return Response({'error': 'MCHJUser topilmadi'}, status=400)
            mchj_id = mchj_user.mchj.id  # Agar user MCHJga tegishli bo'lsa, ID ni olish

        response_data = {
            'user_id': user.id,
            'role_id': user.role.id if user.role else None,
            'mchj_id': mchj_id,
            'access_token': access_token,
            'refresh_token': str(refresh),
        }

        return Response(response_data, status=200)