"""Independent synthetic controls for the SHINE Table 2 locator."""

import importlib.util
from pathlib import Path

import pytest


def module():
    spec = importlib.util.spec_from_file_location(
        "shine_table", Path(__file__).resolve().parents[2] / "scripts/qualify_shine_table.py"
    )
    assert spec
    assert spec.loader
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


HEADER = "Retail outlet restriction to about 300 outlets (about5%of current outlets)"
TRANSITION = "CS→FSFVCS→FSCVDU→FSFVDU→FSCV"
TEXT = (
    "Placing the mean at 19.4% and using SD=3.6%, we parameterised the "
    "one-off increase in smoking net cessation as X=beta (23.4, 97.2), "
    "median 19.2%, 95% UI: 12.9% to 26.9%."
)


def html(*, section="T2", heading=HEADER, transition=TRANSITION, text=TEXT):
    return (
        "<html><head><title>Tobacco endgame intervention impacts</title>"
        '<meta name="doi" content="10.1136/tc-2022-057655"></head>'
        f'<body><section id="{section}"><table><tbody>'
        f'<tr><td colspan="2">{heading}</td></tr>'
        "<tr><td>NS→CS</td><td>beta (23.4, 97.2) refers to initiation.</td></tr>"
        f"<tr><td>{transition}</td><td>{text}</td></tr>"
        "</tbody></table></section></body></html>"
    ).encode()


def test_retail_cessation_row_and_location_are_preserved() -> None:
    result = module().extract_table(html())
    assert result["source_beta"] == ["23.4", "97.2"]
    assert result["mean_percent"] == "19.4"
    assert result["median_percent"] == "19.2"
    assert result["sd_percentage_points"] == "3.6"
    assert result["ui95_percent"] == ["12.9", "26.9"]
    assert result["locator"]["section"] == "T2"
    assert result["locator"]["cessation_body_row"] == 3


@pytest.mark.parametrize("change", ["section", "heading", "transition", "missing_beta", "duplicate", "mean"])
def test_ambiguous_or_wrong_source_structure_fails_closed(change) -> None:
    kwargs = {}
    if change == "section":
        kwargs["section"] = "T3"
    elif change == "heading":
        kwargs["heading"] = "Different intervention"
    elif change == "transition":
        kwargs["transition"] = "NS→CS"
    elif change == "missing_beta":
        kwargs["text"] = TEXT.replace("X=beta", "X=other")
    elif change == "mean":
        kwargs["text"] = TEXT.replace("19.4%", "19.5%")
    data = html(**kwargs)
    if change == "duplicate":
        data = data.replace(b"</tbody>", f"<tr><td>{TRANSITION}</td><td>{TEXT}</td></tr></tbody>".encode())
    with pytest.raises(ValueError, match="SHINE"):
        module().extract_table(data)