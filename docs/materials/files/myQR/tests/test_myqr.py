from typing import Any
from pathlib import Path

from myqr import file_ops
from myqr import myqr_streamlit as qr_app


class DummyImage:
    def save(self, file_path: str) -> None:
        """Write placeholder image bytes to disk for test assertions."""
        Path(file_path).write_bytes(b"png-bytes")
# End of DummyImage()

class DummyQR:
    def make_image(self, fill_color: str, back_color: str) -> DummyImage:
        """Return a dummy image object that mimics qrcode output."""
        return DummyImage()
# End of DummyQR()

def test_check_data_dir_creates_then_detects_existing(tmp_path: Path) -> None:
    """Create output directory once, then confirm second call reports existing."""
    out_dir = tmp_path / "0_out"

    created = file_ops.check_data_dir(str(out_dir))
    existed = file_ops.check_data_dir(str(out_dir))

    assert created is True
    assert existed is False
    assert out_dir.exists()
# End of test_check_data_dir_creates_then_detects_existing()

def test_save_with_unique_filename_adds_counter(tmp_path: Path) -> None:
    """Verify filename collision appends _01 suffix."""
    first = tmp_path / "myQRCode.png"
    first.write_text("exists", encoding="utf-8")

    next_name = file_ops.save_with_unique_filename(str(first))

    assert next_name.endswith("myQRCode_01.png")
# End of test_save_with_unique_filename_adds_counter()

def test_save_file_writes_image_and_reports_success(tmp_path: Path, monkeypatch: Any) -> None:
    """Ensure save_file writes PNG and emits a success message."""
    out_dir = tmp_path / "0_out"
    monkeypatch.setattr(qr_app, "OUTPUTDIR", f"{out_dir}/")

    messages = []
    monkeypatch.setattr(qr_app.st, "success", lambda msg: messages.append(("success", msg)))
    monkeypatch.setattr(qr_app.st, "error", lambda msg: messages.append(("error", msg)))

    saved_path = qr_app.save_file("#000000", "#ffffff", "qr.png", DummyQR())

    assert Path(saved_path).exists()
    assert messages
    assert messages[0][0] == "success"
# End of test_save_file_writes_image_and_reports_success()