import os
import time
from flask import Blueprint, request, jsonify, current_app, send_file
from werkzeug.utils import secure_filename
from ..modules import FileEntry, User, db

files_bp = Blueprint("files", __name__)

def file_to_dict(f):
    uploader = User.query.get(f.uploaded_by) if f.uploaded_by else None
    return {
        "id": f.id,
        "filename": f.filename,
        "original_name": f.original_name,
        "size": f.size,
        "mime_type": f.mime_type,
        "uploaded_by": f.uploaded_by,
        "workspaceId": f.workspaceId,
        "uploader_name": (uploader.name or uploader.username) if uploader else "Inconnu",
        "created_at": f.created_at
    }

@files_bp.route("/api/files", methods=["GET"])
def list_files():
    files = FileEntry.query.order_by(FileEntry.id.desc()).all()
    return jsonify([file_to_dict(f) for f in files])

@files_bp.route("/api/workspaces/<int:workspace_id>/files", methods=["GET"])
def workspace_files(workspace_id):
    files = FileEntry.query.filter_by(workspaceId=workspace_id).order_by(FileEntry.id.desc()).all()
    return jsonify([file_to_dict(f) for f in files])

@files_bp.route("/api/files/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    files = request.files.getlist("file")
    if not files or all(f.filename == "" for f in files):
        return jsonify({"error": "No file selected"}), 400

    uploaded_by = request.form.get("uploaded_by", 0, type=int)
    workspaceId = request.form.get("workspaceId", type=int)
    created_at = time.strftime("%Y-%m-%d %H:%M:%S")
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    entries = []

    for file in files:
        if file.filename == "":
            continue
        original_name = file.filename
        filename = f"{int(time.time() * 1000)}_{secure_filename(original_name)}"
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        size = os.path.getsize(filepath)
        mime_type = file.content_type or ""
        entry = FileEntry(
            filename=filename,
            original_name=original_name,
            filepath=filepath,
            size=size,
            mime_type=mime_type,
            uploaded_by=uploaded_by,
            workspaceId=workspaceId,
            created_at=created_at
        )
        db.session.add(entry)
        entries.append(entry)

    db.session.commit()
    return jsonify({"message": f"{len(entries)} fichier(s) uploade(s)", "count": len(entries)})

@files_bp.route("/api/files/<int:file_id>/download")
def download_file(file_id):
    entry = FileEntry.query.get(file_id)
    if not entry or not os.path.exists(entry.filepath):
        return jsonify({"error": "File not found"}), 404
    return send_file(entry.filepath, as_attachment=True, download_name=entry.original_name)

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
