FexCam
## Project Overview

This project is a **Proof of Concept (PoC)** developed for **security
research and educational purposes**.\
It demonstrates the technical capabilities of modern web APIs---such as
**Camera**, **Geolocation**, and **Metadata**---and how they can be
accessed by a server once a user grants explicit browser permissions.

The primary objective is to raise awareness about **Social Engineering
tactics** and the critical importance of **proper browser permission
management**.

------------------------------------------------------------------------

## Legal & Ethical Disclaimer

> **IMPORTANT: THIS TOOL IS FOR EDUCATIONAL PURPOSES ONLY**

-   **Unauthorized Usage:** Using this tool against targets without
    prior **mutual written consent** is strictly prohibited and may be
    illegal.
-   **Liability:** The organization (**@DsevenFex**) assumes **no
    responsibility** for misuse, data loss, or legal consequences
    resulting from this software.
-   **Compliance:** The end-user is solely responsible for compliance
    with all applicable **local and international privacy regulations**
    (e.g., GDPR, CCPA).
-   **Prohibition:** Malicious activities or unauthorized data
    collection are **strictly forbidden**.

------------------------------------------------------------------------

## Technical Features

-   **Multi-Tunneling Support**\
    Integrated support for **Ngrok** and **Cloudflare** to expose local
    development servers to the internet.

-   **System Metadata Extraction**\
    Captures **User-Agent**, **IP address**, and detailed browser
    configuration data.

-   **Geolocation Precision**\
    Demonstrates retrieval of GPS coordinates using the **W3C
    Geolocation API**.

-   **Media Stream Processing**\
    Real-time camera frame capture to highlight risks associated with
    media access permissions.

-   **Automated Data Management**\
    Structured organization of captured data into dedicated local
    directories.

------------------------------------------------------------------------

## Installation & Deployment

### 1. Repository Cloning

``` bash
git clone https://github.com/Dsevenfex/FexCam
cd FexCam
```

### 2. Environment Configuration

``` bash
python3 -m venv venv
```
##### Linux && Mac
```bash
source venv/bin/activate 
```
##### Windows
```bash
venv\Scripts\activate 

```

### 3. Dependency Installation

``` bash
pip install -r requirements.txt
```

### 4. Execution

``` bash
python FexCam.py
```

### 5. Tunneling Setup

-   Select **Ngrok** or **Cloudflare** via the CLI.
-   If **Ngrok** is selected, ensure a valid `authtoken` is configured.

------------------------------------------------------------------------


##  Directory Architecture

| Path               | Description                                   |
|--------------------|-----------------------------------------------|
| `photos/`          | Archived captured media assets                |
| `infos/`           | System and browser metadata (JSON)            |
| `locations/`       | Geographic coordinate data (JSON)             |
| `TOKEN_NGROK.txt`  | Local Ngrok authentication token              |

---


## License

This project is distributed under the **MIT License**.\
Refer to the official `LICENSE` file for further details.


