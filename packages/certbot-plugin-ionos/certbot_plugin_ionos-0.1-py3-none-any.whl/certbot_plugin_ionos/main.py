import zope.interface
import logging
import uuid

from certbot import interfaces, errors
from certbot.plugins import dns_common

from ionos_api import Client
from ionos_api.Model import RecordDefinition


logger = logging.getLogger(__name__)


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for Gandi (using LiveDNS)."""

    description = 'Obtain certificates using a DNS TXT record (if you are using Gandi for DNS).'


    def __init__(self, config, name, **kwargs):
        if name in ("dns", "certbot-plugin-ionos:dns"):
            logger.warning("Certbot is moving to remove 3rd party plugins prefixes. Please use --authenticator dns-ionos --dns-ionos-config")

        super(Authenticator, self).__init__(config, name, **kwargs)
        self.credentials = None


    @classmethod
    def add_parser_arguments(cls, add):  # pylint: disable=arguments-differ
        super(Authenticator, cls).add_parser_arguments(add)
        add('config', help='Ionos API configuration INI file.')


    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return 'This plugin configures a DNS TXT record to respond to a dns-01 challenge using ' + \
               'the Ionos DNS API.'

    def _validate_sharing_id(self, credentials):
        sharing_id = credentials.conf('sharing-id')
        if sharing_id:
            try:
                uuid.UUID(sharing_id, version=4)
            except ValueError:
                raise errors.PluginError("Invalid sharing_id: {0}.".format(sharing_id))

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            'config',
            'Ionos API configuration INI file.',
            {
                'url': 'Location of the API service',
                'key-prefix': 'Prefix for the API key',
                'key': 'API key for DNS management',
            },
            self._validate_sharing_id
        )


    def _perform(self, domain, validation_name, validation):
        rec = RecordDefinition(name=validation_name, type="TXT", content=validation)
        self._get_ionos_cli().add_record(rec)
        # TODO: Handle error
        #if error is not None:
        #    raise errors.PluginError('An error occurred adding the DNS TXT record: {0}'.format(error))


    def _cleanup(self, domain, validation_name, validation):
        rec = RecordDefinition(name=validation_name, type="TXT", content=validation)
        self._get_ionos_cli().remove_record(rec)
        #error = gandi_api.del_txt_record(self._get_gandi_config(), domain, validation_name, validation)
        #if error is not None:
        #    logger.warn('Unable to find or delete the DNS TXT record: %s', error)


    def _get_ionos_cli(self) -> Client:
        return Client(self.credentials.conf('url'),
                      ".".join((self.credentials.conf('key-prefix'),
                                self.credentials.conf('key'))))