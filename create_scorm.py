import os
import shutil
from zipfile import ZipFile
from tkinter import filedialog, messagebox
import tkinter as tk

# Función para crear el imsmanifest.xml
from lxml import etree


def crear_imsmanifest(video_filename, ficha_images, build_folder, pdf_filename, output_folder):
    manifest = etree.Element("manifest", identifier="curso-completo", version="1.0",
                             xmlns="http://www.imsglobal.org/xsd/imscp_v1p1")

    metadata = etree.SubElement(manifest, "metadata")
    etree.SubElement(metadata, "schema").text = "ADL SCORM"
    etree.SubElement(metadata, "schemaversion").text = "1.2"

    organizations = etree.SubElement(manifest, "organizations", default="org_1")
    organization = etree.SubElement(organizations, "organization", identifier="org_1")
    etree.SubElement(organization, "title").text = "Curso Completo: Video, Ficha, Juego y Actividad"

    # Agregar video
    item_video = etree.SubElement(organization, "item", identifier="item_video", identifierref="resource_video")
    etree.SubElement(item_video, "title").text = "Video Explicativo"

    # Agregar ficha
    item_ficha = etree.SubElement(organization, "item", identifier="item_ficha", identifierref="resource_ficha")
    etree.SubElement(item_ficha, "title").text = "Ficha"

    # Agregar juego de Unity
    item_juego = etree.SubElement(organization, "item", identifier="item_juego", identifierref="resource_juego")
    etree.SubElement(item_juego, "title").text = "Juego Interactivo (Unity)"

    # Agregar PDF
    item_pdf = etree.SubElement(organization, "item", identifier="item_pdf", identifierref="resource_pdf")
    etree.SubElement(item_pdf, "title").text = "Actividad PDF para Descargar"

    resources = etree.SubElement(manifest, "resources")

    # Recurso: Video
    resource_video = etree.SubElement(resources, "resource", identifier="resource_video", type="webcontent", href="video.html")
    etree.SubElement(resource_video, "file", href=f"video/{video_filename}")
    etree.SubElement(resource_video, "file", href="video.html")

    # Recurso: Ficha
    resource_ficha = etree.SubElement(resources, "resource", identifier="resource_ficha", type="webcontent", href="ficha.html")
    for image in ficha_images:
        etree.SubElement(resource_ficha, "file", href=f"ficha/{os.path.basename(image)}")
    etree.SubElement(resource_ficha, "file", href="ficha.html")

    # Recurso: Juego Unity
    resource_juego = etree.SubElement(resources, "resource", identifier="resource_juego", type="webcontent", href="index.html")
    for root, dirs, files in os.walk(build_folder):
        for file in files:
            file_path = os.path.relpath(os.path.join(root, file), build_folder)
            etree.SubElement(resource_juego, "file", href=f"Build/{file_path}")

    # Recurso: PDF
    resource_pdf = etree.SubElement(resources, "resource", identifier="resource_pdf", type="webcontent", href="pdf.html")
    etree.SubElement(resource_pdf, "file", href=f"actividad/{os.path.basename(pdf_filename)}")
    etree.SubElement(resource_pdf, "file", href="pdf.html")

    # Guardar imsmanifest.xml
    manifest_tree = etree.ElementTree(manifest)
    manifest_tree.write(os.path.join(output_folder, "imsmanifest.xml"), pretty_print=True, xml_declaration=True, encoding="UTF-8")


def crear_archivos_html(video_filename, ficha_images, pdf_filename, output_folder):
    # Crear video.html
    video_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Video Explicativo</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>Video Explicativo</h1>
        <video controls width="100%">
            <source src="video/{video_filename}" type="video/mp4">
            Tu navegador no soporta la reproducción de video.
        </video>
    </body>
    </html>
    """
    with open(os.path.join(output_folder, "video.html"), 'w') as f:
        f.write(video_html)

    # Crear ficha.html con carrusel que tiene principio y final
    ficha_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Ficha</title>
        <meta charset="utf-8">
        <style>
            .carousel-container {
                position: relative;
                max-width: 100%;
                margin: auto;
                max-height: 450px; /* Ajuste para evitar scroll */
                overflow: hidden;
            }
            .carousel-slide {
                display: none;
                text-align: center;
            }
            .carousel-slide img {
                max-width: 100%;
                height: auto;
                max-height: 450px; /* Ajuste para limitar altura */
            }
            .prev, .next {
                cursor: pointer;
                position: absolute;
                top: 50%;
                width: auto;
                margin-top: -22px;
                padding: 16px;
                color: #cccccc; /* Flechas gris claro visibles */
                font-weight: bold;
                font-size: 18px;
                transition: 0.6s ease;
                border-radius: 0 3px 3px 0;
                user-select: none;
                background-color: rgba(0, 0, 0, 0.1); /* Fondo semitransparente */
            }
            .next {
                right: 0;
                border-radius: 3px 0 0 3px;
            }
            .prev {
                left: 0;
            }
            .prev.disabled, .next.disabled {
                visibility: hidden;
            }
            .active, .prev:hover, .next:hover {
                background-color: rgba(0, 0, 0, 0.3); /* Color más visible al pasar el ratón */
            }
        </style>
    </head>
    <body>
        <h1>Ficha</h1>
        <div class="carousel-container">
    """
    for i, image in enumerate(ficha_images):
        ficha_html += f'''
        <div class="carousel-slide">
            <img src="ficha/{os.path.basename(image)}" alt="Ficha {i+1}">
        </div>
        '''
    ficha_html += """
            <a class="prev" onclick="changeSlide(-1)">&#10094;</a>
            <a class="next" onclick="changeSlide(1)">&#10095;</a>
        </div>

        <script>
            let slideIndex = 0;
            showSlides(slideIndex);

            function changeSlide(n) {
                showSlides(slideIndex += n);
            }

            function showSlides(n) {
                let slides = document.getElementsByClassName("carousel-slide");
                let prevBtn = document.querySelector(".prev");
                let nextBtn = document.querySelector(".next");

                if (n >= slides.length - 1) {
                    slideIndex = slides.length - 1;
                    nextBtn.classList.add('disabled');  // Deshabilita la flecha siguiente
                } else {
                    nextBtn.classList.remove('disabled');
                }

                if (n <= 0) {
                    slideIndex = 0;
                    prevBtn.classList.add('disabled');  // Deshabilita la flecha anterior
                } else {
                    prevBtn.classList.remove('disabled');
                }

                for (let i = 0; i < slides.length; i++) {
                    slides[i].style.display = "none";
                }

                slides[slideIndex].style.display = "block";
            }
        </script>
    </body>
    </html>
    """
    with open(os.path.join(output_folder, "ficha.html"), 'w') as f:
        f.write(ficha_html)

    # Crear pdf.html
    pdf_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Actividad PDF</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>Actividad PDF</h1>
        <iframe src="actividad/{os.path.basename(pdf_filename)}" width="100%" height="600px"></iframe>
    </body>
    </html>
    """
    with open(os.path.join(output_folder, "pdf.html"), 'w') as f:
        f.write(pdf_html)


def empaquetar_scorm(output_folder, output_zip):
    with ZipFile(output_zip, 'w') as zipf:
        for root, dirs, files in os.walk(output_folder):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, output_folder))


def crear_paquete_scorm(video_path, ficha_paths, build_path, pdf_path, output_zip):
    # Crear una carpeta temporal en Documentos para evitar problemas de permisos
    output_folder = os.path.join(os.environ["USERPROFILE"], "Documents", "scorm_package")
    
    # Si la carpeta ya existe, eliminarla
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    
    # Crear las carpetas de destino
    os.makedirs(output_folder)
    os.makedirs(os.path.join(output_folder, "video"))
    os.makedirs(os.path.join(output_folder, "ficha"))
    os.makedirs(os.path.join(output_folder, "actividad"))

    # Copiar los archivos a las carpetas correspondientes
    shutil.copy(video_path, os.path.join(output_folder, "video"))
    for image in ficha_paths:
        shutil.copy(image, os.path.join(output_folder, "ficha"))
    shutil.copy(pdf_path, os.path.join(output_folder, "actividad"))

    # Copiar todo el contenido de la carpeta Build (y el index.html)
    build_dest = os.path.join(output_folder, "Build")
    os.makedirs(build_dest)
    
    for item in os.listdir(build_path):
        s = os.path.join(build_path, item)
        
        # Copiar los archivos de la carpeta `Build` directamente dentro de `Build/`
        if os.path.isdir(s) and item == "Build":  # Es la carpeta Build
            shutil.copytree(s, build_dest, dirs_exist_ok=True)
        elif os.path.isfile(s) and item == "index.html":  # Copiar el index.html
            shutil.copy(s, os.path.join(output_folder, "index.html"))

    # Crear archivos HTML en la raíz
    crear_archivos_html(os.path.basename(video_path), ficha_paths, pdf_path, output_folder)

    # Crear el imsmanifest.xml
    crear_imsmanifest(os.path.basename(video_path), ficha_paths, build_dest, 
                      os.path.join(output_folder, "actividad", os.path.basename(pdf_path)), output_folder)

    # Empaquetar todo en un archivo .zip
    empaquetar_scorm(output_folder, output_zip)
    print(f"Paquete SCORM creado: {output_zip}")


# Interfaz Gráfica para arrastrar y soltar archivos
class SCORMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Creador de Paquetes SCORM")
        
        self.video_path = ""
        self.ficha_paths = []
        self.build_path = ""
        self.pdf_path = ""
        
        # Botones para cargar archivos
        self.create_widgets()

    def create_widgets(self):
        # Botón para cargar el video
        self.btn_video = tk.Button(self.root, text="Cargar Video", command=self.cargar_video)
        self.btn_video.pack(pady=5)
        
        # Botón para cargar imágenes de la ficha
        self.btn_ficha = tk.Button(self.root, text="Cargar Fichas (JPG)", command=self.cargar_fichas)
        self.btn_ficha.pack(pady=5)
        
        # Botón para cargar la build del juego de Unity
        self.btn_build = tk.Button(self.root, text="Cargar Build Unity", command=self.cargar_build)
        self.btn_build.pack(pady=5)
        
        # Botón para cargar el PDF de la actividad
        self.btn_pdf = tk.Button(self.root, text="Cargar PDF Actividad", command=self.cargar_pdf)
        self.btn_pdf.pack(pady=5)
        
        # Botón para crear el paquete SCORM
        self.btn_crear_scorm = tk.Button(self.root, text="Crear Paquete SCORM", command=self.crear_scorm)
        self.btn_crear_scorm.pack(pady=20)
    
    def cargar_video(self):
        self.video_path = filedialog.askopenfilename(filetypes=[("Video MP4", "*.mp4")])
        if self.video_path:
            self.btn_video.config(text="Video Cargado", bg="green", fg="white")
    
    def cargar_fichas(self):
        self.ficha_paths = filedialog.askopenfilenames(filetypes=[("Imágenes JPG", "*.jpg")])
        if self.ficha_paths:
            self.btn_ficha.config(text="Fichas Cargadas", bg="green", fg="white")
    
    def cargar_build(self):
        self.build_path = filedialog.askdirectory()
        if self.build_path:
            self.btn_build.config(text="Build Cargada", bg="green", fg="white")
    
    def cargar_pdf(self):
        self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF", "*.pdf")])
        if self.pdf_path:
            self.btn_pdf.config(text="PDF Cargado", bg="green", fg="white")
    
    def crear_scorm(self):
        if not self.video_path or not self.ficha_paths or not self.build_path or not self.pdf_path:
            messagebox.showwarning("Faltan archivos", "Debes cargar todos los archivos necesarios antes de crear el paquete SCORM")
            return
        
        output_zip = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("Archivo ZIP", "*.zip")])
        if output_zip:
            crear_paquete_scorm(self.video_path, self.ficha_paths, self.build_path, self.pdf_path, output_zip)
            messagebox.showinfo("SCORM creado", f"Paquete SCORM creado exitosamente: {output_zip}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SCORMApp(root)
    root.mainloop()
