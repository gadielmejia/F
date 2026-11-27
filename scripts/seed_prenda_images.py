import os  # noqa: E402
import shutil  # noqa: E402
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
from app import create_app  # noqa: E402
from app.database.database import db  # noqa: E402
from app.models.prenda import Prenda  # noqa: E402
from app.models.prenda_imagen import PrendaImagen  # noqa: E402

FRONTEND_ASSETS_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), "..", "..", "RENTSTYLE-FRONT-EDN", "src", "assets"
    )
)
UPLOADS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "app", "static", "uploads", "prendas")
)

PRODUCT_IMAGE_MAP = {
    1: "vestidoverde.jpg",
    2: "vestidonregro.jpg",
    3: "vestidoazul.png",
    4: "vestidorojo.png",
    5: "vestidodorado.png",
}


def ensure_uploads_dir():
    os.makedirs(UPLOADS_DIR, exist_ok=True)


def copy_asset_to_uploads(asset_name):
    src = os.path.join(FRONTEND_ASSETS_DIR, asset_name)
    if not os.path.isfile(src):
        raise FileNotFoundError(f"No se encontró el asset de imagen: {src}")
    base, ext = os.path.splitext(asset_name)
    dst_name = f"{base}_{os.path.getmtime(src):.0f}{ext}"
    dst = os.path.join(UPLOADS_DIR, dst_name)
    shutil.copy2(src, dst)
    return dst_name


def main():
    ensure_uploads_dir()
    app = create_app()
    with app.app_context():
        for prenda_id, asset_name in PRODUCT_IMAGE_MAP.items():
            prenda = Prenda.query.get(prenda_id)
            if not prenda:
                print(f"[SKIP] Prenda {prenda_id} no encontrada")
                continue

            if prenda.imagenes:
                print(
                    f"[SKIP] Prenda {prenda_id} ya tiene {len(prenda.imagenes)} imagen(es)"
                )
                continue

            try:
                saved_filename = copy_asset_to_uploads(asset_name)
            except FileNotFoundError as exc:
                print(f"[ERROR] {exc}")
                continue

            imagen = PrendaImagen(idPrenda=prenda_id, filename=saved_filename)
            db.session.add(imagen)
            db.session.commit()
            print(f"[OK] Prenda {prenda_id} -> {saved_filename}")

        print("Seed terminado.")


if __name__ == "__main__":
    main()
