from ibata.utils.Helper import Helper


def test_append_values_if_not_none():
    data = []
    values = ["neco", "", None, None, "neco1"]
    assert ["neco", "", "neco1"] == Helper.append_values_if_not_none(data, values)
    assert ["neco", "", "neco1", "neco", "", "neco1"] == Helper.append_values_if_not_none(data, values)


def test_none_to_empty():
    assert "None" == Helper.none_to_empty("None")
    assert "" == Helper.none_to_empty("")
    assert "" == Helper.none_to_empty(None)
