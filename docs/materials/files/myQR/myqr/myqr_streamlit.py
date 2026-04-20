import os
from typing import Any

from PIL import Image
import qrcode
import streamlit as st

from myqr import file_ops as fo


OUTPUTDIR = "0_out/"


def generate_qrcode(
    data: str,
    color: str,
    bgcolor: str,
    box_size: int,
    border: int,
    fname: str,
) -> None:
    """Generate and display a QR code image."""
    qr = qrcode.QRCode(version=1, box_size=box_size, border=border)
    qr.add_data(data)
    qr.make(fit=True)

    saved_file = save_file(bgcolor, color, fname, qr)

    if saved_file is not None:
        image = Image.open(saved_file)
        st.image(image, caption="Uploaded PNG", use_container_width=True)
# End of generate_qrcode()


def save_file(bgcolor: str, color: str, fname: str, qr: Any) -> str:
    """Save QR image to a unique filename in OUTPUTDIR."""
    img = qr.make_image(fill_color=color, back_color=bgcolor)

    fo.check_data_dir(OUTPUTDIR)
    fname = OUTPUTDIR + fname
    fname = fo.save_with_unique_filename(fname)

    if os.path.exists(fname):
        st.error(
            f"Attention: The file, {fname}, already exists! Please change the filename above."
        )
    else:
        img.save(fname)
        st.success(f"Saved file as {fname}")

    return fname
# End of save_file()


def app() -> None:
    """Streamlit main app function."""
    st.title("Hey! It's MyQR: An Interactive QR Code Generator!")
    st.write("Generate QR codes with customizable styles!")

    data = st.text_input(
        "Enter the data for the QR Code:", "https://www.oliverbonhamcarter.com"
    )

    suggested_file_name = "myQRCode.png"
    fname = st.text_input("Enter the filename to save the QRcode", suggested_file_name)

    color = st.color_picker("Select QR Code color", "#23dda0")
    bgcolor = st.color_picker("Select Background color", "#0E228E")
    box_size = st.slider("Select Box Size", min_value=1, max_value=20, value=10)
    border = st.slider("Select Border Size", min_value=1, max_value=10, value=4)

    if st.button("Generate QR Code"):
        if data:
            generate_qrcode(data, color, bgcolor, box_size, border, fname)
        else:
            st.warning("Please enter some data to generate the QR code!")

# End of app()

if __name__ == "__main__":
    app()