from unittest.mock import patch
import json

from tests.utils import fixtures_path
from hestia_earth.validation.utils import _group_nodes
from hestia_earth.validation.validators.input import (
    validate_must_include_id,
    validate_input_country,
    validate_related_impacts,
    validate_fertiliser_value,
    validate_animalFeed_requires_isAnimalFeed
)


class_path = 'hestia_earth.validation.validators.input'


def test_validate_must_include_id_valid():
    # no inputs should be valid
    assert validate_must_include_id([]) is True

    with open(f"{fixtures_path}/input/mustIncludeId/valid.json") as f:
        data = json.load(f)
    assert validate_must_include_id(data.get('nodes')) is True

    with open(f"{fixtures_path}/input/mustIncludeId/valid-multiple-ids.json") as f:
        data = json.load(f)
    assert validate_must_include_id(data.get('nodes')) is True


def test_validate_must_include_id_invalid():
    with open(f"{fixtures_path}/input/mustIncludeId/invalid.json") as f:
        data = json.load(f)
    assert validate_must_include_id(data.get('nodes')) == {
        'level': 'warning',
        'dataPath': '.inputs[0]',
        'message': 'should add missing inputs: potassiumNitrateKgK2O'
    }


def test_validate_input_country_valid():
    # no inputs should be valid
    assert validate_input_country({}) is True

    with open(f"{fixtures_path}/input/country/valid.json") as f:
        cycle = json.load(f)
    assert validate_input_country(cycle, 'inputs') is True


def test_validate_input_country_invalid():
    with open(f"{fixtures_path}/input/country/invalid.json") as f:
        cycle = json.load(f)
    assert validate_input_country(cycle, 'inputs') == {
        'level': 'error',
        'dataPath': '.inputs[1].country',
        'message': 'must be a country'
    }


def test_validate_related_impacts_valid():
    # no inputs should be valid
    assert validate_related_impacts({}, 'inputs') is True

    with open(f"{fixtures_path}/input/impactAssessment/valid.json") as f:
        nodes = json.load(f).get('nodes')
    assert validate_related_impacts(nodes[0], 'inputs', _group_nodes(nodes)) is True


def test_validate_related_impacts_invalid():
    with open(f"{fixtures_path}/input/impactAssessment/invalid.json") as f:
        nodes = json.load(f).get('nodes')
    assert validate_related_impacts(nodes[0], 'inputs', _group_nodes(nodes)) == {
        'level': 'error',
        'dataPath': '.inputs[1].impactAssessment',
        'message': 'can not be linked to the same Cycle'
    }


def fake_get_post(_country_id, product_id, fert_id):
    return {
        'inorganicPhosphorusFertiliserUnspecifiedKgP2O5': (44, 4),
        'inorganicPotassiumFertiliserUnspecifiedKgK2O': (84, 8),
        'inorganicNitrogenFertiliserUnspecifiedKgN': (166, 12),
        'ammoniumSulphateKgN': (166, 12),
        'ureaKgN': (166, 12),
    }[fert_id]


def test_validate_fertiliser_value_incomplete_valid(*args):
    with open(f"{fixtures_path}/input/fertiliser/incomplete/valid.json") as f:
        cycle = json.load(f)
    assert validate_fertiliser_value(cycle, cycle.get('site')) is True


@patch(f"{class_path}.get_post", side_effect=fake_get_post)
def test_validate_fertiliser_value_complete_invalid(*args):
    with open(f"{fixtures_path}/input/fertiliser/complete/invalid.json") as f:
        cycle = json.load(f)
    assert validate_fertiliser_value(cycle, cycle.get('site'), 'inputs') == [
        {
            'level': 'warning',
            'dataPath': '.inputs[0].value',
            'message': 'is outside confidence interval',
            'params': {
                'term': {
                    '@type': 'Term',
                    '@id': 'ureaKgN',
                    'termType': 'inorganicFertiliser',
                    'units': 'kg N'
                },
                'group': 'Nitrogen (kg N)',
                'country': {
                    '@type': 'Term',
                    '@id': 'GADM-GBR'
                },
                'outliers': [113],
                'threshold': 0.95,
                'min': 142.48,
                'max': 189.52
            }
        },
        {
            'level': 'warning',
            'dataPath': '.inputs[1].value',
            'message': 'is outside confidence interval',
            'params': {
                'term': {
                    '@type': 'Term',
                    '@id': 'ammoniumSulphateKgN',
                    'termType': 'inorganicFertiliser',
                    'units': 'kg N'
                },
                'group': 'Nitrogen (kg N)',
                'country': {
                    '@type': 'Term',
                    '@id': 'GADM-GBR'
                },
                'outliers': [113],
                'threshold': 0.95,
                'min': 142.48,
                'max': 189.52
            }
        },
        {
            'level': 'warning',
            'dataPath': '.inputs[2].value',
            'message': 'is outside confidence interval',
            'params': {
                'term': {
                    '@type': 'Term',
                    '@id': 'inorganicNitrogenFertiliserUnspecifiedKgN',
                    'termType': 'inorganicFertiliser',
                    'units': 'kg N'
                },
                'group': 'Nitrogen (kg N)',
                'country': {
                    '@type': 'Term',
                    '@id': 'GADM-GBR'
                },
                'outliers': [113],
                'threshold': 0.95,
                'min': 142.48,
                'max': 189.52
            }
        },
        {
            'level': 'warning',
            'dataPath': '.inputs[3].value',
            'message': 'is outside confidence interval',
            'params': {
                'term': {
                    '@type': 'Term',
                    '@id': 'inorganicPotassiumFertiliserUnspecifiedKgK2O',
                    'termType': 'inorganicFertiliser',
                    'units': 'kg K2O'
                },
                'group': 'Potassium (kg K2O)',
                'country': {
                    '@type': 'Term',
                    '@id': 'GADM-GBR'
                },
                'outliers': [217],
                'threshold': 0.95,
                'min': 68.32,
                'max': 99.68
            }
        },
        {
            'level': 'warning',
            'dataPath': '.inputs[4].value',
            'message': 'is outside confidence interval',
            'params': {
                'term': {
                    '@type': 'Term',
                    '@id': 'inorganicPhosphorusFertiliserUnspecifiedKgP2O5',
                    'termType': 'inorganicFertiliser',
                    'units': 'kg P2O5'
                },
                'group': 'Phosphorus (kg P2O5)',
                'country': {
                    '@type': 'Term',
                    '@id': 'GADM-GBR'
                },
                'outliers': [183],
                'threshold': 0.95,
                'min': 36.16,
                'max': 51.84
            }
        }
    ]


@patch(f"{class_path}.get_post", side_effect=fake_get_post)
def test_validate_fertiliser_value_complete_valid(*args):
    with open(f"{fixtures_path}/input/fertiliser/complete/valid.json") as f:
        cycle = json.load(f)
    assert validate_fertiliser_value(cycle, cycle.get('site')) is True


@patch(f"{class_path}.get_prior", side_effect=fake_get_post)
@patch(f"{class_path}.get_post", return_value=(None, None))
def test_validate_fertiliser_value_complete_valid_with_prior_no_posterior(*args):
    with open(f"{fixtures_path}/input/fertiliser/complete/valid.json") as f:
        cycle = json.load(f)
    assert validate_fertiliser_value(cycle, cycle.get('site')) is True


@patch(f"{class_path}.get_prior", return_value=(None, None))
@patch(f"{class_path}.get_post", return_value=(None, None))
def test_validate_fertiliser_value_complete_valid_no_prior_no_posterior(*args):
    with open(f"{fixtures_path}/input/fertiliser/complete/valid.json") as f:
        cycle = json.load(f)
    assert validate_fertiliser_value(cycle, cycle.get('site')) is True


@patch(f"{class_path}.get_post", return_value=Exception)
def test_validate_fertiliser_value_handle_exception(*args):
    with open(f"{fixtures_path}/input/fertiliser/complete/valid.json") as f:
        cycle = json.load(f)
    assert validate_fertiliser_value(cycle, cycle.get('site')) is True


def test_validate_animalFeed_requires_isAnimalFeed_valid():
    # no inputs should be valid
    assert validate_animalFeed_requires_isAnimalFeed({}, {}) is True

    with open(f"{fixtures_path}/input/animalFeed-fate/valid.json") as f:
        cycle = json.load(f)
    assert validate_animalFeed_requires_isAnimalFeed(cycle, cycle.get('site'), 'inputs') is True


def test_validate_animalFeed_requires_isAnimalFeed_invalid():
    with open(f"{fixtures_path}/input/animalFeed-fate/invalid.json") as f:
        cycle = json.load(f)
    assert validate_animalFeed_requires_isAnimalFeed(cycle, cycle.get('site'), 'inputs') == {
        'level': 'error',
        'dataPath': '.inputs[0].isAnimalFeed',
        'message': 'must specify is it an animal feed'
    }
