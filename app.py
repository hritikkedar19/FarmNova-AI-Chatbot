import os
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from config import Config
from database import db
from gemini_service import GeminiService

app = Flask(__name__)
app.config.from_object(Config)
Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)
gemini = GeminiService()
ALLOWED = {"png", "jpg", "jpeg", "webp", "pdf"}

try:
    db.ping()
    print(f"MongoDB Atlas connected: {db.name}")
except Exception as e:
    print(f"MongoDB connection warning: {e}")


def allowed_file(name):
    return "." in name and name.rsplit(".", 1)[1].lower() in ALLOWED


def get_cid(value):
    return db.oid(value)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/health")
def health():
    mongo_ok = False
    try:
        mongo_ok = db.ping()
    except Exception:
        pass
    return jsonify({"status": "ok", "mongodb": mongo_ok, "gemini_configured": bool(os.getenv("GEMINI_API_KEY"))})


@app.get("/api/conversations")
def conversations():
    return jsonify([db.conversation_dict(c) for c in db.list_conversations()])


@app.post("/api/conversations")
def create_conversation():
    c = db.create_conversation()
    return jsonify(db.conversation_dict(c)), 201


@app.get("/api/conversations/<cid>")
def get_conversation(cid):
    c = db.get_conversation(cid)
    if not c:
        return jsonify({"error": "Conversation not found."}), 404
    return jsonify({**db.conversation_dict(c), "messages": [db.message_dict(m) for m in db.get_messages(cid)]})


@app.delete("/api/conversations/<cid>")
def delete_conversation(cid):
    if not db.delete_conversation(cid):
        return jsonify({"error": "Conversation not found."}), 404
    return jsonify({"success": True})


@app.post("/api/chat")
def chat():
    text = (request.form.get("message") or "").strip()
    cid = request.form.get("conversation_id")
    if not text and not request.files.get("file"):
        return jsonify({"error": "Please enter a message or attach a file."}), 400

    c = db.get_conversation(cid) if cid else None
    if not c:
        c = db.create_conversation()
    cid = str(c["_id"])

    f = request.files.get("file")
    saved = name = ftype = None
    if f and f.filename:
        if not allowed_file(f.filename):
            return jsonify({"error": "Allowed files: PNG, JPG, JPEG, WEBP and PDF."}), 400
        f.stream.seek(0, 2); size = f.stream.tell(); f.stream.seek(0)
        if size > app.config["MAX_UPLOAD_MB"] * 1024 * 1024:
            return jsonify({"error": f"Maximum file size is {app.config['MAX_UPLOAD_MB']} MB."}), 400
        name = secure_filename(f.filename)
        ext = name.rsplit(".", 1)[1].lower()
        folder = Path(app.config["UPLOAD_FOLDER"]) / ("documents" if ext == "pdf" else "images")
        folder.mkdir(parents=True, exist_ok=True)
        saved = str(folder / f"{cid}_{len(db.get_messages(cid)) + 1}_{name}")
        f.save(saved); ftype = f.mimetype

    db.add_message(cid, "user", text or "Please analyze the attached file.", name, ftype, saved)

    try:
        history = db.get_messages(cid)
        reply = gemini.generate_reply(history, latest_file=saved)
        a = db.add_message(cid, "assistant", reply)
        if c.get("title") == "New FarmNova Chat" and text:
            db.update_title(cid, text[:60])
        return jsonify({"conversation_id": cid, "message": db.message_dict(a)})
    except Exception as e:
        return jsonify({"error": str(e)}), 503 if "temporarily busy" in str(e).lower() else 500


@app.post("/api/regenerate/<cid>")
def regenerate(cid):
    c = db.get_conversation(cid)
    if not c:
        return jsonify({"error": "Conversation not found."}), 404
    messages = db.get_messages(cid)
    users = [m for m in messages if m.get("role") == "user"]
    if not users:
        return jsonify({"error": "No user message to regenerate."}), 400
    try:
        reply = gemini.generate_reply(messages, latest_file=users[-1].get("file_path"))
        a = db.add_message(cid, "assistant", reply)
        return jsonify({"message": db.message_dict(a)})
    except Exception as e:
        return jsonify({"error": str(e)}), 503 if "temporarily busy" in str(e).lower() else 500


@app.get("/api/conversations/<cid>/pdf")
def pdf(cid):
    c = db.get_conversation(cid)
    if not c:
        return jsonify({"error": "Conversation not found."}), 404
    out = Path(app.config["UPLOAD_FOLDER"]) / "reports"; out.mkdir(parents=True, exist_ok=True)
    filename = f"farmnova_chat_{cid}.pdf"; path = out / filename
    styles = getSampleStyleSheet()
    story = [Paragraph("FarmNova AI Conversation Report", styles["Title"]), Spacer(1, 12),
             Paragraph(c.get("title", "FarmNova Chat"), styles["Heading2"]), Spacer(1, 12)]
    for m in db.get_messages(cid):
        role = "Farmer" if m.get("role") == "user" else "FarmNova AI"
        safe = (m.get("content") or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br/>")
        story += [Paragraph(f"<b>{role}</b>", styles["Heading3"]), Paragraph(safe, styles["BodyText"])]
        if m.get("file_name"): story.append(Paragraph(f"Attachment: {m['file_name']}", styles["BodyText"]))
        story.append(Spacer(1, 10))
    SimpleDocTemplate(str(path), pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40).build(story)
    return send_from_directory(out, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=os.getenv("FLASK_DEBUG", "0") == "1")
