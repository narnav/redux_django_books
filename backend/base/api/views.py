from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User

from .serializers import NoteSerializer
from base.models import Note, Profile, OrderBookS, Book

# MyTokenObtainPairSerializer extend (inherite)TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # classmethod (static method) method we can use with out creating an object
    @classmethod
    def get_token(cls, user):
        # super -> the class we inherit
        token = super().get_token(user)
        # select one row from Profile table (where user = given user)

        # from here it's our code
        pro = Profile.objects.get(user=user)
        print(pro)
        # Add custom claims
        token['username'] = user.username
        token['eeemail'] = user.email
        token['staff'] = user.is_staff
        token['airLiner'] = pro.is_airLiner
        token['waga'] = "baga"
        # our code done
        # ...

        return token

# TokenObtainPairView - Django built-in method that make login

# MyTokenObtainPairView extend (inherite) TokenObtainPairView


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',
    ]

    return Response(routes)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def orderBook(request):
    user = request.user
    id = request.data["id"]
    book = Book.objects.get(_id=id)
    OrderBookS.objects.create(user=user, book=book)
    return Response({"id": book._id, "bookName": book.bookName, "author": book.author})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrders(request):
    user = request.user
    orders = user.orderbooks_set.all()
    # user.note_set.all()
    myOrders = []
    for order in orders:
        myOrders.append({"bookName": order.book.bookName,
                        "author": order.book.author})
    return Response(myOrders)

#     book = models.ForeignKey(Book, on_delete=models.DO_NOTHING, null=True)
#     _id = models.AutoField(primary_key=True, editable=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addBook(request):
    user = request.user
    bookName = request.data["bookName"]
    author = request.data["author"]
    book = Book.objects.create(
        bookName=bookName, author=author)
    return Response({"id": book._id, "bookName": bookName, "author": author})


@api_view(['GET'])
def getAllBooks(request):
    books = Book.objects.all()
    arBooks = []
    for book in books:
        arBooks.append(
            {"id": book._id, "bookName": book.bookName, "author": book.author})
    return Response(arBooks)


# class OrderBookS(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     bookName = models.CharField(max_length=50)
#     author = models.CharField(max_length=50)
#     _id = models.AutoField(primary_key=True, editable=False)

#     def __str__(self):
#         return self.bookName


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getNotes(request):
    print("innnn")
    user = request.user
    print(user)
    notes = user.note_set.all()
    print(user.note_set)
    print(notes)
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)

# Register/signup

# doSignUpAsync({ userName, email, pwd, avatar, address, isAirLiner })


@api_view(['POST'])
def register(request):
    userName = request.data["userName"]
    password = request.data["pwd"]
    email = request.data["email"]
    avatar = request.data["avatar"]
    address = request.data["address"]
    isAirLiner = request.data["isAirLiner"]
    print(userName, password, email, avatar, address, isAirLiner)
    # create new user
    user = User.objects.create_user(
        username=userName, password=password, email=email)

    # # create new profile with the new user....
    Profile.objects.create(user=user, avatar=avatar,
                           address=address, is_airLiner=isAirLiner)
    return Response({"isAirLiner": isAirLiner, "userName": userName})

# user = models.OneToOneField(
#         User, on_delete=models.CASCADE, primary_key=True)
#     avatar = models.CharField(max_length=50)
#     address = models.CharField(max_length=50)
#     credit = models.CharField(max_length=4)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOneNote(request):
    user = request.user
    print(user)
    notes = user.note_set.all()
    ps = user.pita_set.all()
    print(ps)
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)
