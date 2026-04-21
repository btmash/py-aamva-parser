from aamva_parser.field_mapping import FieldMapper


def test_field_mapper_state() -> None:
    field_mapper = FieldMapper()
    assert field_mapper.field_for("state") == "DAJ"
