import qrcode
import argparse
import sys
import pathlib


def generate_qr_code(
    data,
    output_file: str = "qrcode.png",
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
):
    """
    Generates a QR code based on the provided parameters and saves it as an image file.

    :param data: The data to encode in the QR code
    :param output_file: The name of the output image file
    :param version: The version of the QR code (between 1 and 40)
    :param error_correction: The error correction level (L, M, Q, H)
    :param box_size: The size of each box in the QR code in pixels
    :param border: The size of the border in boxes
    """
    qr = qrcode.QRCode(
        version=version,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    img.save(output_file)


def validate_args(args, error_correction_levels):
    """
    Validates and handles command-line arguments.

    :param args: The parsed command-line arguments
    :param error_correction_levels: The dictionary of error correction levels
    :return: None
    """
    if args.data is None:
        print("Error: Data to encode is required")
        return False

    if args.version < 1 or args.version > 40:
        print("Error: Version must be between 1 and 40")
        return False

    args.error_correction = args.error_correction.upper()

    if args.error_correction not in error_correction_levels:
        print("Error: Invalid error correction level. Choose from L, M, Q, or H")
        return False

    args.error_correction = error_correction_levels[args.error_correction]

    if args.box_size < 1:
        print("Error: Box size must be greater than 0")
        return False

    if args.border < 1:
        print("Error: Border must be greater than 0")
        return False

    output_file_path = pathlib.Path(args.output_file)
    if output_file_path.suffix.lower() not in [".png", ".jpg", ".jpeg"]:
        print("Error: Output file must be in PNG or JPG format")
        return False

    return True


def main():
    """
    Main function to parse command-line arguments and generate a QR code based on the provided
    input parameters.
    """
    parser = argparse.ArgumentParser(description="Generate QR codes.")

    parser.add_argument(
        "-v", "--version", type=int, default=1, help="QR code version | V1-V40"
    )

    parser.add_argument(
        "-e",
        "--error_correction",
        type=str,
        default="H",
        help="Error correction level | L, M, Q, H",
    )

    parser.add_argument(
        "-bs", "--box_size", type=int, default=10, help="Box size in pixels"
    )

    parser.add_argument("-b", "--border", type=int, default=4, help="Border in boxes")

    parser.add_argument(
        "-o", "--output_file", type=str, default="qrcode.png", help="Output file name"
    )

    parser.add_argument("-d", "--data", type=str, help="Data to encode")

    args = parser.parse_args()

    error_correction_levels = {
        "L": qrcode.constants.ERROR_CORRECT_L,
        "M": qrcode.constants.ERROR_CORRECT_M,
        "Q": qrcode.constants.ERROR_CORRECT_Q,
        "H": qrcode.constants.ERROR_CORRECT_H,
    }

    if not validate_args(args, error_correction_levels):
        parser.print_help()
        sys.exit(1)

    try:
        generate_qr_code(
            args.data.encode("utf-8"),
            args.output_file,
            args.version,
            args.error_correction,
            args.box_size,
            args.border,
        )
        print(f"QR code successfully generated and saved as {args.output_file}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
