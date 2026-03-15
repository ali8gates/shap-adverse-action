from shap_aa.backfill import BackfillRecord, compare_backfill


def test_identical_batches_fully_match():
    live = [BackfillRecord("APP-1", {"x": 1.0}, 0.5, ["low_account_tenure"])]
    backfilled = [BackfillRecord("APP-1", {"x": 1.0}, 0.5, ["low_account_tenure"])]
    report = compare_backfill(live, backfilled)
    assert report.fully_matched
    assert report.match_rate == 1.0


def test_score_drift_is_caught():
    live = [BackfillRecord("APP-1", {"x": 1.0}, 0.5, ["low_account_tenure"])]
    backfilled = [BackfillRecord("APP-1", {"x": 1.0}, 0.62, ["low_account_tenure"])]
    report = compare_backfill(live, backfilled)
    assert not report.fully_matched
    assert any("model score differs" in m for m in report.mismatches)


def test_missing_backfill_record_is_reported():
    live = [BackfillRecord("APP-1", {"x": 1.0}, 0.5, [])]
    backfilled = []
    report = compare_backfill(live, backfilled)
    assert not report.fully_matched
    assert "no matching backfill record" in report.mismatches[0]
