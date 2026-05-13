import os
import time
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from ..modules import FileEntry, db

files_bp = Blueprint("files", __name__)

@files_bp.route("/api/files", methods=["GET"])
def list_files():
    files = FileEntry.query.order_by(FileEntry.id.desc()).all()
    return jsonify([{
        "id": f.id,
        "filename": f.filename,
        "original_name": f.original_name,
        "size": f.size,
        "mime_type": f.mime_type,
        "uploaded_by": f.uploaded_by,
        "created_at": f.created_at
    } for f in files])

@files_bp.route("/api/files/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    original_name = file.filename
    ext = original_name.rsplit(".", 1)[-1].lower() if "." in original_name else ""
    filename = f"{int(time.time())}_{secure_filename(original_name)}"
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)

    size = os.path.getsize(filepath)
    mime_type = file.content_type or ""
    uploaded_by = request.form.get("uploaded_by", 0, type=int)
    created_at = time.strftime("%Y-%m-%d %H:%M:%S")

    entry = FileEntry(
        filename=filename,
        original_name=original_name,
        filepath=filepath,
        size=size,
        mime_type=mime_type,
        uploaded_by=uploaded_by,
        created_at=created_at
    )
    db.session.add(entry)
    db.session.commit()

    return jsonify({"id": entry.id, "message": "File uploaded"})

@files_bp.route("/api/files/<int:file_id>/delete", methods=["DELETE"])
def delete_file(file_id):
    entry = FileEntry.query.get(file_id)
    if not entry:
        return jsonify({"error": "File not found"}), 404
    try:
        if os.path.exists(entry.filepath):
            os.remove(entry.filepath)
    except:
        pass
    db.session.delete(entry)
    db.session.commit()
    return jsonify({"message": "File deleted"})
