#  Browser Permission & Metadata Awareness Tool (PoC)

###  Project Overview
This project is a **Proof of Concept (PoC)** developed for security research and educational purposes. It demonstrates how modern web APIs (Camera, Geolocation, and Metadata) can be accessed by a server once a user grants browser permissions. 

The goal is to raise awareness about **Social Engineering** and the importance of managing browser permissions carefully.

---

### ! LEGAL & ETHICAL DISCLAIMER
**IMPORTANT: This tool is for EDUCATIONAL PURPOSES only.**

* **Usage of this tool for attacking targets without prior mutual consent is illegal.**
* The Organization (**@DsevenFex**) assumes **no liability** and is not responsible for any misuse or damage caused by this program.
* The end-user is solely responsible for complying with all applicable local and international privacy laws (e.g., GDPR).
* **NEVER** use this tool for malicious activities or unauthorized data collection.

---

###  Features
* **Multi-Tunneling:** Support for both `Ngrok` and `Cloudflare` to expose the local server.
* **System Metadata:** Captures `User-Agent`, `IP address`, and `Browser Info`.
* **Geolocation Tracking:** Demonstrates how GPS coordinates are retrieved via the Geolocation API.
* **Media Stream:** Captures camera frames in real-time to illustrate media access risks.
* **Automated Storage:** Organizes captured data into local folders (`photos/`, `infos/`, `locations/`).

###  Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Dsevenfex/FexCam
    cd FexCam
    ```

2. **venv**
   ```bash
   python3 -m vevn venv
   ```
3 **Venv**
  ```bash
  source venv/bin/activate
  ```

4 **Install Dependencies:**
    ``` bash
    pip install -r requirements.txt
    ```

5.  **Run the Tool:**
    ```bash
    python main.py
    ```

5.  **Configuration:**
    * Choose between **Ngrok** or **Cloudflare** in the CLI.
    * If using Ngrok, make sure to provide your `authtoken`.

---

### 📁 Directory Structure
* `photos/` - Stores captured camera images.
* `infos/` - Stores user system information (JSON).
* `locations/` - Stores GPS data (JSON).
* `TOKEN_NGROK.txt` - Local storage for your Ngrok token.

---

###  How to Stay Safe?
* **Be Cautious:** Do not click on suspicious links from unknown sources.
* **Manage Permissions:** Regularly check `chrome://settings/content` (or browser equivalent) to see which sites have access to your camera and location.
* **Use Protection:** Use browser extensions that block scripts and unauthorized tracking.

---

### 📜 License
This project is licensed under the **MIT License** - see the LICENSE file for details.
