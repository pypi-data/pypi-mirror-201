import pytest

from wunderkafka.structures import SRMeta
from wunderkafka.serdes.avro.headers import ConfluentClouderaHeadersHandler

parse = ConfluentClouderaHeadersHandler().parse
pack = ConfluentClouderaHeadersHandler().pack

BAD_HEADERS = (
    b'\x00',
    b'\x00\x00\x00=',
    b'\x08\xf2',
)


@pytest.mark.parametrize("bad_header", list(BAD_HEADERS))
def test_short_message(bad_header) -> None:
    with pytest.raises(RuntimeError):
        parse(bad_header)


# ToDo (tribunsky.kir): bring to common exceptions.
def test_unknown_protocol() -> None:
    with pytest.raises(RuntimeError):
        parse(b'\x05\x00\x00\x00=')
    with pytest.raises(ValueError):
        pack(5, meta=SRMeta(1, 1, 1))


def test_handle_hw_int() -> None:
    hdr = parse(b'\x03\x00\x00\x00=')
    assert hdr.protocol_id == 3
    assert hdr.schema_id == 61


def test_handle_hw_int2():
    serialized = b'\x03\x00\x00\x034'
    hdr = parse(serialized)
    assert hdr.protocol_id == 3
    assert hdr.schema_id == 820
    packed = pack(hdr.protocol_id, meta=SRMeta(hdr.schema_id, hdr.schema_version, hdr.meta_id))
    assert packed == serialized


def test_handle_hw_meta():
    hdr = parse(b'\x01\x00\x00\x00\x00\x00\x00\x00 \x00\x00\x00\x01')
    assert hdr.protocol_id == 1
    assert hdr.meta_id == 32
    assert hdr.schema_version == 1


def test_handle_hw_meta2():
    serialized = b'\x01\x00\x00\x00\x00\x00\x00\x01\xa8\x00\x00\x00\x01'
    hdr = parse(serialized)
    assert hdr.protocol_id == 1
    assert hdr.meta_id == 424
    assert hdr.schema_version == 1
    packed = pack(hdr.protocol_id, meta=SRMeta(hdr.schema_id, hdr.schema_version, hdr.meta_id))
    assert packed == serialized

    with pytest.raises(ValueError):
        pack(hdr.protocol_id, meta=SRMeta(hdr.schema_id, hdr.schema_version, None))
