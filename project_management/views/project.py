from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader


class ParkingSpace:
    def __init__(self, number, status):
        self.number = number
        self.status = status


def projects(request):


    matrix = zip(
        [ParkingSpace(1, 1), ParkingSpace(2, 0), ParkingSpace(3, 0), ParkingSpace(4, 0), ParkingSpace(5, 1), ParkingSpace(6, 0), ParkingSpace(7, -1), ParkingSpace(8, -1), ParkingSpace(9, 0), ParkingSpace(10, 0)],
        [ParkingSpace(0, -1), ParkingSpace(0, -1), ParkingSpace(0, -1), ParkingSpace(0, -1), ParkingSpace(0, -1), ParkingSpace(0, -1), ParkingSpace(0, -1), ParkingSpace(0, -1), ParkingSpace(0, -1), ParkingSpace(0, -1)],
        [ParkingSpace(11, 1), ParkingSpace(12, 0), ParkingSpace(13, 0), ParkingSpace(14, 0), ParkingSpace(15, 0), ParkingSpace(16, 1), ParkingSpace(17, 0), ParkingSpace(18, 0), ParkingSpace(19, 1), ParkingSpace(20, 0)],
        [ParkingSpace(21, 0), ParkingSpace(22, 0), ParkingSpace(23, 1), ParkingSpace(24, 1), ParkingSpace(25, 0), ParkingSpace(26, 0), ParkingSpace(27, 1), ParkingSpace(28, 0), ParkingSpace(29, 0), ParkingSpace(30, 1)],
    )

    context = {
        "matrix": matrix,
        "length": list(range(0)),
        "width": list(range(0)),
    }
    return render(request, "square.html", context=context)
