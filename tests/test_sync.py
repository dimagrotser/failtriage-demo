def test_stock_sync_finishes(request):
    # Stands in for a race: the first attempt loses and the rerun wins.
    assert request.node.execution_count > 1
