from flask import Flask, render_template, request, redirect, url_for, send_file
from PIL import Image
from rembg import remove
import io

app = Flask(__name__)

# Función para procesar la imagen eliminando el fondo
def process_image(image_uploaded):
    image = Image.open(image_uploaded)
    processed_image = remove_background(image)
    return processed_image

# Función para eliminar el fondo de la imagen
def remove_background(image):
    image_byte = io.BytesIO()
    image.save(image_byte, format='PNG')
    image_byte.seek(0)
    processed_image_bytes = remove(image_byte.read())
    return Image.open(io.BytesIO(processed_image_bytes))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Obtener el archivo subido por el usuario
        uploaded_image = request.files["image"]

        if uploaded_image:
            # Procesar la imagen para eliminar el fondo
            processed_image = process_image(uploaded_image)
            
            # Guardar la imagen procesada en un archivo temporal
            processed_image_path = "processed_image.png"
            processed_image.save(processed_image_path)

            # Redirigir a la ruta de descarga
            return redirect(url_for("download_image"))

    return render_template("index.html")

@app.route("/download")
def download_image():
    # Descargar la imagen procesada
    return send_file("processed_image.png", as_attachment=True, download_name="processed_image.png")

if __name__ == "__main__":
    app.run(debug=True)

