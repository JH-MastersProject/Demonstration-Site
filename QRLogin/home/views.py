from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from QRLogin.QRAuth import get_count, validate, authenticate as qr_authenticate
from home.models import QRUser


# Create your views here.
@login_required()
def home(request):
    user = QRUser.objects.get(user=request.user)
    return render(request, 'home/index.html', context={"user": user})


def attempt_login(request):
    username = request.GET["username"]
    password = request.GET["password"]
    user = authenticate(request, username=username, password=password)

    if not user:
        response = JsonResponse({"error": "Invalid Username or Password"})
        response.status_code = 401
        return response

    temp = QRUser.objects.get(user=user)
    if not temp.twofact:
        login(request, user)
        response = JsonResponse({"success": "success"})
        response.status_code = 200
        return response
    else:
        id = temp.qr_id
        count = get_count(id)

        response = JsonResponse({"twofa": count})
        response.status_code = 200
        return response


def attempt_2fa_login(request):
    username = request.GET["username"]
    password = request.GET["password"]
    qr = request.GET.getlist("qr")

    user = authenticate(username=username, password=password)
    if user:
        qr_user = QRUser.objects.get(user=user)

        if not qr_user.twofact:
            response = JsonResponse({"error": "Attempting 2fa when user does not have it enabled"})
            response.status_code = 400
            return response
        else:

            # Check if it is correct qr code
            qr_id = qr_user.qr_id

            if qr_authenticate(qr_id, qr):
                login(request, user)
                response = JsonResponse({"success": "Logged in"})
                response.code = 200
                return response
            else:
                response = JsonResponse({"error": "Wrong Code"})
                response.code = 401
                return response

    else:
        response = JsonResponse({"error": "Invalid Username or Password"})
        response.code = 401
        return response


def login_page(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
    return render(request, 'home/login.html')


def logout_page(request):
    logout(request)
    return redirect("/")


@login_required()
def twofact_setup(request):
    temp = QRUser.objects.get(user=request.user)
    if temp.twofact:
        return redirect('/')

    return render(request, 'home/twofact_setup.html')


def add_existing_2fa_code(request):
    qr = request.GET["qr"]

    qr_id = validate(qr)
    if not qr_id:
        response = JsonResponse({"error": "Invalid QR"})
        response.status_code = 400
        return response

    add_qr_id(request.user, qr_id)

    return HttpResponse("success")


def add_qr_id(user, data):
    qr_user = QRUser.objects.get(user=user)
    qr_user.qr_id = data
    qr_user.twofact = True
    qr_user.save()
