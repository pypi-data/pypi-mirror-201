from typing import Callable

from dtn7zero.constants import RUNNING_MICROPYTHON, PORT_REST
from dtn7zero.data import BundleInformation
from dtn7zero.utility import debug
from py_dtn7 import Bundle, DTNRESTClient, to_dtn_timestamp
from py_dtn7.bundle import BundleProcessingControlFlags, PrimaryBlock, HopCountBlock, PayloadBlock, BundleAgeBlock, NONE_ENDPOINT_SPECIFIC_PART_NAME


class LocalEndpoint:
    def __init__(self, endpoint_identifier: str, receive_callback=Callable[[Bundle], None]):
        """ The LocalEndpoint is the entry-point for the application to send/receive bundles.

        endpoint_identifier examples:
            dtn addressing scheme -> "echo", "echo/subecho"
            ipn addressing scheme -> "12", "24.15.16"

        callback may be None, but then the endpoint should be regularly polled for new bundles.
        """

        self.endpoint_identifier = endpoint_identifier
        self.receive_callback = receive_callback

        if receive_callback is None:
            self.bundle_buffer: list[Bundle] = []

        self.bpa = None

        self.last_bundle_creation_time = 0
        self.last_sequence_number = 0

    def bpa_local_bundle_delivery(self, bundle: Bundle):
        if self.receive_callback is None:
            self.bundle_buffer.append(bundle)
        else:
            self.receive_callback(bundle)

    @property
    def full_endpoint_uri(self):
        if self.bpa.full_node_uri.startswith('dtn'):
            return '{}{}'.format(self.bpa.full_node_uri, self.endpoint_identifier)
        elif not self.endpoint_identifier:
            return self.bpa.full_node_uri  # special case -> ipn addressing + '' empty endpoint (direct node endpoint)
        else:
            return '{}.{}'.format(self.bpa.full_node_uri, self.endpoint_identifier)

    def bpa_register(self, bpa):
        self.bpa = bpa

    def bpa_unregister(self):
        self.bpa = None

    def poll(self):
        if self.receive_callback is not None:
            raise Exception('cannot poll active endpoint with callback {}'.format(self.endpoint_identifier))
        if not self.bundle_buffer:
            return None
        return self.bundle_buffer.pop(0)

    def start_transmission(self, payload: bytes, full_destination_uri: str, lifetime: int = 3600 * 24 * 1000, anonymous=False) -> str:
        if self.bpa is None:
            raise Exception('cannot start transmission on unregistered LocalEndpoint {}'.format(self.endpoint_identifier))

        bundle_processing_control_flags = BundleProcessingControlFlags(0)
        bundle_processing_control_flags.set_flag(2)  # do not fragment bundle

        bundle_age_block = None

        if RUNNING_MICROPYTHON:
            self.last_sequence_number += 1

            bundle_age_block = BundleAgeBlock.from_objects()
        else:
            current_time = to_dtn_timestamp()
            if current_time == self.last_bundle_creation_time:
                self.last_sequence_number += 1
            else:
                self.last_bundle_creation_time = current_time
                self.last_sequence_number = 0

        if full_destination_uri.startswith('dtn'):
            anonymous_uri = 'dtn:{}'.format(NONE_ENDPOINT_SPECIFIC_PART_NAME)
        else:
            anonymous_uri = 'ipn:{}'.format(NONE_ENDPOINT_SPECIFIC_PART_NAME)

        primary_block = PrimaryBlock.from_objects(
            full_destination_uri=full_destination_uri,
            full_source_uri=anonymous_uri if anonymous else self.full_endpoint_uri,
            full_report_to_uri=anonymous_uri if anonymous else self.bpa.full_node_uri,
            bundle_processing_control_flags=bundle_processing_control_flags,
            bundle_creation_time=self.last_bundle_creation_time,
            sequence_number=self.last_sequence_number,
            lifetime=lifetime
        )

        hop_count_block = HopCountBlock.from_objects(hop_limit=32, hop_count=0)

        payload_block = PayloadBlock.from_objects(data=payload)

        bundle = Bundle(
            primary_block=primary_block,
            bundle_age_block=bundle_age_block,
            hop_count_block=hop_count_block,
            payload_block=payload_block
        )

        debug('starting transmission of bundle: {}'.format(bundle.bundle_id))

        self.bpa.local_bundle_dispatch_queue.append(BundleInformation(bundle))

        return bundle.bundle_id

    def cancel_transmission(self, bundle_id: str) -> bool:
        if self.bpa is None:
            raise Exception('cannot cancel transmission on unregistered LocalEndpoint {}'.format(self.endpoint_identifier))

        return self.bpa.cancel_transmission(bundle_id)


class RemoteEndpoint:

    def __init__(self, dtn7rs_ip: str, endpoint_specific_part: str):
        """
        This is a relic of a time when we could not generate bundles on our own.

        It is functional and encapsulated, meaning it requires no other dtn7zero dependencies to operate.
        """
        self.endpoint_specific_part = endpoint_specific_part

        self.dtn_rest_client: DTNRESTClient = DTNRESTClient('http://{}'.format(dtn7rs_ip), PORT_REST)

        self.dtn_rest_client.register(self.endpoint_specific_part)

    def __del__(self):
        self.dtn_rest_client.unregister(self.endpoint_specific_part)

    @property
    def full_endpoint_address(self):
        return '//{}/{}'.format(self.dtn_rest_client.node_id, self.endpoint_specific_part)

    def poll(self):
        raw_bundle = self.dtn_rest_client.fetch_endpoint(self.endpoint_specific_part)

        if b'Nothing to receive' == raw_bundle:
            return None
        else:
            return Bundle.from_cbor(raw_bundle)

    def start_transmission(self, payload: bytes, full_destination_uri: str, lifetime: int = 3600 * 24 * 1000) -> str:
        if self.dtn_rest_client is None:
            raise Exception('cannot start transmission on unregistered RemoteEndpoint {}'.format(self.endpoint_specific_part))

        response = self.dtn_rest_client.send(payload=payload, destination=full_destination_uri, lifetime=lifetime)

        if response.status_code != 200:
            raise Exception('error occurred on generating a bundle on RemoteEndpoint {}'.format(self.full_endpoint_address))

        return ''  # currently we do not get the bundle-id of the generated bundle from the remote :(
