from toolbox.views import View


def test_output_data_when_property_is_read():
    v = View()

    got = v.data

    assert got == []  # nosec
