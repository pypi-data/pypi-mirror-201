"""Test module v1_calculate"""
from pathlib import Path

import pytest

from astropy.table import Table
from astropy.time import Time
import numpy as np

from stdatamodels.jwst.datamodels import ImageModel

from jwst.lib import engdb_mast
from jwst.lib import engdb_tools
import jwst.lib.set_telescope_pointing as stp
import jwst.lib.v1_calculate as v1c

from jwst.lib.tests.engdb_mock import EngDB_Mocker

# Requires pysiaf
pytest.importorskip('pysiaf')

DATA_PATH = Path(__file__).parent / 'data'

# Engineering parameters
# Time range corresponds to OTE-1 exposure jw01134001037_03107_00001_nrcb1_uncal.fits
# Midpoint is about 2022-02-02T22:25:00
MAST_GOOD_STARTTIME = Time('59612.93401553055', format='mjd')
MAST_GOOD_ENDTIME = Time('59612.93500967592', format='mjd')

# Time range for the mock database
MOCK_GOOD_STARTTIME = Time('59240.10349754328', format='mjd')
MOCK_GOOD_ENDTIME = Time('59240.1082197338', format='mjd')


@pytest.fixture
def engdb_service():
    """Setup the service to operate through the mock service"""
    with EngDB_Mocker():
        yield engdb_tools.ENGDB_Service(base_url='http://localhost')


def test_from_models(engdb_service, tmp_path):
    """Test v1_calculate_from_models for basic running"""
    model = ImageModel()
    model.meta.exposure.start_time = MOCK_GOOD_STARTTIME.mjd
    model.meta.exposure.end_time = MOCK_GOOD_ENDTIME.mjd

    v1_table = v1c.v1_calculate_from_models([model], method=stp.Methods.COARSE_TR_202111, engdb_url=engdb_service.base_url)
    v1_formatted = v1c.simplify_table(v1_table)

    # Save for post-test examination
    v1_formatted.write(tmp_path / 'test_from_models_service.ecsv', format='ascii.ecsv')

    truth = Table.read(DATA_PATH / 'test_from_models_service.ecsv')
    errors = v1_compare_simplified_tables(v1_formatted, truth)
    errors_str = '\n'.join(errors)
    assert len(errors) == 0, f'V1 tables are different: {errors_str}'


def test_over_time(engdb_service, tmp_path):
    """Test v1_calculate_over_time for basic running"""
    v1_table = v1c.v1_calculate_over_time(MOCK_GOOD_STARTTIME.mjd, MOCK_GOOD_ENDTIME.mjd,
                                          method=stp.Methods.COARSE_TR_202111,
                                          engdb_url=engdb_service.base_url)
    v1_formatted = v1c.simplify_table(v1_table)

    # Save for post-test examination
    v1_formatted.write(tmp_path / 'test_over_time_service.ecsv', format='ascii.ecsv')

    truth = Table.read(DATA_PATH / 'test_over_time_service.ecsv')
    errors = v1_compare_simplified_tables(v1_formatted, truth)
    errors_str = '\n'.join(errors)
    assert len(errors) == 0, f'V1 tables are different: {errors_str}'


def test_from_models_mast(tmp_path):
    """Test v1_calculate_from_models for basic running"""
    model = ImageModel()
    model.meta.exposure.start_time = MAST_GOOD_STARTTIME.mjd
    model.meta.exposure.end_time = MAST_GOOD_ENDTIME.mjd

    try:
        v1_table = v1c.v1_calculate_from_models([model], method=stp.Methods.COARSE_TR_202111, engdb_url=engdb_mast.MAST_BASE_URL)
    except ValueError as exception:
        pytest.xfail(f'MAST engineering database not available, possibly no token specified: {exception}')
    v1_formatted = v1c.simplify_table(v1_table)

    # Save for post-test examination
    v1_formatted.write(tmp_path / 'test_from_models_mast.ecsv', format='ascii.ecsv')

    truth = Table.read(DATA_PATH / 'test_from_models_mast.ecsv')
    errors = v1_compare_simplified_tables(v1_formatted, truth)
    errors_str = '\n'.join(errors)
    assert len(errors) == 0, f'V1 tables are different: {errors_str}'


def test_over_time_mast(tmp_path):
    """Test v1_calculate_over_time for basic running"""
    try:
        v1_table = v1c.v1_calculate_over_time(MAST_GOOD_STARTTIME.mjd, MAST_GOOD_ENDTIME.mjd,
                                              method=stp.Methods.COARSE_TR_202111, engdb_url=engdb_mast.MAST_BASE_URL)
    except ValueError as exception:
        pytest.xfail(f'MAST engineering database not available, possibly no token specified: {exception}')
    v1_formatted = v1c.simplify_table(v1_table)

    # Save for post-test examination
    v1_formatted.write(tmp_path / 'test_over_time_mast.ecsv', format='ascii.ecsv')

    truth = Table.read(DATA_PATH / 'test_over_time_mast.ecsv')
    errors = v1_compare_simplified_tables(v1_formatted, truth)
    errors_str = '\n'.join(errors)
    assert len(errors) == 0, f'V1 tables are different: {errors_str}'


def v1_compare_simplified_tables(a, b, rtol=1e-05):
    """Calculate diff between tables generated by v1_calculate
    """
    errors = []
    if len(a) != len(b):
        errors.append(f'len(a)={len(a)} not equal to len(b)={len(b)}')

    if not all(a['obstime'] == b['obstime']):
        errors.append('obstimes different')

    if not np.allclose(a['ra'], b['ra'], rtol=rtol):
        errors.append('RAs are different')

    if not np.allclose(a['dec'], b['dec'], rtol=rtol):
        errors.append('DECs are different')

    if not np.allclose(a['pa_v3'], b['pa_v3'], rtol=rtol):
        errors.append('PA_V3s are different')

    return errors
