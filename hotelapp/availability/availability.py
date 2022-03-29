import datetime
from hotelapp.models import Rooms, Reservation
# from hotelapp.views import reservation


def check_availability(room, check_in, check_out):
    avail_list = []
    reservation_list = Reservation.objects.filter(room=room)
    for reservation in reservation_list:
        if reservation.check_in > check_out or reservation.check_out < check_in:
            avail_list.append(True)
        else:
                avail_list.append(False)

    return all(avail_list)