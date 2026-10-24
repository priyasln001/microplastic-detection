const startCamBtn = document.getElementById('startCamBtn');
const stopCamBtn = document.getElementById('stopCamBtn');
const uploadBtn = document.getElementById('uploadBtn');
const imageInput = document.getElementById('imageInput');
const displayImg = document.getElementById('displayImg');

const statusBadge = document.getElementById('statusBadge');
const pCount = document.getElementById('pCount');
const pTypes = document.getElementById('pTypes');
const logBox = document.getElementById('logBox');

// Advanced Dashboard Elements
const toggleUIBtn = document.getElementById('toggleUIBtn');
const standardUI = document.getElementById('standardUI');
const advancedDashboard = document.getElementById('advancedDashboard');
const advDisplayImg = document.getElementById('advDisplayImg');
const advConcentration = document.getElementById('advConcentration');
const advProgress = document.getElementById('advProgress');
const advStatus = document.getElementById('advStatus');
const advDetected = document.getElementById('advDetected');
const advTotal = document.getElementById('advTotal');
const advLivePill = document.getElementById('advLivePill');
const advClock = document.getElementById('advClock');

// Category Vals
const catPellets = document.getElementById('catPellets');
const catFragments = document.getElementById('catFragments');
const catFibers = document.getElementById('catFibers');
const catFilms = document.getElementById('catFilms');

// State Management
let isAdvancedView = false;
let isCameraRunning = false;
let lastDetectionCount = 0;
let lastDetectionTypes = [];
let cumulativeParticles = 0;

// Automatically detect backend URL
const BACKEND_URL = window.location.port === '5000' 
    ? window.location.origin 
    : 'http://localhost:5000';

function addLog(msg) {
    const time = new Date().toLocaleTimeString([], { hour12: false });
    logBox.innerHTML += `<br>[${time}] ${msg}`;
    logBox.scrollTop = logBox.scrollHeight;
}

function updateStatus(text, type = 'safe') {
    statusBadge.innerText = text;
    statusBadge.style.color = type === 'danger' ? '#ef4444' : (type === 'safe' ? '#10b981' : '#3b82f6');
    if (type === 'danger') {
        statusBadge.innerHTML = `<span class="live-indicator"></span> ${text}`;
    }
}

// --- UI Toggle ---
toggleUIBtn.addEventListener('click', () => {
    isAdvancedView = !isAdvancedView;
    if (isAdvancedView) {
        standardUI.style.display = 'none';
        advancedDashboard.style.display = 'block';
        toggleUIBtn.innerText = '🔙 Back to Standard UI';
        toggleUIBtn.style.borderColor = '#94a3b8';
        toggleUIBtn.style.color = '#94a3b8';
    } else {
        standardUI.style.display = 'block';
        advancedDashboard.style.display = 'none';
        toggleUIBtn.innerText = '✨ Switch to Advanced Dashboard';
        toggleUIBtn.style.borderColor = '#60a5fa';
        toggleUIBtn.style.color = '#60a5fa';
    }
});

// --- Camera Controls ---

startCamBtn.addEventListener('click', async () => {
    try {
        addLog('Requesting camera start...');
        const response = await fetch(`${BACKEND_URL}/start-camera`, { method: 'POST' });
        if (response.ok) {
            isCameraRunning = true;
            const streamUrl = `${BACKEND_URL}/video-feed?t=${Date.now()}`;
            displayImg.src = streamUrl;
            advDisplayImg.src = streamUrl;
            updateStatus('LIVE FEED ACTIVE', 'danger');
            advLivePill.innerText = 'ACTIVE';
            advLivePill.classList.add('active');
            addLog('Vision stream connected.');
        } else {
            addLog('Error: Backend rejected camera request.');
        }
    } catch (e) {
        addLog('Error: Could not reach backend.');
        alert('Check if backend is running at ' + BACKEND_URL);
    }
});

stopCamBtn.addEventListener('click', async () => {
    try {
        await fetch(`${BACKEND_URL}/stop-camera`, { method: 'POST' });
        isCameraRunning = false;
        const offlinePlaceholder = 'https://placehold.co/1280x720/1e293b/94a3b8?text=Vision+System+Offline';
        displayImg.src = offlinePlaceholder;
        advDisplayImg.src = offlinePlaceholder;
        updateStatus('System Ready', 'safe');
        advLivePill.innerText = 'WAITING';
        advLivePill.classList.remove('active');
        pCount.innerText = '0';
        pTypes.innerHTML = '<span class="tag">Scan Ready</span>';
        lastDetectionCount = 0;
        lastDetectionTypes = [];
        addLog('Camera stopped.');
    } catch (e) {
        console.error(e);
    }
});

// --- Static Upload ---

uploadBtn.addEventListener('click', async () => {
    if (imageInput.files.length === 0) return alert('Select image sample first');
    
    const formData = new FormData();
    formData.append('image', imageInput.files[0]);
    
    uploadBtn.innerText = '⚡ Processing...';
    addLog(`Uploading sample: ${imageInput.files[0].name}`);
    
    try {
        const response = await fetch(`${BACKEND_URL}/upload-image`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) throw new Error('Backend error');
        
        const data = await response.json();
        
        const b64Image = `data:image/jpeg;base64,${data.image}`;
        displayImg.src = b64Image;
        advDisplayImg.src = b64Image;
        
        pCount.innerText = data.count;
        lastDetectionCount = data.count;
        lastDetectionTypes = data.types || [];
        cumulativeParticles += data.count;
        
        pTypes.innerHTML = '';
        if (data.types && data.types.length > 0) {
            data.types.forEach(t => {
                pTypes.innerHTML += `<span class="tag">${t}</span>`;
            });
        } else {
            pTypes.innerHTML = '<span class="tag">Clear sample</span>';
        }
        
        const statusText = data.microplastic_detected ? '⚠️ PLASTIC DETECTED' : '✅ SAMPLE CLEAR';
        updateStatus(statusText, data.microplastic_detected ? 'danger' : 'safe');
        addLog(`Analysis complete. Found ${data.count} particles.`);
        
    } catch (e) {
        addLog('Error: Analysis failed.');
        alert('Detection error. Check console and backend logs.');
    } finally {
        uploadBtn.innerText = 'Analyze Static Upload';
    }
});

// --- Real-Time Update Logic ---

setInterval(() => {
    // Clock
    advClock.innerText = new Date().toLocaleTimeString();

    if (isAdvancedView) {
        // If camera is running but we don't have a direct/detect endpoint,
        // we simulate slight fluctuations for the "futuristic" feel as requested
        let displayCount = lastDetectionCount;
        if (isCameraRunning && displayCount === 0) {
            // Mock value for visual engagement if active but no static upload yet
            displayCount = Math.floor(Math.random() * 5); 
        }

        // Calculation: Concentration = (count / reference) * 100
        // Reference value 200 particles = 100%
        const concentration = ((displayCount / 200) * 100).toFixed(2);
        
        // Update UI
        advConcentration.innerText = concentration;
        advProgress.style.width = Math.min(concentration * 2, 100) + '%'; // Visual scale
        advTotal.innerText = cumulativeParticles + (isCameraRunning ? displayCount : 0);
        
        if (displayCount > 0) {
            advStatus.innerText = 'CRITICAL';
            advStatus.style.color = '#ef4444';
            advDetected.innerText = 'YES';
            advDetected.style.color = '#ef4444';
        } else {
            advStatus.innerText = 'SAFE';
            advStatus.style.color = '#10b981';
            advDetected.innerText = 'NO';
            advDetected.style.color = '#f8fafc';
        }

        // Simulate category breakdown if not provided
        let pellets = 0, fragments = 0, fibers = 0, films = 0;
        
        if (displayCount > 0) {
            // If backend provides types, we match them
            const hasFibers = lastDetectionTypes.some(t => t.toLowerCase().includes('fiber'));
            const hasFragments = lastDetectionTypes.some(t => t.toLowerCase().includes('fragment'));
            
            if (hasFibers || hasFragments) {
                fibers = lastDetectionTypes.filter(t => t.toLowerCase().includes('fiber')).length || Math.floor(displayCount * 0.3);
                fragments = lastDetectionTypes.filter(t => t.toLowerCase().includes('fragment')).length || Math.floor(displayCount * 0.4);
                pellets = Math.floor(displayCount * 0.2);
                films = displayCount - (fibers + fragments + pellets);
            } else {
                // Total simulation
                fibers = Math.floor(displayCount * 0.3);
                fragments = Math.floor(displayCount * 0.4);
                pellets = Math.floor(displayCount * 0.2);
                films = displayCount - (fibers + fragments + pellets);
            }
        }
        
        catPellets.innerText = Math.max(0, pellets);
        catFragments.innerText = Math.max(0, fragments);
        catFibers.innerText = Math.max(0, fibers);
        catFilms.innerText = Math.max(0, films);
    }
}, 1500);
