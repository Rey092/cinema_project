from django.utils.datetime_safe import datetime
from django.utils.timezone import utc
from cinema_site.models import Seance, Cinema


def string_to_bool(request_inst, key):
    bool_str = request_inst.POST[key]
    return bool_str.lower() in ('yes', 'true', 't', '1')


def localize_datetime_to_rus(time, time_format=None):
    if time_format == 'dateMonth':
        text = time.strftime('%d %b')
    else:
        text = time.strftime('%H:%M - %d %b')

    replacements = [
        ('Jan', 'Янв'), ('Feb', 'Фев'), ('Mar', 'Мар'), ('Apr', 'Апр'),
        ('May', 'Май'), ('Jun', 'Июн'), ('Jul', 'Июл'), ('Aug', 'Авг'),
        ('Sep', 'Сен'), ('Oct', 'Окт'), ('Nov', 'Ноя'), ('Dec', 'Дек'),
    ]
    for target, replacement in replacements:
        text = text.replace(target, replacement)

    return text


def seance_serializer(queryset):
    result = []
    i = 0
    for obj in queryset:
        result.append({
            'model': 'Seance',
            'id': obj.id,
            'fields': {
                'time': localize_datetime_to_rus(obj.time),
                'movie': obj.movie.title,
                'hall': obj.hall.hall_number,
                'price': obj.price,
            }
        })
        i += 1

    return result


def handle_schedule_ajax(request):
    status_2d = string_to_bool(request, 'status_2d')
    status_3d = string_to_bool(request, 'status_3d')
    status_imax = string_to_bool(request, 'status_imax')

    qs = Seance.objects.select_related('movie', 'hall').filter(
        time__gt=datetime.now(tz=utc), movie__is_active=True, ).order_by('time')

    if not status_2d:
        qs = qs.exclude(seance_format='2D')
    if not status_3d:
        qs = qs.exclude(seance_format='3D')
    if not status_imax:
        qs = qs.exclude(seance_format='IMAX')

    if not any([status_2d, status_3d, status_imax]):
        qs = Seance.objects.none()

    for cinema in Cinema.objects.all():
        status = string_to_bool(request, cinema.slug)
        if status:
            qs = qs.filter(hall__cinema=cinema)

    data = seance_serializer(qs)
    return data
