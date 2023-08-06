import subprocess
import sys
from os import path
from typing import List, Callable
from enum import Enum
from dataclasses import dataclass

from certbot.main import main as _certbot_main

from .Config import API_CONFIGS_LOCATION
from .Tools import StdOutCapture, package_available


@dataclass
class DNSAPIWrapper:
    error: Callable[[], List[str]]
    certbot_args: List[str]


class DNSProviders(str, Enum):
    GANDI = "Gandi"
    IONOS = "Ionos"


def _gandi_errors():
    def err_gen():
        if not package_available("certbot_plugin_gandi"):
            yield "Dependency \"certbot-plugin-gandi\" is not installed."
        # TODO: Check config ?
        if not path.exists(f"{API_CONFIGS_LOCATION}/gandi.ini"):
            yield "Configuration file \"gandi.ini\" not found in the config directory \"%s\"." % API_CONFIGS_LOCATION

    return list(err_gen())


def _ionos_errors():
    def err_gen():
        if not package_available("certbot_plugin_ionos"):
            yield "Dependency \"certbot-plugin-ionos\" is not installed."
        # TODO: Check config ?
        if not path.exists(f"{API_CONFIGS_LOCATION}/ionos.ini"):
            yield "Configuration file \"ionos.ini\" not found in the config directory \"%s\"." % API_CONFIGS_LOCATION

    return list(err_gen())


Provider2API = {
    DNSProviders.GANDI.value: DNSAPIWrapper(
        _gandi_errors,
        ["dns-gandi", "--dns-gandi-credentials", f"{API_CONFIGS_LOCATION}/gandi.ini"]
    ),

    DNSProviders.IONOS.value: DNSAPIWrapper(
        _ionos_errors,
        ["dns-ionos", "--dns-ionos-config", f"{API_CONFIGS_LOCATION}/ionos.ini"]
    )
}

AvailableDNSProviders = Enum("AvailableDNSProviders", [(a.name, a.value) for a in DNSProviders
                             if len(Provider2API[a].error()) == 0])

UnavailableDNSProviders = Enum("UnavailableDNSProviders", [(a.name, a.value) for a in DNSProviders
                             if len(Provider2API[a].error()) != 0])


class CertbotManager:
    def __init__(self, certs_location):
        self.certs_location = certs_location

    def update_certs(self):
        subprocess.call(["rsync", "-raL", "--delete", "/etc/letsencrypt/live/", self.certs_location])

    def list_certs(self):
        # TODO: Parse & jsonify (dict / list).
        with StdOutCapture() as lines:
            _certbot_main(["certificates"])

        return "\n".join(lines)

    @classmethod
    def cert_related_op(cls, dns_provider: DNSProviders):
        if dns_provider.value not in Provider2API.keys():
            raise ValueError("No API configured for the DNS provider %s" % dns_provider)

        api_conf = Provider2API[dns_provider.value]

        api_conf_error = api_conf.error()
        if api_conf_error:
            raise RuntimeError(api_conf_error)

        yield "--authenticator"
        for a in api_conf.certbot_args:
            yield a

    def register_cert(self, dns_provider: DNSProviders, domains: List[str], email: str):
        def args_generator():
            yield "certonly"

            for a in CertbotManager.cert_related_op(dns_provider):
                yield a

            yield "--email"
            yield email

            for d in domains:
                yield "-d"
                yield d

            yield "--agree-tos"
            yield "-n"

        with StdOutCapture() as lines:
            _certbot_main(list(args_generator()))

        self.update_certs()

        return "\n".join(lines)

    def renew_cert(self, dns_provider: DNSProviders, name: str, force: bool = False):
        def args_generator():
            yield "renew"
            if force:
                yield "--force-renewal"

            for a in CertbotManager.cert_related_op(dns_provider):
                yield a

            yield "--cert-name"
            yield name

            yield "--agree-tos"
            yield "-n"

        with StdOutCapture() as lines:
            _certbot_main(list(args_generator()))

        self.update_certs()

        return "\n".join(lines)

    def delete_cert(self, name: str):
        with StdOutCapture() as lines:
            _certbot_main(["delete", "--cert-name", name, "-n"])

        self.update_certs()
        return "\n".join(lines)

    def list_plugin_errors(self, dns_provider: DNSProviders):
        return Provider2API[dns_provider.value].error()
