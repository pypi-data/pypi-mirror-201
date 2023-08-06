import json
import pathlib
import tempfile

import pytest
import requests_mock

from rebotics_sdk.advanced.packers import ClassificationDatabasePacker, ZipDatabasePacker, \
    DuplicateFeatureVectorsException, VirtualClassificationDatabasePacker
from rebotics_sdk.providers import FVMProvider


@pytest.fixture(scope="module")
def script_cwd(request):
    return request.fspath.join("..")


def test_classification_packing(script_cwd):
    db_folder = pathlib.Path(script_cwd.join("db"))
    with tempfile.TemporaryDirectory() as dirname:
        destination_filename = pathlib.Path(dirname, 'test')
        packer = ClassificationDatabasePacker(destination=destination_filename)
        features = db_folder / 'features.txt'
        labels = db_folder / 'labels.txt'
        images_folder = db_folder / 'custom_folder/'

        res = packer.pack(labels, features, images_folder)

        assert 'test.rcdb' in res

        with packer.zipfile(res, mode='r') as zip_io:
            meta = json.loads(packer.read_lines(zip_io.read('meta.json').decode('utf-8'))[0])

        expected_keys = [
            'packed',
            'model_type',
            'model_codename',
            'sdk_version',
            'packer_version',
            'core_version',
            'fvm_version'
        ]
        for key in expected_keys:
            assert key in meta.keys()

        assert len(packer.images) == 2

        packer = ClassificationDatabasePacker(source=res)
        entries = list(packer.unpack())
        assert len(entries) == 2
        entry = entries[0]
        assert entry.label == '123123123'
        assert entry.feature == '123123123123123'
        internal_filename = entry.filename
        assert internal_filename == 'image_1.png'

        for key in expected_keys:
            assert key in packer.meta_data.keys()

        # testing if it can be dumped to the FS
        og_file = images_folder / internal_filename
        tmp_file = db_folder / internal_filename

        with open(tmp_file, 'wb') as fout:
            fout.write(entry.image)

        assert og_file.stat().st_size == tmp_file.stat().st_size
        tmp_file.unlink()


def test_classification_packing_check_duplicates(script_cwd):
    db_folder = pathlib.Path(script_cwd.join("db"))
    packer = ClassificationDatabasePacker(destination='test', check_duplicates=True)
    features = db_folder / 'features.txt'
    labels = db_folder / 'labels.txt'
    images_folder = db_folder / 'custom_folder/'

    with pytest.raises(DuplicateFeatureVectorsException) as excinfo:
        packer.pack(labels, features, images_folder)
    assert "duplicate" in str(excinfo.value)


def test_zip_packing():
    packer = ZipDatabasePacker()
    packed = packer.pack(
        labels=[
            '123123123'
        ],
        features=[
            '123123123123123'
        ]
    )
    assert packer.meta_data['count'] == 1

    unpacker = ZipDatabasePacker(source=packed)
    for entry in unpacker.unpack():
        assert entry.label == '123123123'
        assert entry.feature == '123123123123123'

    assert unpacker.meta_data['count'] == 1


def test_virtual_packing_and_unpacking(script_cwd):
    db_folder = pathlib.Path(script_cwd.join("db"))

    with tempfile.TemporaryDirectory() as dirname, requests_mock.Mocker() as m:
        m.get('https://via.placeholder.com/150', text='some file')
        destination_filename = pathlib.Path(dirname, 'test')
        # destination_filename = db_folder / "test.rcdb"
        provider = FVMProvider(host='https://r3dev-fvm.rebotics.net/')
        packer = VirtualClassificationDatabasePacker(
            destination=destination_filename,
            provider=provider,
        )

        features = db_folder / 'features.txt'
        labels = db_folder / 'labels.txt'
        images = db_folder / 'image_urls.txt'
        uuids = db_folder / 'uuid.txt'

        res = packer.pack(
            labels, features, uuids, images
        )
        assert 'test.rcdb' in res, "Same destination is returned properly and extension is set normally"

        unpacker = VirtualClassificationDatabasePacker(
            source=pathlib.Path(dirname, 'test.rcdb'),
            with_images=True,
            provider=provider,
        )
        data = list(unpacker.unpack())
        assert len(data) == 2, "There are only two entries along the way"
