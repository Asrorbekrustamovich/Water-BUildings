from rest_framework import generics
from .models import Role, User, viloyat, MCHJ, Xodimlar, MCHJUser, Holat, Instrument,Type
from .serializers import RoleSerializer, UserSerializer, ViloyatSerializer, MCHJSerializer, XodimlarSerializer, MCHJUserSerializer, HolatSerializer, InstrumentSerializer,TypeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
class RoleListCreateView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class RoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

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
        mchj_id = self.kwargs['mchj_id']
        return Instrument.objects.filter(mchj_id=mchj_id)
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