from flask import Flask, render_template, request, redirect, url_for, send_file
from PIL import Image
from rembg import remove
import io

app = Flask(__name__)

def process_image(image_uploaded):
    image = Image.open(image_uploaded)
    processed_image = remove_background(image)
    return processed_image

def remove_background(image):
    image_byte = io.BytesIO()
    image.save(image_byte, format='PNG')
    image_byte.seek(0)
    processed_image_bytes = remove(image_byte.read())
    return Image.open(io.BytesIO(processed_image_bytes))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded_image = request.files["image"]

        if uploaded_image:
            processed_image = process_image(uploaded_image)
            
            processed_image_path = "processed_image.png"
            processed_image.save(processed_image_path)

            return redirect(url_for("download_image"))

    return render_template("index.html")

@app.route("/download")
def download_image():
    return send_file("processed_image.png", as_attachment=True, download_name="processed_image.png")

if __name__ == "__main__":
    app.run(debug=True)

