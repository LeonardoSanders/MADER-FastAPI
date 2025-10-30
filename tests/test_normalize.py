from mader_project.functions.normalize_text import normalize_text


def test_normalize_text():
    response = normalize_text('Leonardo Sanders')

    assert response == 'leonardo sanders'
