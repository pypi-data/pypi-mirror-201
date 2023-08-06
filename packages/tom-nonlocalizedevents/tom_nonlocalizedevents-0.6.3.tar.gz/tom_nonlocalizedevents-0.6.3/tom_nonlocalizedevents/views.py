import json

from django.contrib import messages
from django.core.cache import cache
from django.http import Http404
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView
from django.views.generic.base import View
from django.urls import reverse
from django.conf import settings

from rest_framework import permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from tom_nonlocalizedevents.models import EventCandidate, EventLocalization, NonLocalizedEvent
from tom_nonlocalizedevents.serializers import (EventCandidateSerializer, EventLocalizationSerializer,
                                                NonLocalizedEventSerializer)


class NonLocalizedEventListView(LoginRequiredMixin, ListView):
    """
    Unadorned Django ListView subclass for NonLocalizedEvent model.
    """
    model = NonLocalizedEvent
    template_name = 'tom_nonlocalizedevents/index.html'

    def get_queryset(self):
        # '-created' is most recent first
        qs = NonLocalizedEvent.objects.order_by('-created')
        return qs


# from the tom_alerts query_result.html

class CreateEventFromSCiMMAAlertView(View):
    """
    Creates the models.NonLocalizedEvent instance and redirect to NonLocalizedEventDetailView
    """
    pass

    def post(self, request, *args, **kwargs):
        """
        """
        # the request.POST is a QueryDict object;
        # for SCiMMA, alerts: list items are PKs to skip.dev.hop.scimma.org/api/alerts/PK/
        query_id = self.request.POST['query_id']
        # broker_name = self.request.POST['broker']  # should be "SCIMMA"
        # broker_class = get_service_class(broker_name)  # should be <class 'tom_scimma.scimma.SCIMMABroker'>
        alerts = [int(id) for id in request.POST.getlist('alerts', [])]

        errors = []
        # if the user didn't select an alert; warn and re-direct back
        if not alerts:
            messages.warning(request, 'Please select at least one alert from which to create an event.')
            reverse_url: str = reverse('tom_alerts:run', kwargs={'pk': query_id})
            return redirect(reverse_url)

        # try to extract EventID from Alert and use it to create a NoneLocalizedEvent
        for alert_id in alerts:
            cached_alert = json.loads(cache.get(f'alert_{alert_id}'))  # cached by tom_alerts.views.py::RunQueryView
            # early return: alert not in cache
            if not cached_alert:
                messages.error(request, 'Could not create event(s). Try re-running the query to refresh the cache.')
                return redirect(reverse('tom_alerts:run', kwargs={'pk': query_id}))

            # early return: alert not LVC/LVC COUNTERPART NOTICE
            if cached_alert.get('topic', '') != 'lvc.lvc-counterpart':
                messages.error(request,
                               ('Only Alerts from the lvc.lvc-counterpart topic have '
                                'parsed event_trig_num required for Event origination. '
                                'Please select an appropriate alert.'))
                return redirect(reverse('tom_alerts:run', kwargs={'pk': query_id}))

            # early return: event_trig_num not found in parsed alert message
            event_trig_num = cached_alert['message'].get('event_trig_num', None)
            if event_trig_num is None:
                messages.error(request,
                               (f'Could not create event for alert: {alert_id}. '
                                'event_trig_num not found in alert message.'))
                return redirect(reverse('tom_alerts:run', kwargs={'pk': query_id}))

            nonlocalizedevent, created = NonLocalizedEvent.objects.get_or_create(event_id=event_trig_num)
            if not created:
                # the nonlocalizedevent already existed
                messages.warning(request, f'Event {event_trig_num} already exists.')
                errors.append(nonlocalizedevent.event_id)

        if len(alerts) == len(errors):
            # zero nonlocalizedevents created
            return redirect(reverse('tom_alerts:run', kwargs={'pk': query_id}))
        elif len(alerts) == 1:
            # one nonlocalizedevent created
            return redirect(reverse('nonlocalizedevents:detail', kwargs={'pk': nonlocalizedevent.pk}))
        else:
            # multipe nonlocalizedevent created
            return redirect(reverse('nonlocalizedevents:index'))

# Django Rest Framework Views


class NonLocalizedEventViewSet(viewsets.ModelViewSet):
    """
    DRF API endpoint that allows NonLocalizedEvents to be viewed or edited.
    """
    queryset = NonLocalizedEvent.objects.all()
    serializer_class = NonLocalizedEventSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event_id', 'event_type']


class EventCandidateViewSet(viewsets.ModelViewSet):
    """
    DRF API endpoint for EventCandidate model.

    Implementation has changes for bulk_create and update/PATCH EventCandidate instances.
    """
    queryset = EventCandidate.objects.all()
    serializer_class = EventCandidateSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nonlocalizedevent', 'viable', 'priority']

    def get_serializer(self, *args, **kwargs):
        # In order to ensure the list_serializer_class is used for bulk_create, we check that the POST data is a list
        # and add `many = True` to the kwargs
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True

        return super().get_serializer(*args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Provide support for the PATCH HTTP verb to update individual model fields.

        An example request might look like:

            PATCH http://localhost:8000/api/eventcandidates/18/

        with a Request Body of:

            {
                "viability": false
            }

        """
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class EventLocalizationViewSet(viewsets.ModelViewSet):
    """
    DRF API endpoint that allows EventLocalizations to be viewed or edited.
    """
    queryset = EventLocalization.objects.all()
    serializer_class = EventLocalizationSerializer
    permission_classes = [permissions.IsAuthenticated]


class SupereventPkView(LoginRequiredMixin, TemplateView):
    template_name = 'tom_nonlocalizedevents/superevent_vue_app.html'

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        superevent = NonLocalizedEvent.objects.get(pk=kwargs['pk'])
        sequences = list(superevent.sequences.order_by('sequence_id').values(
            'sequence_id', 'event_subtype', 'created', 'pk'))
        for sequence in sequences:
            # Set the created date as a string so it can be in json format
            sequence['created'] = sequence['created'].isoformat()
        context['superevent_pk'] = kwargs['pk']
        context['superevent_id'] = superevent.event_id
        context['sequences'] = json.dumps(sequences)
        context['tom_api_url'] = settings.TOM_API_URL
        context['hermes_api_url'] = settings.HERMES_API_URL
        return context


class SupereventIdView(LoginRequiredMixin, TemplateView):
    template_name = 'tom_nonlocalizedevents/superevent_vue_app.html'

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        try:
            superevent = NonLocalizedEvent.objects.get(event_id=kwargs['event_id'])
            sequences = list(superevent.sequences.order_by('sequence_id').values(
                'sequence_id', 'event_subtype', 'created', 'pk'))
            for sequence in sequences:
                # Set the created date as a string so it can be in json format
                sequence['created'] = sequence['created'].isoformat()
            context['superevent_id'] = kwargs['event_id']
            context['superevent_pk'] = superevent.pk
            context['sequences'] = json.dumps(sequences)
            context['tom_api_url'] = settings.TOM_API_URL
            context['hermes_api_url'] = settings.HERMES_API_URL
            return context
        except NonLocalizedEvent.DoesNotExist:
            raise Http404
