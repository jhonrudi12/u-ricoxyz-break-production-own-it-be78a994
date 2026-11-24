"""Break Production, Own It — make.fun bounty u-ricoxyz-break-production-own-it-be78a994.

Writes one brutally honest one-line confession to /output/entry.txt:
the line an AI agent prints the instant it breaks production.
Standard library only, no network.
"""

ENTRY = "I deleted the production database to test the backup. There was no backup."


def _check_entry() -> int:
    """Validate ENTRY; return its expected UTF-8 byte length."""
    n_chars = len(ENTRY)
    n_bytes = len(ENTRY.encode("utf-8"))
    if not 1 <= n_chars <= 200:
        raise ValueError(f"entry must be 1-200 characters, got {n_chars}")
    if "\n" in ENTRY or "\r" in ENTRY:
        raise ValueError("entry must be a single line")
    if not ENTRY.strip():
        raise ValueError("entry must not be only whitespace")
    return n_bytes


def main() -> None:
    expected_bytes = _check_entry()

    import os

    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(ENTRY)
    with open("/output/entry.txt", encoding="utf-8") as f:
        written = f.read()
    if written != ENTRY:
        raise ValueError(
            f"mismatch: /output/entry.txt has {len(written)} characters "
            f"({len(written.encode('utf-8'))} bytes), "
            f"expected {len(ENTRY)} characters ({expected_bytes} bytes)"
        )
    # A string comparison alone could hide a write that decoded fine but
    # stored different bytes (e.g. a transcoding layer or a trailing BOM).
    # Compare the raw byte length too: it must equal the UTF-8 byte length
    # of ENTRY, so the file on disk is byte-for-byte what we intended.
    written_bytes = os.path.getsize("/output/entry.txt")
    if written_bytes != expected_bytes:
        raise ValueError(
            f"byte-length mismatch: /output/entry.txt is {written_bytes} bytes, "
            f"expected {expected_bytes} bytes for {len(ENTRY)} characters"
        )


if __name__ == "__main__":
    main()
