from datetime import timedelta
import itertools
from operator import itemgetter

from django.db.models import Count, Q, F, ExpressionWrapper, FloatField
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic.list import ListView

import django_filters
from django_filters.rest_framework import FilterSet
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from subjects.models import Subject
from .water_control import water_control
from .models import Session, WaterAdministration, Weighing, WaterType
from .serializers import (SessionListSerializer,
                          SessionDetailSerializer,
                          WaterAdministrationDetailSerializer,
                          WeighingDetailSerializer,
                          WaterTypeDetailSerializer,
                          )


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield (start_date + timedelta(n))


class WaterHistoryListView(ListView):
    template_name = 'water_history.html'

    def get_context_data(self, **kwargs):
        context = super(WaterHistoryListView, self).get_context_data(**kwargs)
        subject = Subject.objects.get(pk=self.kwargs['subject_id'])
        context['title'] = mark_safe(
            'Water history of <a href="%s">%s</a>' % (
                reverse('admin:subjects_subject_change',
                        args=[subject.id]),
                subject.nickname))
        context['site_header'] = 'Alyx'
        url = reverse('weighing-plot', kwargs={'subject_id': subject.id})
        context['plot_url'] = url
        return context

    def get_queryset(self):
        subject = Subject.objects.get(pk=self.kwargs['subject_id'])
        return water_control(subject).to_jsonable()[::-1]


def weighing_plot(request, subject_id=None):
    if not request.user.is_authenticated:
        return HttpResponse('')
    if subject_id in (None, 'None'):
        return HttpResponse('')
    wc = water_control(Subject.objects.get(pk=subject_id))
    return wc.plot()


class SessionFilter(FilterSet):
    subject = django_filters.CharFilter(field_name='subject__nickname', lookup_expr=('iexact'))
    dataset_types = django_filters.CharFilter(field_name='dataset_types',
                                              method='filter_dataset_types')
    performance_gte = django_filters.NumberFilter(field_name='performance',
                                                  method=('filter_performance_gte'))
    performance_lte = django_filters.NumberFilter(field_name='performance',
                                                  method=('filter_performance_lte'))
    users = django_filters.CharFilter(field_name='users__username', method=('filter_users'))
    date_range = django_filters.CharFilter(field_name='date_range', method=('filter_date_range'))
    type = django_filters.CharFilter(field_name='type', lookup_expr=('iexact'))
    lab = django_filters.CharFilter(field_name='lab__name', lookup_expr=('iexact'))

    def filter_users(self, queryset, name, value):
        users = value.split(',')
        queryset = queryset.filter(users__username__in=users)
        queryset = queryset.annotate(
            users_count=Count('users__username'))
        queryset = queryset.filter(users_count__gte=len(users))
        return queryset

    def filter_date_range(self, queryset, name, value):
        drange = value.split(',')
        queryset = queryset.filter(
            Q(start_time__date__gte=drange[0]),
            Q(start_time__date__lte=drange[1]),
        )
        return queryset

    def filter_dataset_types(self, queryset, name, value):
        dtypes = value.split(',')
        queryset = queryset.filter(data_dataset_session_related__dataset_type__name__in=dtypes)
        queryset = queryset.annotate(
            dtypes_count=Count('data_dataset_session_related__dataset_type'))
        queryset = queryset.filter(dtypes_count__gte=len(dtypes))
        return queryset

    def filter_performance_gte(self, queryset, name, perf):
        queryset = queryset.exclude(n_trials__isnull=True)
        pf = ExpressionWrapper(100 * F('n_correct_trials') / F('n_trials'),
                               output_field=FloatField())
        queryset = queryset.annotate(performance=pf)
        return queryset.filter(performance__gte=float(perf))

    def filter_performance_lte(self, queryset, name, perf):
        queryset = queryset.exclude(n_trials__isnull=True)
        pf = ExpressionWrapper(100 * F('n_correct_trials') / F('n_trials'),
                               output_field=FloatField())
        queryset = queryset.annotate(performance=pf)
        return queryset.filter(performance__lte=float(perf))

    class Meta:
        model = Session
        exclude = ['json']


class WeighingFilter(FilterSet):
    nickname = django_filters.CharFilter(field_name='subject__nickname', lookup_expr='iexact')

    class Meta:
        model = Weighing
        exclude = ['json']


class WaterAdministrationFilter(FilterSet):
    nickname = django_filters.CharFilter(field_name='subject__nickname', lookup_expr='iexact')

    class Meta:
        model = WaterAdministration
        exclude = ['json']


class SessionAPIList(generics.ListCreateAPIView):
    """
    List and create sessions - view in summary form
    """
    queryset = Session.objects.all()
    queryset = SessionListSerializer.setup_eager_loading(queryset)
    serializer_class = SessionListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_class = SessionFilter


class SessionAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Detail of one session
    """
    queryset = Session.objects.all()
    queryset = SessionDetailSerializer.setup_eager_loading(queryset)
    serializer_class = SessionDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)


class WeighingAPIListCreate(generics.ListCreateAPIView):
    """
    Lists or creates a new weighing.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = WeighingDetailSerializer
    queryset = Weighing.objects.all()
    queryset = WeighingDetailSerializer.setup_eager_loading(queryset)
    filter_class = WeighingFilter


class WeighingAPIDetail(generics.RetrieveDestroyAPIView):
    """
    Allows viewing of full detail and deleting a weighing.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = WeighingDetailSerializer
    queryset = Weighing.objects.all()


class WaterTypeList(generics.ListCreateAPIView):
    queryset = WaterType.objects.all()
    serializer_class = WaterTypeDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'name'


class WaterAdministrationAPIListCreate(generics.ListCreateAPIView):
    """
    Lists or creates a new water administration.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = WaterAdministrationDetailSerializer
    queryset = WaterAdministration.objects.all()
    queryset = WaterAdministrationDetailSerializer.setup_eager_loading(queryset)
    filter_class = WaterAdministrationFilter


class WaterAdministrationAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Allows viewing of full detail and deleting a water administration.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = WaterAdministrationDetailSerializer
    queryset = WaterAdministration.objects.all()


def _merge_lists_dicts(la, lb, key):
    lst = sorted(itertools.chain(la, lb), key=itemgetter(key))
    out = []
    for k, v in itertools.groupby(lst, key=itemgetter(key)):
        d = {}
        for dct in v:
            d.update(dct)
        out.append(d)
    return out


class WaterRequirement(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None, nickname=None):
        assert nickname
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        subject = Subject.objects.get(nickname=nickname)
        records = subject.water_control.to_jsonable(start_date=start_date, end_date=end_date)
        data = {'subject': nickname, 'implant_weight': subject.implant_weight, 'records': records}
        return Response(data)
