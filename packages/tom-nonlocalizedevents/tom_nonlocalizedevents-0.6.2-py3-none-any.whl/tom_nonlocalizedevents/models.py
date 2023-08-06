from django.db import models
from django.contrib.postgres.fields import BigIntegerRangeField
from django.contrib.postgres.indexes import SpGistIndex

from tom_targets.models import Target

import numpy as np
from psycopg2.extensions import register_adapter, AsIs
from healpix_alchemy.constants import HPX
from astropy.coordinates import SkyCoord
import logging


def adapt_numpy_float64(np_float64):
    return AsIs(np_float64)


def adapt_numpy_int64(np_int64):
    return AsIs(np_int64)


register_adapter(np.float64, adapt_numpy_float64)
register_adapter(np.int64, adapt_numpy_int64)


logger = logging.getLogger(__name__)


class NonLocalizedEvent(models.Model):
    """Represents a NonLocalizedEvent being followed-up upon by this TOM.

    A NonLocalizedEvent is distinguished from a Target in that it is localized to a region of the sky
    (vs. a specific RA,DEC). The potential Targets in the localization region must be identified,
    prioritized, and categorized (retired, of-interest, etc) for follow-up EM observations

    For the moment, this is rather GraceDB (GW) specific, but sh/could be generalized to work
    with gamma-ray burst and neutrino events.
    """

    class NonLocalizedEventType(models.TextChoices):
        GRAVITATIONAL_WAVE = 'GW', 'Gravitational Wave'
        GAMMA_RAY_BURST = 'GRB', 'Gamma-ray Burst'
        NEUTRINO = 'NU', 'Neutrino'
        UNKNOWN = 'UNK', 'Unknown'

    class NonLocalizedEventState(models.TextChoices):
        ACTIVE = 'ACTIVE'
        INACTIVE = 'INACTIVE'
        RETRACTED = 'RETRACTED'

    state = models.CharField(
        max_length=16,
        choices=NonLocalizedEventState.choices,
        default=NonLocalizedEventState.ACTIVE,
        help_text='The current state of this NonLocalizedEvent'
    )

    event_type = models.CharField(
        max_length=3,
        choices=NonLocalizedEventType.choices,
        default=NonLocalizedEventType.GRAVITATIONAL_WAVE,
        help_text='The type of NonLocalizedEvent, used for determining how to ingest and display it'
    )
    # TODO: ask Curtis/Rachel/Andy about generalized use cases.
    event_id = models.CharField(
        max_length=64,
        help_text='Unique identifer for the event. I.E. the TRIGGER_NUM for a GW event.'
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['event_id'], name='unique_event_id')
        ]

    @property
    def gracedb_url(self):
        """Construct and return the GraceDB URL for this nonlocalizedevent from the event_id Field.

        for example, https://gracedb.ligo.org/superevents/S200316bj/
        """
        # TODO: add check that superevent_type is GRAVITATIONAL_WAVE
        return f"https://gracedb.ligo.org/superevents/{self.event_id}/"

    @property
    def treasuremap_url(self):
        """Construct and return the Treasure Map (treasuremap.space) URL for this nonlocalizedevent
        from the event_id Field.

        for example: http://treasuremap.space/alerts?graceids=S200219ac
        """
        # TODO: add check that superevent_type is GRAVITATIONAL_WAVE
        return f"http://treasuremap.space/alerts?graceids={self.event_id}"

    def __str__(self):
        return f"{self.event_id}"


class EventLocalization(models.Model):
    """Represents a region of the sky in which a nonlocalizedevent may have taken place.
    """
    nonlocalizedevent = models.ForeignKey(NonLocalizedEvent, related_name='localizations', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    date = models.DateTimeField(
        help_text='The datestamp of this localizations creation.'
    )
    skymap_moc_file_url = models.URLField(
        default='',
        help_text='The URL to a file containing skymap MOC file for the event sequence. Used to generate localization.'
    )
    distance_mean = models.FloatField(
        default=0,
        help_text='The posterior mean distance in Mpc.'
    )
    distance_std = models.FloatField(
        default=0,
        help_text='The posterior standard deviation of the distance in Mpc.'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['nonlocalizedevent', 'date'], name='unique_date_per_nonlocalizedevent')
        ]


class EventSequence(models.Model):
    nonlocalizedevent = models.ForeignKey(NonLocalizedEvent, related_name='sequences', on_delete=models.CASCADE)
    localization = models.ForeignKey(EventLocalization, related_name='sequences', null=True, on_delete=models.SET_NULL)
    sequence_id = models.PositiveIntegerField(
        default=1,
        help_text='The version / update number of this event. I.E. the SEQUENCE_NUM for a GW event.'
    )
    event_subtype = models.CharField(
        max_length=256,
        default='',
        help_text='The subtype of the event. Options are type specific, i.e. GW events have initial, '
                  'preliminary, update types.'
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['nonlocalizedevent', 'sequence_id'],
                name='unique_sequence_per_nonlocalizedevent'
            )
        ]
    # far = models.FloatField(
    #     default=0,
    #     verbose_name='false alarm rate',
    #     help_text='The estimated false alarm rate'
    # )
    # event_probabilities = models.JSONField(
    #     default=dict,
    #     blank=True,
    #     help_text='A dictionary of potential event source probabilities'
    # )
    # details = models.JSONField(
    #     default=dict,
    #     blank=True,
    #     help_text='A dictionary for extra details related to this sequence of the event.'
    # )


class EventCandidate(models.Model):
    target = models.ForeignKey(Target, on_delete=models.CASCADE)
    nonlocalizedevent = models.ForeignKey(NonLocalizedEvent, related_name='candidates', on_delete=models.CASCADE)

    viable = models.BooleanField(
        default=True,
        help_text='Whether this event candidate is actively being considered or not'
    )
    viability_reason = models.TextField(
        default='',
        help_text='Reason why this candidates viability is set the way it is.'
    )
    priority = models.IntegerField(
        default=1,
        # TODO: add description, etc
    )
    healpix = models.BigIntegerField(
        default=-1,
        help_text='Stores the healpix index for this candidates target, used for MOC lookups'
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.target:
            self.healpix = HPX.skycoord_to_healpix(SkyCoord(self.target.ra, self.target.dec, unit='deg'))
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['target', 'nonlocalizedevent'], name='unique_target_nonlocalizedevent')
        ]

    def __str__(self):
        return f'EventCandidate({self.id}) NonLocalizedEvent: {self.nonlocalizedevent} Target: {self.target}'


class CredibleRegion(models.Model):
    localization = models.ForeignKey(EventLocalization, related_name='credibleregions', on_delete=models.CASCADE)
    candidate = models.ForeignKey(EventCandidate, related_name='credibleregions', on_delete=models.CASCADE)

    smallest_percent = models.IntegerField(
        default=100,
        help_text='Smallest percent credible region this candidate falls into for this localization.'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['localization', 'candidate'], name='unique_localization_candidate')
        ]


class SkymapTile(models.Model):
    """ A healpix_alchemy style tile linked to an event localization
    """
    localization = models.ForeignKey(EventLocalization, related_name='tiles', on_delete=models.CASCADE)
    tile = BigIntegerRangeField(db_index=True)
    probdensity = models.FloatField(null=False)
    distance_mean = models.FloatField(
        default=0
    )
    distance_std = models.FloatField(
        default=0
    )

    class Meta:
        indexes = [SpGistIndex(fields=('tile',))]
