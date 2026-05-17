from flask import Flask, render_template, request, send_file, jsonify
import qrcode
import qrcode.image.svg
import io
import base64
from PIL import Image

app = Flask(__name__)


def generate_qr(
    text,
    fill_color="#000000",
    back_color="#ffffff",
    box_size=10,
    border=4,
    error_correction="M",
    output_format="PNG",
):
    ec_map = {
        "L": qrcode.constants.ERROR_CORRECT_L,
        "M": qrcode.constants.ERROR_CORRECT_M,
        "Q": qrcode.constants.ERROR_CORRECT_Q,
        "H": qrcode.constants.ERROR_CORRECT_H,
    }

    qr = qrcode.QRCode(
        version=None,  # auto-size
        error_correction=ec_map.get(error_correction, qrcode.constants.ERROR_CORRECT_M),
        box_size=box_size,
        border=border,
    )
    qr.add_data(text)
    qr.make(fit=True)

    if output_format == "SVG":
        factory = qrcode.image.svg.SvgImage
        img = qr.make_image(image_factory=factory)
        buf = io.BytesIO()
        img.save(buf)
        buf.seek(0)
        return buf.read().decode("utf-8"), "svg+xml"

    img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGBA")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf.read(), "png"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400

    fill_color = data.get("fill_color", "#000000")
    back_color = data.get("back_color", "#ffffff")
    box_size = int(data.get("box_size", 10))
    border = int(data.get("border", 4))
    error_correction = data.get("error_correction", "M")
    output_format = data.get("format", "PNG")

    try:
        result, mime_type = generate_qr(
            text, fill_color, back_color, box_size, border, error_correction, output_format
        )
        if output_format == "SVG":
            return jsonify({"image": result, "format": "svg"})
        else:
            b64 = base64.b64encode(result).decode("utf-8")
            return jsonify({"image": b64, "format": "png"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/download", methods=["POST"])
def download():
    data = request.json
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400

    fill_color = data.get("fill_color", "#000000")
    back_color = data.get("back_color", "#ffffff")
    box_size = int(data.get("box_size", 10))
    border = int(data.get("border", 4))
    error_correction = data.get("error_correction", "M")
    output_format = data.get("format", "PNG")

    result, mime_type = generate_qr(
        text, fill_color, back_color, box_size, border, error_correction, output_format
    )

    if output_format == "SVG":
        buf = io.BytesIO(result.encode("utf-8"))
        return send_file(buf, mimetype="image/svg+xml", as_attachment=True, download_name="qrcode.svg")
    else:
        buf = io.BytesIO(result)
        return send_file(buf, mimetype="image/png", as_attachment=True, download_name="qrcode.png")


if __name__ == "__main__":
    app.run(debug=True)