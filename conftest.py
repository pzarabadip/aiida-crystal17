"""Initialise a text database and profile."""
import os
import shutil
import tempfile

import pytest

from aiida.manage.fixtures import fixture_manager

from aiida_crystal17.tests import (get_resource_path, get_test_structure, get_test_structure_and_symm,
                                   open_resource_binary)
from aiida_crystal17.tests.utils import AiidaTestApp


@pytest.fixture(scope='session')
def aiida_environment():
    """Set up a test profile for the duration of the tests."""
    # TODO this is required locally for click
    # (see https://click.palletsprojects.com/en/7.x/python3/)
    os.environ['LC_ALL'] = 'en_US.UTF-8'
    with fixture_manager() as fixture_mgr:
        yield fixture_mgr


@pytest.fixture(scope='function')
def db_test_app(aiida_environment):
    """Clear the database after each test."""
    if os.environ.get('MOCK_CRY17_EXECUTABLES', True) != 'false':
        print('NB: using mock executable')
        executables = {
            'crystal17.basic': 'mock_crystal17',
            'crystal17.main': 'mock_crystal17',
            'crystal17.doss': 'mock_properties17',
            'crystal17.fermi': 'mock_properties17',
            'gulp.single': 'mock_gulp',
            'gulp.optimize': 'mock_gulp',
            'gulp.fitting': 'mock_gulp'
        }
    else:
        executables = {
            'crystal17.basic': 'crystal17',
            'crystal17.main': 'crystal17',
            'crystal17.doss': 'properties17',
            'crystal17.fermi': 'properties17',
            'gulp.single': 'gulp',
            'gulp.optimize': 'gulp',
            'gulp.fitting': 'gulp'
        }

    test_workdir = os.environ.get('CRY17_TEST_WORKDIR', None)
    if test_workdir:
        print('NB: using test workdir: {}'.format(test_workdir))
        work_directory = test_workdir
    else:
        work_directory = tempfile.mkdtemp()
    yield AiidaTestApp(work_directory, executables, environment=aiida_environment)
    aiida_environment.reset_db()
    if not test_workdir:
        shutil.rmtree(work_directory)


@pytest.fixture(scope='function')
def get_structure():
    return get_test_structure


@pytest.fixture(scope='function')
def get_structure_and_symm():
    return get_test_structure_and_symm


@pytest.fixture(scope='function')
def get_cif():

    def _get_cif(name):
        from aiida.orm import CifData
        if name == 'pyrite':
            with open_resource_binary('cif', 'pyrite.cif') as handle:
                return CifData(file=handle)
        raise ValueError(name)

    return _get_cif


@pytest.fixture(scope='function')
def upload_basis_set_family():
    """Upload a basis set family."""
    from aiida_crystal17.data.basis_set import BasisSetData

    def _upload(folder_name='sto3g', group_name='sto3g', stop_if_existing=True):
        BasisSetData.upload_basisset_family(get_resource_path('basis_sets', folder_name),
                                            group_name,
                                            'minimal basis sets',
                                            stop_if_existing=stop_if_existing,
                                            extension='.basis')
        return BasisSetData.get_basis_group_map(group_name)

    return _upload
