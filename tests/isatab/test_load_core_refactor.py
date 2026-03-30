from pathlib import Path

import pytest

from isatools.isatab.load.core import ISATabInvestigationLoader, load


def _minimal_investigation_text(identifier: str = "INV-1") -> str:
    return "\n".join(
        [
            "ONTOLOGY SOURCE REFERENCE",
            "Term Source Name\t",
            "Term Source File\t",
            "Term Source Version\t",
            "Term Source Description\t",
            "INVESTIGATION",
            f"Investigation Identifier\t{identifier}",
            "Investigation Title\tTest title",
            "Investigation Description\tTest description",
            "Investigation Submission Date\t",
            "Investigation Public Release Date\t",
            "INVESTIGATION PUBLICATIONS",
            "Investigation PubMed ID\t",
            "Investigation Publication DOI\t",
            "Investigation Publication Author List\t",
            "Investigation Publication Title\t",
            "Investigation Publication Status\t",
            "Investigation Publication Status Term Accession Number\t",
            "Investigation Publication Status Term Source REF\t",
            "INVESTIGATION CONTACTS",
            "Investigation Person Last Name\t",
            "Investigation Person First Name\t",
            "Investigation Person Mid Initials\t",
            "Investigation Person Email\t",
            "Investigation Person Phone\t",
            "Investigation Person Fax\t",
            "Investigation Person Address\t",
            "Investigation Person Affiliation\t",
            "Investigation Person Roles\t",
            "Investigation Person Roles Term Accession Number\t",
            "Investigation Person Roles Term Source REF\t",
            "",
        ]
    )


def _wide_investigation_text(identifier: str = "INV-WIDE", num_comments: int = 140) -> str:
    lines = [
        "ONTOLOGY SOURCE REFERENCE",
        "Term Source Name\t",
        "Term Source File\t",
        "Term Source Version\t",
        "Term Source Description\t",
        "INVESTIGATION",
        f"Investigation Identifier\t{identifier}",
        "Investigation Title\tWide title",
        "Investigation Description\tWide description",
        "Investigation Submission Date\t",
        "Investigation Public Release Date\t",
    ]
    for i in range(num_comments):
        lines.append(f"Comment[c{i}]\tv{i}")
    lines.extend(
        [
            "INVESTIGATION PUBLICATIONS",
            "Investigation PubMed ID\t",
            "Investigation Publication DOI\t",
            "Investigation Publication Author List\t",
            "Investigation Publication Title\t",
            "Investigation Publication Status\t",
            "Investigation Publication Status Term Accession Number\t",
            "Investigation Publication Status Term Source REF\t",
            "INVESTIGATION CONTACTS",
            "Investigation Person Last Name\t",
            "Investigation Person First Name\t",
            "Investigation Person Mid Initials\t",
            "Investigation Person Email\t",
            "Investigation Person Phone\t",
            "Investigation Person Fax\t",
            "Investigation Person Address\t",
            "Investigation Person Affiliation\t",
            "Investigation Person Roles\t",
            "Investigation Person Roles Term Accession Number\t",
            "Investigation Person Roles Term Source REF\t",
            "",
        ]
    )
    return "\n".join(lines)


def test_load_accepts_investigation_file_path(tmp_path: Path):
    inv_path = tmp_path / "i_test.txt"
    inv_path.write_text(_minimal_investigation_text("INV-FILE"), encoding="utf-8")

    investigation = load(str(inv_path))

    assert investigation.identifier == "INV-FILE"


def test_load_directory_requires_single_i_file(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        load(str(tmp_path))

    (tmp_path / "i_one.txt").write_text(_minimal_investigation_text("INV-1"), encoding="utf-8")
    (tmp_path / "i_two.txt").write_text(_minimal_investigation_text("INV-2"), encoding="utf-8")
    with pytest.raises(ValueError):
        load(str(tmp_path))


def test_loader_context_closes_owned_file(tmp_path: Path):
    inv_path = tmp_path / "i_test.txt"
    inv_path.write_text(_minimal_investigation_text("INV-CTX"), encoding="utf-8")

    with ISATabInvestigationLoader(str(inv_path)) as loader:
        assert loader.investigation.identifier == "INV-CTX"
        assert not loader.file.closed

    assert loader.file.closed


def test_load_preserves_wide_investigation_sections(tmp_path: Path):
    inv_path = tmp_path / "i_wide.txt"
    inv_path.write_text(_wide_investigation_text(), encoding="utf-8")

    investigation = load(str(inv_path))

    comment_names = {c.name for c in investigation.comments}
    assert "c139" in comment_names


def test_load_raises_section_order_error(tmp_path: Path):
    bad_inv = "\n".join(
        [
            "INVESTIGATION",
            "Investigation Identifier\tINV-BAD",
            "",
        ]
    )
    inv_path = tmp_path / "i_bad.txt"
    inv_path.write_text(bad_inv, encoding="utf-8")

    with pytest.raises(IOError, match="Invalid ISA-Tab section order"):
        load(str(inv_path))
