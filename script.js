// ==========================================
// ARISE TECH - NEURAL PLATFORM v2.0
// Fixed: Editor visibility, Login stability, Mobile responsive
// ==========================================

// ===== FIREBASE CONFIG =====
const firebaseConfig = {
    apiKey: "AIzaSyAz8CIPuN8u_8dTWpF1A6Ab65pz045GSf8",
    databaseURL: "https://arise-tech-system-default-rtdb.firebaseio.com",
    projectId: "arise-tech-system"
};

// Initialize Firebase safely
let db = null;
try {
    firebase.initializeApp(firebaseConfig);
    db = firebase.database();
    console.log("✅ Firebase Connected");
} catch (e) {
    console.warn("⚠️ Firebase Error:", e);
}

// ===== CONFIG =====
const CONFIG = {
    ADMIN_NAME: "song.arise",
    SUB_ADMIN: "kiyotaka.ayanokouji",
    DEFAULT_PASS: "1322010",
    WHATSAPP: {
        EGYPT: "201055719273",
        KUWAIT: "96597805334"
    },
    XP_PER_RUN: 20,
    XP_PER_LEVEL: 100,
    MAX_HISTORY: 5,
    MAX_ATTEMPTS: 3
};

// ===== STATE =====
let users = {};
let userData = {};
let currentUser = null;
let pyodide = null;
let editor = null;
let attempts = CONFIG.MAX_ATTEMPTS;
let isBlocked = false;
let isEditorReady = false;
let isPyodideReady = false;

// Safe localStorage
try {
    users = JSON.parse(localStorage.getItem('arise_users')) || {
        [CONFIG.ADMIN_NAME]: CONFIG.DEFAULT_PASS,
        [CONFIG.SUB_ADMIN]: CONFIG.DEFAULT_PASS
    };
    userData = JSON.parse(localStorage.getItem('arise_userdata')) || {};
} catch (e) {
    console.warn("LocalStorage error:", e);
    users = {
        [CONFIG.ADMIN_NAME]: CONFIG.DEFAULT_PASS,
        [CONFIG.SUB_ADMIN]: CONFIG.DEFAULT_PASS
    };
}

// ===== INITIALIZATION =====
window.onload = function() {
    console.log("🚀 Arise Tech Initializing...");
    initPyodide();
    setTimeout(checkSession, 500);
};

// ===== PYODIDE (Background Loading) =====
async function initPyodide() {
    try {
        updateSystemStatus("Loading Python Engine...");
        pyodide = await loadPyodide();
        await pyodide.loadPackage("micropip");
        isPyodideReady = true;
        updateSystemStatus("✅ System Ready");
        const runBtn = document.getElementById('run-btn');
        if (runBtn && isEditorReady) {
            runBtn.disabled = false;
            runBtn.innerHTML = '▶️ EXECUTE CODE';
        }
    } catch (err) {
        console.error("❌ Pyodide Error:", err);
        updateSystemStatus("⚠️ Engine Error - Refresh");
    }
}

function updateSystemStatus(msg) {
    const status = document.getElementById('system-status');
    if (status) status.innerText = msg;
}

// ===== MONACO EDITOR (FIXED) =====
function initEditor() {
    console.log("📝 Initializing Monaco Editor...");
    const container = document.getElementById('editor-container');
    if (!container) return;

    container.style.width = '100%';
    container.style.height = '400px';

    require.config({ 
        paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs' }
    });

    require(['vs/editor/editor.main'], function() {
        try {
            if (editor) editor.dispose();
            editor = monaco.editor.create(container, {
                value: '# Welcome to Arise Tech\nprint("Hello Neural World!")',
                language: 'python',
                theme: 'vs-dark',
                fontSize: window.innerWidth < 768 ? 14 : 16,
                fontFamily: 'Consolas, "Courier New", monospace',
                minimap: { enabled: false },
                automaticLayout: true,
                padding: { top: 15 }
            });
            setTimeout(() => { if(editor) editor.layout(); }, 100);
            isEditorReady = true;
            document.getElementById('run-btn').disabled = false;
            document.getElementById('run-btn').innerHTML = '▶️ EXECUTE CODE';
        } catch (err) {
            showFallbackEditor();
        }
    });
}

// --- FIX: VISIBILITY IN FALLBACK EDITOR ---
function showFallbackEditor() {
    const container = document.getElementById('editor-container');
    const fallback = document.getElementById('editor-fallback');
    if (!container) return;

    container.innerHTML = '';
    const textarea = document.createElement('textarea');
    textarea.id = 'fallback-textarea';
    
    // التعديل هنا لضمان الرؤية التامة
    textarea.style.width = '100%';
    textarea.style.height = '100%';
    textarea.style.background = '#1e1e1e'; 
    textarea.style.color = '#00f2ff'; // لون سيان واضح جداً
    textarea.style.padding = '15px';
    textarea.style.fontSize = '16px';
    textarea.style.fontFamily = 'monospace';
    textarea.style.caretColor = 'white';
    textarea.style.outline = 'none';
    textarea.style.border = 'none';
    textarea.value = '# Arise Tech Editor\nprint("Hello World")';

    container.appendChild(textarea);
    editor = {
        getValue: () => textarea.value,
        setValue: (v) => textarea.value = v,
        layout: () => {}
    };
    isEditorReady = true;
    document.getElementById('run-btn').disabled = false;
}

// ===== SECURITY / LOGIN =====
function handleLogin() {
    if (isBlocked) return;
    const user = document.getElementById('login-user').value.trim();
    const pass = document.getElementById('login-pass').value.trim();
    if (users[user] === pass) {
        enterSystem(user);
    } else {
        handleFailedAttempt();
    }
}

function handleFailedAttempt() {
    attempts--;
    if (attempts <= 0) blockSystem();
    else showToast(`Invalid! ${attempts} left`, "error");
}

function blockSystem() {
    isBlocked = true;
    showToast("ACCESS DENIED: Redirecting...", "blocked");
    setTimeout(() => {
        window.location.href = `https://wa.me/${CONFIG.WHATSAPP.EGYPT}`;
    }, 2000);
}

function showToast(message, type) {
    const alertBox = document.getElementById('security-alert');
    if (!alertBox) return;
    alertBox.innerText = message;
    alertBox.className = 'security-toast toast-active';
    setTimeout(() => alertBox.classList.remove('toast-active'), 3000);
}

function enterSystem(user) {
    currentUser = user;
    sessionStorage.setItem('arise_current_user', user);
    if (!userData[user]) userData[user] = { xp: 0, level: 1, history: [] };
    showScreen('main-screen');
    updateUI();
    setTimeout(initEditor, 300);
}

function checkSession() {
    const user = sessionStorage.getItem('arise_current_user');
    if (user) enterSystem(user);
}

function showScreen(id) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById(id).classList.add('active');
}

function updateUI() {
    if (!currentUser) return;
    document.getElementById('display-username').innerText = currentUser;
    document.getElementById('display-level').innerText = userData[currentUser].level;
    document.getElementById('display-xp').innerText = userData[currentUser].xp;
}

// باقي الوظائف (runCode, addXP, etc) تظل كما هي في كودك الأصلي...
async function runCode() {
    if (!isEditorReady || !isPyodideReady) return;
    const code = editor.getValue();
    const outputEl = document.getElementById('output');
    try {
        pyodide.runPython(`import sys, io\nsys.stdout = io.StringIO()`);
        await pyodide.runPythonAsync(code);
        outputEl.innerText = pyodide.runPython("sys.stdout.getvalue()") || "✅ Success";
        outputEl.className = 'output-success';
        addXP(20);
    } catch (err) {
        outputEl.innerText = err.toString();
        outputEl.className = 'output-error';
    }
}

function addXP(amount) {
    userData[currentUser].xp += amount;
    const newLevel = Math.floor(userData[currentUser].xp / 100) + 1;
    if (newLevel > userData[currentUser].level) {
        userData[currentUser].level = newLevel;
        alert("Level Up!");
    }
    updateUI();
    saveData();
}

function saveData() {
    localStorage.setItem('arise_userdata', JSON.stringify(userData));
}

function logout() {
    sessionStorage.clear();
    location.reload();
}
