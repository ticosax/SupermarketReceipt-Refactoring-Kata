def test_fake_catalog(catalog, cloves_the_spice, cloves_the_hardware):
    """despite products share the same name, the catalog sees 2 distinct products"""
    assert len(catalog.prices) == 2
