from django.core.paginator import Paginator
from django.shortcuts import render
import random
from datetime import timedelta
from .models import Studies, Modalities


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


def init_db(request):
    """
    База предоставляется уже предзаполненной, но в случае желания перехода
    на другую СУБД, можно раскомментировать код ниже и сгенерировать тестовые данные.
    """
    return render(request, 'test_datatable/init_db.html')


def studies_view(request):
    """Displaying the studies table with possible data filtering"""
    studies = Studies.objects.all()
    modalities = Modalities.objects.all()

    reset_filters = request.GET.get('reset-filters')

    if not reset_filters:
        date_birthday_from = request.GET.get('patient-birthdate-filter-start', '')
        date_birthday_to = request.GET.get('patient-birthdate-filter-end', '')

        date_study_from = request.GET.get('study-date-filter-start', '')
        date_study_to = request.GET.get('study-date-filter-end', '')

        selected_modalities = request.GET.getlist('study-modality-filter')
        selected_modalities = [int(modality_id) for modality_id in selected_modalities if modality_id.isdigit()]

        search_fio = request.GET.get('search-input-fio', '')
        search_id = request.GET.get('search-input-id', '')

        if date_birthday_from:
            studies = studies.filter(patient_birthdate__gte=date_birthday_from)
        if date_birthday_to:
            studies = studies.filter(patient_birthdate__lte=date_birthday_to)
        if date_study_from:
            studies = studies.filter(study_date__gte=date_study_from)
        if date_study_to:
            studies = studies.filter(study_date__lte=date_study_to)
        if selected_modalities:
            studies = studies.filter(study_modality_id__in=selected_modalities)
        if search_fio:
            studies = studies.filter(patient_fio__icontains=search_fio)
        if search_id:
            studies = studies.filter(study_uid__icontains=search_id)

        paginator = Paginator(studies, 20)

        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)

        context = {
            'page': page,
            'studies': page,
            'modalities': modalities,
            'date_birthday_from': date_birthday_from,
            'date_birthday_to': date_birthday_to,
            'date_study_from': date_study_from,
            'date_study_to': date_study_to,
            'selected_modalities': selected_modalities,
            'search_fio': search_fio,
            'search_id': search_id,
        }
    else:
        paginator = Paginator(studies, 20)

        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)

        context = {
            'page': page,
            'studies': page,
            'modalities': modalities,
        }

    return render(request, 'test_datatable/studies_db.html', context=context)
