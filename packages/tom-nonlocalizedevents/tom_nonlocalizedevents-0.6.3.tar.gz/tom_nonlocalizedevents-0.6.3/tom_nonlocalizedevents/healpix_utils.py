''' This set of methods supports generating and querying healpix MOC maps for GW events,
    using healpix_alchemy and model mappings with sql_alchemy queries.
'''
from astropy.table import Table
from astropy.io import fits
from tom_nonlocalizedevents.models import EventCandidate, SkymapTile, EventLocalization, CredibleRegion
from django.db import transaction
from django.conf import settings
from healpix_alchemy.constants import HPX, LEVEL
from healpix_alchemy.types import Tile, Point
import sqlalchemy as sa
from sqlalchemy.orm import relationship, declarative_base, Session
from astropy_healpix import uniq_to_level_ipix
from mocpy import MOC
from ligo.skymap import distance
from dateutil.parser import parse
import os
import sys
import json
import logging

# from django.db.models import Sum, Subquery, F, Min
# from tom_nonlocalizedevents_base.settings import DATABASES


logger = logging.getLogger(__name__)

POOL_RECYCLE = 4 * 60 * 60
SA_DB_CONNECTION_URL = os.getenv(
    'SA_DB_CONNECTION_URL',
    (f"postgresql://{settings.DATABASES['default']['USER']}:{settings.DATABASES['default']['PASSWORD']}"
     f"@{settings.DATABASES['default']['HOST']}:{settings.DATABASES['default']['PORT']}"
     f"/{settings.DATABASES['default']['NAME']}"))
CREDIBLE_REGION_PROBABILITIES = sorted(json.loads(os.getenv(
    'CREDIBLE_REGION_PROBABILITIES', '[0.25, 0.5, 0.75, 0.9, 0.95]')), reverse=True)

Base = declarative_base()
sa_engine = sa.create_engine(SA_DB_CONNECTION_URL, pool_recycle=POOL_RECYCLE)


def uniq_to_bigintrange(value):
    level, ipix = uniq_to_level_ipix(value)
    shift = 2 * (LEVEL - level)
    return (ipix << shift, (ipix + 1) << shift)


def sequence_to_bigintrange(sequence):
    return f'[{sequence[0]},{sequence[1]})'


def tiles_from_moc(moc):
    return (f'[{lo},{hi})' for lo, hi in moc._interval_set.nested)


def tiles_from_polygon_skycoord(polygon):
    return tiles_from_moc(MOC.from_polygon_skycoord(polygon.transform_to(HPX.frame)))


def create_localization_for_multiorder_fits(nonlocalizedevent, multiorder_fits_url):
    ''' Takes in a GraceDB url to multiorder fits file and creates the skymap tiles in db
    '''
    logger.info(f"Creating localization for {nonlocalizedevent.event_id} with MOC skymap {multiorder_fits_url}")
    header = fits.getheader(multiorder_fits_url, 1)
    creation_date = parse(header.get('DATE'))
    try:
        localization = EventLocalization.objects.get(nonlocalizedevent=nonlocalizedevent, date=creation_date)
    except EventLocalization.DoesNotExist:
        distance_mean = header.get('DISTMEAN')
        distance_std = header.get('DISTSTD')
        data = Table.read(multiorder_fits_url)
        row_dist_mean, row_dist_std, _ = distance.parameters_to_moments(data['DISTMU'], data['DISTSIGMA'])
        with transaction.atomic():
            localization = EventLocalization.objects.create(
                nonlocalizedevent=nonlocalizedevent,
                distance_mean=distance_mean,
                distance_std=distance_std,
                skymap_moc_file_url=multiorder_fits_url,
                date=creation_date
            )
            for i, row in enumerate(data):
                # This is necessary to make sure we don't get an underflow error in postgres
                # when operating with the probdensity float field
                probdensity = row['PROBDENSITY'] if row['PROBDENSITY'] > sys.float_info.min else 0
                SkymapTile.objects.create(
                    localization=localization,
                    tile=uniq_to_bigintrange(row['UNIQ']),
                    probdensity=probdensity,
                    distance_mean=row_dist_mean[i],
                    distance_std=row_dist_std[i]
                )
    return localization


# healpix_alchemy models pointing to django ORM models, for building a sql alchemy query
class SaSkymap(Base):
    __tablename__ = 'tom_nonlocalizedevents_eventlocalization'
    id = sa.Column(sa.Integer, primary_key=True)
    tiles = relationship(lambda: SaSkymapTile)


class SaSkymapTile(Base):
    __tablename__ = 'tom_nonlocalizedevents_skymaptile'
    id = sa.Column(sa.Integer, primary_key=True)
    localization_id = sa.Column(sa.ForeignKey(SaSkymap.id), primary_key=True)
    tile = sa.Column(Tile, primary_key=True, index=True)
    probdensity = sa.Column(sa.Float, nullable=False)
    distance_mean = sa.Column(sa.Float, nullable=False)
    distance_std = sa.Column(sa.Float, nullable=False)


class SaTarget(Base):
    __tablename__ = 'tom_targets_target'
    id = sa.Column(sa.Integer, primary_key=True)
    distance = sa.Column(sa.Float, nullable=True)
    distance_err = sa.Column(sa.Float, nullable=True)


class SaEventCandidate(Base):
    __tablename__ = 'tom_nonlocalizedevents_eventcandidate'
    id = sa.Column(sa.Integer, primary_key=True)
    target_id = sa.Column(sa.ForeignKey(SaTarget.id), primary_key=True)
    healpix = sa.Column(Point, index=True, nullable=False)


def update_all_credible_region_percents_for_candidates(eventlocalization, event_candidate_ids=None):
    ''' This helper function runs through the defined set of discrete credible region probabilities
        and creates or updates the probability of a credible region for each of the event candidates
        that fall within the event localization's credible region of that priority
    '''
    if not event_candidate_ids:
        event_candidate_ids = list(eventlocalization.nonlocalizedevent.candidates.values_list('pk', flat=True))
    for probability in CREDIBLE_REGION_PROBABILITIES:
        update_credible_region_percent_for_candidates(eventlocalization, probability, event_candidate_ids)


def update_credible_region_percent_for_candidates(eventlocalization, prob, event_candidate_ids=None):
    ''' This function creates a credible region linkage with probability prob for each of the event candidate
        ids supplied if they fall within that prob for the event location specified.
    '''
    if not event_candidate_ids:
        event_candidate_ids = list(eventlocalization.nonlocalizedevent.candidates.values_list('pk', flat=True))

    session = Session(sa_engine)

    cum_prob = sa.func.sum(
        SaSkymapTile.probdensity * SaSkymapTile.tile.area
    ).over(
        order_by=SaSkymapTile.probdensity.desc()
    ).label(
        'cum_prob'
    )

    subquery = sa.select(
        SaSkymapTile.probdensity,
        cum_prob
    ).filter(
        SaSkymapTile.localization_id == eventlocalization.id
    ).subquery()

    min_probdensity = sa.select(
        sa.func.min(subquery.columns.probdensity)
    ).filter(
        subquery.columns.cum_prob <= prob
    ).scalar_subquery()

    query = sa.select(
        SaEventCandidate.id
    ).filter(
        SaEventCandidate.id.in_(event_candidate_ids),
        SaSkymapTile.localization_id == eventlocalization.id,
        SaSkymapTile.tile.contains(SaEventCandidate.healpix),
        SaSkymapTile.probdensity >= min_probdensity
    )

    results = session.execute(query)

    for sa_event_candidate_id in results:
        CredibleRegion.objects.update_or_create(
            candidate=EventCandidate.objects.get(id=sa_event_candidate_id[0]),
            localization=eventlocalization,
            defaults={
                'smallest_percent': int(prob * 100.0)
            }
        )


# def point_in_range_django(eventlocalization, prob):
# This code is a beginning attempt to translate the healpix_alchemy query from sql_alchemy to django ORM
# It is non-functional and needs more work to get right.
#     event_candidate_ids = list(eventlocalization.nonlocalizedevent.candidates.values_list('pk', flat=True))

#     SkymapTile.objects.order_by('-probdensity').aggregate(cum_prob=Sum(F('probdensity') * F('tile__area')))

#     cum_prob = SkymapTile.objects.order_by('-probdensity').alias(cum_prob=Sum(F('probdensity') *
#                F('tile__area'))).annotate(cum_prob=F('cum_prob'),
#     )
#     min_probdensity = SkymapTile.objects.order_by('-probdensity').alias(
#         cum_prob=Sum(F('probdensity') * F('tile__area')), min_probdensity=Min(F('probdensity'))).annotate(
#         cum_prob=F('cum_prob'), min_probdensity=F('min_probdensity')
#     ).filter(
#         localization__id=eventlocalization.id,
#         cum_prob__lte=prob,
#         probdensity__gte=min_probdensity,
#         tile__contains=
#         localization__nonlocalizedevent__candidates
#     )
#     candidates = EventCandidate.objects.filter(
#         nonlocalizedevent=eventlocalization.nonlocalizedevent,
#         eventlocalization__tiles__contains(healpix)
#     ).values('id')
