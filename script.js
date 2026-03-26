// ==========================================
// ARISE TECH - NEURAL PLATFORM v2.0
// ==========================================

const firebaseConfig = {
    apiKey: "AIzaSyAz8CIPuN8u_8dTWpF1A6Ab65pz045GSf8",
    databaseURL: "https://arise-tech-system-default-rtdb.firebaseio.com",
    projectId: "arise-tech-system"
};

let db = null;
try {
    firebase.initializeApp(firebaseConfig);
    db = firebase.database();
} catch (e) {
    console.error("Firebase Init Error");
}

const CONFIG = {
    ADMIN_NAME: "song.arise",
    SUB_ADMIN: "kiyotaka.ayanokouji",
    DEFAULT_PASS: "1322010",
    MAX_ATTEMPTS: 3
};

let users = {[CONFIG.ADMIN_NAME]: CONFIG.DEFAULT_PASS, [CONFIG.SUB_ADMIN]: CONFIG.DEFAULT_PASS};
let userData = JSON.parse(localStorage.getItem('arise_userdata')) || {};
let currentUser = null;
let pyodide = null;
let editor = null;
let attempts = CONFIG.MAX_ATTEMPTS;

window.onload = function() {
    initPyodide();
    const savedUser = sessionStorage.getItem('arise_current_user');
    if (savedUser) enterSystem(savedUser);
};

async function initPyodide() {
    try {
        pyodide = await loadPyodide();
        await pyodide.loadPackage("micropip");
        document.getElementById('run-btn').disabled = false;
        document.getElementById('run-btn').innerHTML = '▶️ EXECUTE CODE';
    } catch (err) {
        console.error("Pyodide Fail");
    }
}

function initEditor() {
    const container = document.getElementById('editor-container');
    require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs' }});
    require(['vs/editor/editor.main'], function() {
        try {
            editor = monaco.editor.create(container, {
                value: '# Arise Tech System\nprint("System Ready")',
                language: 'python',
                theme: 'vs-dark',
                automaticLayout: true
            });
        } catch (e) {
            showFallbackEditor();
        }
    }, showFallbackEditor);
}

// التعديل الأساسي لوضوح الكتابة
function showFallbackEditor() {
    const container = document.getElementById('editor-container');
    container.innerHTML = '';
    const textarea = document.createElement('textarea');
    textarea.style.cssText = "width:100%; height:100%; background:#1a1a1a; color:#00f2ff; padding:15px; font-family:monospace; font-size:16px; border:none; outline:none; caret-color:white;";
    textarea.value = 'print("Hello World")';
    container.appendChild(textarea);
    editor = { getValue: () => textarea.value, layout: () => {} };
}

function handleLogin() {
    const u = document.getElementById('login-user').value.trim();
    const p = document.getElementById('login-pass').value.trim();
    if (users[u] === p) enterSystem(u);
    else {
        attempts--;
        if (attempts <= 0) window.location.href = "https://wa.me/201055719273";
        else alert("Wrong! Attempts left: " + attempts);
    }
}

function enterSystem(user) {
    currentUser = user;
    sessionStorage.setItem('arise_current_user', user);
    if (!userData[user]) userData[user] = { xp: 0, level: 1 };
    document.getElementById('login-screen').classList.remove('active');
    document.getElementById('main-screen').classList.add('active');
    updateUI();
    initEditor();
}

function updateUI() {
    document.getElementById('display-username').innerText = currentUser;
    document.getElementById('display-level').innerText = userData[currentUser].level;
    document.getElementById('display-xp').innerText = userData[currentUser].xp;
}

async function runCode() {
    const code = editor.getValue();
    const out = document.getElementById('output');
    try {
        pyodide.runPython(`import sys, io\nsys.stdout = io.StringIO()`);
        await pyodide.runPythonAsync(code);
        out.innerText = pyodide.runPython("sys.stdout.getvalue()") || "Done";
        addXP(20);
    } catch (e) { out.innerText = e.toString(); }
}

function addXP(n) {
    userData[currentUser].xp += n;
    userData[currentUser].level = Math.floor(userData[currentUser].xp / 100) + 1;
    updateUI();
    localStorage.setItem('arise_userdata', JSON.stringify(userData));
}
