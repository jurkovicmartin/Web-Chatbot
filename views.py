from flask import Blueprint, render_template, request, redirect, url_for, send_file, jsonify
import json
import io

from saves import Saves
from model import Model


views = Blueprint(__name__, "views")

chat_saves = Saves()
chat = ""

@views.route("/", methods=["GET", "POST"])
def main():
    response = None
    prompt = None
    checkbox_state = ""

    if request.method == "POST":
        model = Model()

        ### SUBMIT
        prompt = request.form.get("text_input")
        short_answer = request.form.get("checkbox")

        if prompt:
            response = model.get_response(prompt, short_answer)

            dialog = f"<br><br><h2>{prompt}</h2>" + response
            global chat
            chat += dialog
        # Keep the checkbox state
        checkbox_state = "checked" if short_answer else ""

    return render_template("index.html", chat=chat, checkbox_state=checkbox_state, chat_saves=chat_saves)


@views.route("/clear", methods=["POST"])
def clear_chat():
    chat.clear()
    return redirect(url_for("views.main"))


@views.route("/save", methods=["POST"])
def save_chat():
    save_name = f"Save{len(chat_saves) + 1}"
    chat_saves.add_save(save_name, chat)
    return redirect(url_for("views.main"))


@views.route("/saves", methods=["POST"])
def manage_saves():
    # Saves actions
    action = request.form.get("action")

    if action == "rename":
        old_name = request.form.get("old_name")
        new_name = request.form.get("new_name")
        chat_saves.rename_save(old_name, new_name)

    elif action == "delete":
        name = request.form.get("save_name")
        chat_saves.delete_save(name)
        

    elif action == "load":
        name = request.form.get("save_name")
        content = chat_saves.load_save(name)

        global chat
        chat = content
    
    return redirect(url_for("views.main"))



@views.route("/export", methods=["POST"])
def export_saves():
    # Dictionary to json
    data = json.dumps(chat_saves)

    byte_content = io.BytesIO(data.encode("utf-8"))

    # Return the json file as a downloadable file
    return send_file(byte_content, as_attachment=True, download_name="data.json", mimetype="viewslication/json")


@views.route("/upload", methods=["POST"])
def load_saves():
    # Check if the post request has the file part
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["file"]
    
    # If no file is selected
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    # Process the JSON file
    if file and file.filename.endswith(".json"):
        try:
            # Read the JSON data from the file
            data = json.load(file)
            print(type(data))
            for name, content in data.items():
                chat_saves.add_save(name, content)
            
            return redirect(url_for("views.main"))
        
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON file"}), 400
    
    return jsonify({"error": "Only JSON files are allowed"}), 400