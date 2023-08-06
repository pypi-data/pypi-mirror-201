"""
Transport Value

This model calculates the `distance` of the [Transport](https://hestia.earth/schema/Transport) linked to the
[Inputs of the Cycle](https://hestia.earth/schema/Cycle#inputs) by calculating the distance between the
country of the Cycle and the country of origin of the Input (which must be different).
"""
from haversine import haversine
from hestia_earth.utils.api import download_hestia
from hestia_earth.utils.tools import non_empty_list

from hestia_earth.models.log import logRequirements, logShouldRun, debugValues
from hestia_earth.models.utils import _include_methodModel
from .. import MODEL

REQUIREMENTS = {
    "Cycle": {
        "inputs": [{
            "@type": "Input",
            "country": {"@type": "Term", "termType": "region"},
            "transport": [{"@type": "Transport"}]
        }],
        "site": {
            "@type": "Site",
            "country": {"@type": "Term", "termType": "region"}
        }
    }
}
RETURNS = {
    "Transport": [{
        "distance": ""
    }]
}
MODEL_KEY = 'distance'


def _run_transport(cycle: dict, distance_kms: float):
    def exec(transport: dict):
        return _include_methodModel({
            **transport, MODEL_KEY: distance_kms
        }, MODEL) if _should_run_transport(cycle, transport) else transport
    return exec


def _should_run_transport(cycle: dict, transport: dict):
    term_id = transport.get('term', {}).get('@id')
    value_not_set = len(transport.get(MODEL_KEY, [])) == 0

    should_run = all([value_not_set])

    # skip logs if we don't run the model to avoid showing an "error"
    if should_run:
        logRequirements(cycle, model=MODEL, term=term_id, key=MODEL_KEY,
                        value_not_set=value_not_set)
        logShouldRun(cycle, MODEL, term_id, should_run, key=MODEL_KEY)
    return should_run


def _run_input(cycle: dict, site_country: dict):
    def exec(input: dict):
        term_id = input.get('term', {}).get('@id')
        input_country = download_hestia(input.get('country', {}).get('@id'))
        distance_kms = haversine(
            (site_country.get('latitude'), site_country.get('longitude')),
            (input_country.get('latitude'), input_country.get('longitude'))
        )
        debugValues(cycle, model=MODEL, term=term_id, key=MODEL_KEY,
                    distance_kms=distance_kms)
        transport = input.get('transport')
        return {
            **input,
            **({'transport': list(map(_run_transport(cycle, distance_kms), transport))} if transport else {})
        }
    return exec


def _should_run_input(site_country: str):
    def exec(input: dict):
        input_country = input.get('country', {}).get('@id')
        has_transports = len(input.get('transport', [])) > 0
        should_run = all([has_transports, input_country, input_country != site_country])
        return should_run
    return exec


def run(cycle: dict):
    site_country = cycle.get('site', {}).get('country', {}).get('@id')
    inputs = list(filter(_should_run_input(site_country), cycle.get('inputs', [])))
    # download full term to get coordinates only if there is anything to run
    site_country = download_hestia(site_country) if len(inputs) > 0 else site_country
    return non_empty_list(map(_run_input(cycle, site_country), inputs))
