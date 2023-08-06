''' This class defines a message handler for a tom_alertstreams connection to GW events

'''
import logging
import os
import traceback

from tom_nonlocalizedevents.models import NonLocalizedEvent, EventSequence
from tom_nonlocalizedevents.healpix_utils import create_localization_for_multiorder_fits

logger = logging.getLogger(__name__)


EXPECTED_FIELDS = [
    'TRIGGER_NUM',
    'SEQUENCE_NUM',
    'NOTICE_TYPE',
    'SKYMAP_FITS_URL'
]


def extract_fields(message, expected_fields):
    fields = {}
    keys = message.split('\n')
    for key in keys:
        if key:
            field_name = key.split(':')[0]
            if field_name in expected_fields:
                fields[field_name] = key.split(':', maxsplit=1)[1].strip()
    if set(expected_fields) != set(fields.keys()):
        logger.warning(f"Incoming GW message did not have the expected fields, ignoring it: {keys}")
        return {}

    return fields


def get_moc_url_from_skymap_fits_url(skymap_fits_url):
    base, filename = os.path.split(skymap_fits_url)
    # Repair broken skymap filenames given in gcn mock alerts right now
    if filename.endswith('.fit'):
        filename = filename + 's'
    # Replace the non-MOC skymap url provided with the MOC version, but keep the ,# on the end
    filename = filename.replace('LALInference.fits.gz', 'LALInference.multiorder.fits')
    filename = filename.replace('bayestar.fits.gz', 'bayestar.multiorder.fits')
    return os.path.join(base, filename)


def handle_message(message):
    # It receives a bytestring message or a Kafka message in the LIGO GW format
    # fields must be extracted from the message text and stored into in the model
    if not isinstance(message, bytes):
        bytes_message = message.value()
    else:
        bytes_message = message
    fields = extract_fields(bytes_message.decode('utf-8'), EXPECTED_FIELDS)
    if fields:
        nonlocalizedevent, nle_created = NonLocalizedEvent.objects.get_or_create(
            event_id=fields['TRIGGER_NUM'],
            event_type=NonLocalizedEvent.NonLocalizedEventType.GRAVITATIONAL_WAVE,
        )
        if nle_created:
            logger.info(f"Ingested a new GW event with id {fields['TRIGGER_NUM']} from alertstream")
        # Next attempt to ingest and build the localization of the event
        try:
            localization = create_localization_for_multiorder_fits(
                nonlocalizedevent=nonlocalizedevent,
                multiorder_fits_url=get_moc_url_from_skymap_fits_url(fields['SKYMAP_FITS_URL'])
            )
        except Exception as e:
            localization = None
            logger.error(f'Could not create EventLocalization for messsage: {fields}. Exception: {e}')
            logger.error(traceback.format_exc())

        # Now ingest the sequence for that event
        event_sequence, es_created = EventSequence.objects.update_or_create(
            nonlocalizedevent=nonlocalizedevent,
            localization=localization,
            sequence_id=fields['SEQUENCE_NUM'],
            defaults={
                'event_subtype': fields['NOTICE_TYPE']
            }
        )
        if es_created and localization is None:
            warning_msg = (f'{"Creating" if es_created else "Updating"} EventSequence without EventLocalization:'
                           f'{event_sequence} for NonLocalizedEvent: {nonlocalizedevent}')
            logger.warning(warning_msg)


def handle_retraction(message):
    # It receives a bytestring message or a Kafka message in the LIGO GW format
    # For a retraction message, we just set the events status to retracted if it exists.
    if not isinstance(message, bytes):
        bytes_message = message.value()
    else:
        bytes_message = message
    # Just need the event_id from the retraction messages
    fields = extract_fields(bytes_message.decode('utf-8'), ['TRIGGER_NUM'])
    # Then set the state to 'RETRACTED' for the event matching that id
    try:
        retracted_event = NonLocalizedEvent.objects.get(event_id=fields['TRIGGER_NUM'])
        retracted_event.state = NonLocalizedEvent.NonLocalizedEventState.RETRACTED
        retracted_event.save()
    except NonLocalizedEvent.DoesNotExist:
        logger.warning((f"Got a Retraction notice for event id {fields['TRIGGER_NUM']}"
                        f"which does not exist in the database"))
