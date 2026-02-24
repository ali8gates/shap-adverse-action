import pytest

from shap_aa.templates import render_reasons, run_quality_gate


def test_known_codes_pass_the_quality_gate():
    result = run_quality_gate(["low_account_tenure", "high_overdraft_frequency"])
    assert result.passed
    assert result.unmapped_codes == []


def test_unmapped_code_fails_the_quality_gate():
    result = run_quality_gate(["low_account_tenure", "made_up_code"])
    assert not result.passed
    assert result.unmapped_codes == ["made_up_code"]


def test_render_reasons_raises_instead_of_sending_a_blank_reason():
    with pytest.raises(ValueError):
        render_reasons(["not_a_real_code"])


def test_render_reasons_returns_every_reason_not_just_the_first():
    codes = ["low_account_tenure", "high_recent_loan_activity", "high_overdraft_frequency", "low_balance_buffer"]
    text = render_reasons(codes)
    assert len(text) == 4
    assert text[0] != text[-1]
