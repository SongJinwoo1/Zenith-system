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
    
    // Start systems in parallel
    initPyodide();
    
    // Check session after short delay
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
        console.log("✅ Pyodide Ready");
        
        // Update button if on main screen
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
    if (!container) {
        console.error("Editor container not found!");
        return;
    }
    
    // Ensure container has size
    container.style.width = '100%';
    container.style.height = '400px';
    
    require.config({ 
        paths: { 
            'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs' 
        }
    });
    
    require(['vs/editor/editor.main'], function() {
        try {
            // Destroy old instance if exists
            if (editor) {
                editor.dispose();
            }
            
            editor = monaco.editor.create(container, {
                value: '# Welcome to Arise Tech\n# Write your Python code here\nprint("Hello Neural World!")',
                language: 'python',
                theme: 'vs-dark',
                fontSize: window.innerWidth < 768 ? 14 : 16,
                fontFamily: 'Consolas, "Courier New", monospace',
                minimap: { enabled: false },
                scrollBeyondLastLine: false,
                automaticLayout: true, // KEY: Auto-resize
                padding: { top: 15 },
                lineNumbers: 'on',
                roundedSelection: false,
                selectOnLineNumbers: true,
                cursorBlinking: 'smooth',
                cursorStyle: 'line',
                cursorWidth: 2,
                renderLineHighlight: 'all',
                quickSuggestions: true,
                suggestOnTriggerCharacters: true,
                acceptSuggestionOnEnter: 'on',
                tabSize: 4,
                insertSpaces: true,
                detectIndentation: true,
                scrollbar: {
                    useShadows: false,
                    vertical: 'auto',
                    horizontal: 'auto',
                    verticalHasArrows: false,
                    horizontalHasArrows: false,
                    verticalScrollbarSize: 10,
                    horizontalScrollbarSize: 10
                }
            });
            
            // CRITICAL FIX: Force layout after creation
            setTimeout(() => {
                editor.layout();
                console.log("✅ Editor Layout Forced");
            }, 100);
            
            // Resize observer
            window.addEventListener('resize', () => {
                if (editor) {
                    editor.layout();
                    editor.updateOptions({ 
                        fontSize: window.innerWidth < 768 ? 14 : 16 
                    });
                }
            });
            
            // Orientation change
            window.addEventListener('orientationchange', () => {
                setTimeout(() => {
                    if (editor) editor.layout();
                }, 300);
            });
            
            isEditorReady = true;
            
            // Update UI
            const status = document.getElementById('editor-status');
            if (status) status.innerText = 'Ready';
            
            const runBtn = document.getElementById('run-btn');
            if (runBtn && isPyodideReady) {
                runBtn.disabled = false;
                runBtn.innerHTML = '▶️ EXECUTE CODE';
            }
            
            console.log("✅ Monaco Editor Ready");
            
        } catch (err) {
            console.error("❌ Editor Error:", err);
            showFallbackEditor();
        }
    });
}

function showFallbackEditor() {
    const container = document.getElementById('editor-container');
    const fallback = document.getElementById('editor-fallback');
    
    if (container && fallback) {
        container.innerHTML = '';
        fallback.style.display = 'block';
        container.appendChild(fallback);
        
        // Create textarea fallback
        const textarea = document.createElement('textarea');
        textarea.id = 'fallback-textarea';
        textarea.style.width = '100%';
        textarea.style.height = '100%';
        textarea.style.background = '#1e1e1e';
        textarea.style.color = '#d4d4d4';
        textarea.style.border = 'none';
        textarea.style.padding = '15px';
        textarea.style.fontFamily = 'Consolas, monospace';
        textarea.style.fontSize = '14px';
        textarea.style.resize = 'none';
        textarea.value = '# Monaco failed to load\n# Using fallback editor\nprint("Hello World")';
        
        container.appendChild(textarea);
        
        // Override getValue for compatibility
        editor = {
            getValue: () => textarea.value,
            setValue: (v) => textarea.value = v,
            layout: () => {}
        };
        
        isEditorReady = true;
        document.getElementById('run-btn').disabled = false;
        document.getElementById('run-btn').innerHTML = '▶️ EXECUTE CODE';
    }
}

// ===== SECURITY / LOGIN =====
function handleLogin() {
    if (isBlocked) return;
    
    const userInput = document.getElementById('login-user');
    const passInput = document.getElementById('login-pass');
    const info = document.getElementById('attempts-info');
    
    const user = userInput.value.trim();
    const pass = passInput.value.trim();
    
    // Validation
    if (!user || !pass) {
        showToast("⚠️ Please enter username and password", "warning");
        shakeInputs();
        return;
    }
    
    // Check credentials
    if (users[user] === pass) {
        // Success
        enterSystem(user);
    } else {
        // Failed
        handleFailedAttempt(info);
    }
}

function handleFailedAttempt(info) {
    attempts--;
    
    if (attempts > 0) {
        const msg = attempts === 1 
            ? `🚫 Invalid! FINAL WARNING`
            : `🚫 Invalid! ${attempts} attempts left`;
        
        showToast(msg, "error");
        
        info.innerHTML = attempts === 1 
            ? `<span style="color:var(--danger)">⚠️ FINAL WARNING: Last attempt!</span>`
            : `Attempts remaining: ${attempts}`;
        
        shakeInputs();
        
    } else {
        blockSystem(info);
    }
}

function blockSystem(info) {
    isBlocked = true;
    
    info.innerHTML = `<span style="color:var(--warning)">🔒 SECURITY ALERT: Contacting Administration...</span>`;
    
    showToast("🔒 ACCESS DENIED: Redirecting...", "blocked");
    
    // Disable inputs
    document.getElementById('login-user').disabled = true;
    document.getElementById('login-pass').disabled = true;
    document.getElementById('login-btn').disabled = true;
    
    // Redirect
    setTimeout(() => {
        const msg = encodeURIComponent(
            `🚨 ARISE TECH SECURITY ALERT 🚨\n\n` +
            `Unauthorized access attempt!\n` +
            `Time: ${new Date().toUTCString()}\n` +
            `Device: ${navigator.platform}\n` +
            `Browser: ${navigator.userAgent.split(')')[0]})`
        );
        
        window.location.href = `https://wa.me/${CONFIG.WHATSAPP.EGYPT}?text=${msg}`;
    }, 2000);
}

function showToast(message, type) {
    const alertBox = document.getElementById('security-alert');
    if (!alertBox) return;
    
    alertBox.innerText = message;
    alertBox.className = 'security-toast toast-active';
    
    // Colors
    if (type === "warning") {
        alertBox.style.background = "linear-gradient(135deg, #ffaa00, #cc8800)";
    } else if (type === "blocked") {
        alertBox.style.background = "linear-gradient(135deg, #333, #000)";
        alertBox.style.border = "2px solid var(--danger)";
    } else {
        alertBox.style.background = "linear-gradient(135deg, var(--danger), #cc0000)";
    }
    
    setTimeout(() => {
        alertBox.classList.remove('toast-active');
    }, 3000);
}

function shakeInputs() {
    const user = document.getElementById('login-user');
    const pass = document.getElementById('login-pass');
    
    [user, pass].forEach(input => {
        input.style.animation = 'shake 0.5s';
        setTimeout(() => input.style.animation = '', 500);
    });
}

// ===== ENTER SYSTEM =====
function enterSystem(user) {
    console.log(`✅ User ${user} entering system`);
    
    currentUser = user;
    sessionStorage.setItem('arise_current_user', user);
    
    // Init user data
    if (!userData[user]) {
        userData[user] = { xp: 0, level: 1, history: [] };
    }
    
    // Firebase sync for owner
    if (user === CONFIG.ADMIN_NAME && db) {
        syncWithFirebase(user);
    }
    
    // Switch screens
    showScreen('main-screen');
    
    // Update UI
    updateUI();
    
    // Init editor with delay to ensure DOM ready
    setTimeout(initEditor, 300);
    
    saveData();
}

function syncWithFirebase(user) {
    try {
        db.ref('users/' + user).set({
            xp: userData[user].xp,
            level: userData[user].level,
            lastLogin: new Date().toISOString(),
            status: 'online'
        });
        
        db.ref('users/' + user + '/xp').on('value', (snap) => {
            const xp = snap.val();
            if (xp !== null && xp !== userData[user].xp) {
                userData[user].xp = xp;
                const el = document.getElementById('display-xp');
                if (el) el.innerText = xp;
            }
        });
    } catch (e) {
        console.warn("Firebase sync error:", e);
    }
}

// ===== CODE EXECUTION =====
async function runCode() {
    if (!isEditorReady) {
        alert("⏳ Editor still loading... Please wait");
        return;
    }
    
    if (!isPyodideReady) {
        alert("⏳ Python engine loading... Please wait");
        return;
    }
    
    const code = editor.getValue();
    const outputEl = document.getElementById('output');
    const mentorMsg = document.getElementById('mentor-msg');
    const errorAnalysis = document.getElementById('error-analysis');
    const waLink = document.getElementById('wa-link');
    
    // Admin trigger
    if (code.includes("print(song.arise)") || code.includes('print("song.arise")')) {
        if (currentUser === CONFIG.ADMIN_NAME) {
            openAdmin();
        } else {
            outputEl.innerHTML = '<span style="color:var(--danger)">⛔ ACCESS DENIED: Owner privileges required</span>';
            outputEl.className = 'output-error';
        }
        return;
    }
    
    // Add to history
    addToHistory(code);
    
    // Execute
    try {
        pyodide.runPython(`
            import sys
            import io
            sys.stdout = io.StringIO()
            sys.stderr = io.StringIO()
        `);
        
        await pyodide.runPythonAsync(code);
        
        const stdout = pyodide.runPython("sys.stdout.getvalue()");
        const result = stdout || "✅ Code executed successfully (no output)";
        
        outputEl.innerText = result;
        outputEl.className = 'output-success';
        
        mentorMsg.innerHTML = `
            <div style="color:var(--success); margin-bottom:8px; font-weight:bold;">✅ Success!</div>
            <div>Great job! Your code ran perfectly. +${CONFIG.XP_PER_RUN} XP</div>
        `;
        
        if (errorAnalysis) errorAnalysis.style.display = 'none';
        if (waLink) waLink.style.display = 'none';
        
        addXP(CONFIG.XP_PER_RUN);
        
    } catch (err) {
        const errorStr = err.toString();
        
        outputEl.innerText = errorStr;
        outputEl.className = 'output-error';
        
        const errorInfo = parseError(errorStr);
        
        mentorMsg.innerHTML = `
            <div style="color:var(--danger); margin-bottom:8px; font-weight:bold;">⚠️ Error Detected</div>
            <div>${getErrorExplanation(errorInfo.type)}</div>
        `;
        
        const lineEl = document.getElementById('error-line');
        const typeEl = document.getElementById('error-type');
        
        if (lineEl) lineEl.innerText = `Line: ${errorInfo.line}`;
        if (typeEl) typeEl.innerText = `Type: ${errorInfo.type}`;
        if (errorAnalysis) errorAnalysis.style.display = 'block';
        
        // Support link
        const msg = encodeURIComponent(
            `🆘 Support Request - Arise Tech\n\n` +
            `User: ${currentUser}\n` +
            `Level: ${userData[currentUser]?.level || 1}\n` +
            `Error: ${errorInfo.type} (Line ${errorInfo.line})\n\n` +
            `Code:\n\`\`\`\n${code}\n\`\`\``
        );
        
        if (waLink) {
            waLink.href = `https://wa.me/${CONFIG.WHATSAPP.EGYPT}?text=${msg}`;
            waLink.style.display = 'flex';
        }
    }
}

function parseError(errorStr) {
    const lineMatch = errorStr.match(/line (\d+)/);
    const typeMatch = errorStr.match(/(\w+Error):/);
    
    return {
        line: lineMatch ? lineMatch[1] : 'Unknown',
        type: typeMatch ? typeMatch[1] : 'Error',
        full: errorStr
    };
}

function getErrorExplanation(type) {
    const explanations = {
        'SyntaxError': 'Syntax error. Check brackets, colons, and spelling.',
        'IndentationError': 'Indentation error. Ensure consistent spacing.',
        'NameError': 'Undefined variable or function. Check your spelling.',
        'TypeError': 'Data type mismatch. Check your operations.',
        'ValueError': 'Invalid value for this operation.',
        'IndexError': 'Index out of range.',
        'KeyError': 'Key not found in dictionary.',
        'ZeroDivisionError': 'Cannot divide by zero!',
        'AttributeError': 'Object does not have this attribute.',
        'ImportError': 'Failed to import module.',
        'ModuleNotFoundError': 'Module not found.'
    };
    return explanations[type] || 'An unexpected error occurred.';
}

// ===== XP SYSTEM =====
function addXP(amount) {
    if (!currentUser || !userData[currentUser]) return;
    
    const oldLevel = userData[currentUser].level;
    userData[currentUser].xp += amount;
    
    const newLevel = Math.floor(userData[currentUser].xp / CONFIG.XP_PER_LEVEL) + 1;
    
    if (newLevel > oldLevel) {
        userData[currentUser].level = newLevel;
        showLevelUp(newLevel);
        
        if (currentUser === CONFIG.ADMIN_NAME && db) {
            db.ref('users/' + currentUser + '/level').set(newLevel);
        }
    }
    
    updateUI();
    saveData();
}

function showLevelUp(level) {
    const notif = document.getElementById('levelup-notif');
    const text = document.getElementById('levelup-text');
    
    if (text) text.innerText = `You reached Level ${level}!`;
    if (notif) notif.style.display = 'block';
    
    const levelEl = document.getElementById('display-level');
    if (levelEl) {
        levelEl.classList.add('level-up');
        setTimeout(() => levelEl.classList.remove('level-up'), 1000);
    }
    
    setTimeout(() => {
        if (notif) notif.style.display = 'none';
    }, 3000);
}

// ===== HISTORY =====
function addToHistory(code) {
    if (!currentUser || !userData[currentUser]) return;
    
    const history = userData[currentUser].history || [];
    
    history.unshift({
        code: code.substring(0, 100) + (code.length > 100 ? '...' : ''),
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        fullCode: code
    });
    
    if (history.length > CONFIG.MAX_HISTORY) history.pop();
    
    userData[currentUser].history = history;
    updateHistoryUI();
    saveData();
}

function updateHistoryUI() {
    const container = document.getElementById('history-list');
    if (!container) return;
    
    const history = userData[currentUser]?.history || [];
    
    if (history.length === 0) {
        container.innerHTML = '<div style="color:#666; text-align:center; padding:20px;">No history yet</div>';
        return;
    }
    
    container.innerHTML = history.map((item, index) => `
        <div class="history-item" onclick="loadHistory(${index})">
            <div style="word-break:break-word;">${escapeHtml(item.code)}</div>
            <div style="color:#666; font-size:11px; margin-top:5px;">${item.time}</div>
        </div>
    `).join('');
}

function loadHistory(index) {
    const history = userData[currentUser]?.history || [];
    if (!history[index] || !editor) return;
    
    editor.setValue(history[index].fullCode);
    
    // Scroll on mobile
    if (window.innerWidth < 768) {
        document.getElementById('editor-container')?.scrollIntoView({ behavior: 'smooth' });
    }
}

// ===== ADMIN PANEL =====
function openAdmin() {
    const overlay = document.getElementById('admin-overlay');
    const panel = document.getElementById('admin-panel');
    
    if (overlay) overlay.style.display = 'block';
    if (panel) panel.style.display = 'block';
    
    updateUserList();
}

function closeAdmin() {
    const overlay = document.getElementById('admin-overlay');
    const panel = document.getElementById('admin-panel');
    
    if (overlay) overlay.style.display = 'none';
    if (panel) panel.style.display = 'none';
}

function addUser() {
    const userInput = document.getElementById('new-username');
    const passInput = document.getElementById('new-password');
    const roleSelect = document.getElementById('new-role');
    
    const username = userInput?.value?.trim();
    const password = passInput?.value?.trim();
    const role = roleSelect?.value || 'user';
    
    // Validation
    if (!username || !password) {
        alert("⚠️ Please fill in all fields");
        return;
    }
    
    if (username.length < 3) {
        alert("⚠️ Username must be at least 3 characters");
        return;
    }
    
    if (password.length < 4) {
        alert("⚠️ Password must be at least 4 characters");
        return;
    }
    
    if (users[username]) {
        alert("⚠️ Username already exists!");
        return;
    }
    
    // Add user
    users[username] = password;
    
    // Initialize user data
    userData[username] = {
        xp: 0,
        level: 1,
        history: [],
        role: role,
        createdBy: currentUser,
        createdAt: new Date().toISOString()
    };
    
    saveData();
    
    // Clear inputs
    if (userInput) userInput.value = '';
    if (passInput) passInput.value = '';
    
    updateUserList();
    alert(`✅ User "${username}" added successfully as ${role}`);
}

function updateUserList() {
    const container = document.getElementById('user-list');
    if (!container) return;
    
    const entries = Object.entries(users);
    
    container.innerHTML = entries.map(([user, pass]) => {
        const data = userData[user] || {};
        const role = data.role || (user === CONFIG.ADMIN_NAME ? 'owner' : 
                                   user === CONFIG.SUB_ADMIN ? 'co-admin' : 'user');
        
        const roleIcon = role === 'owner' ? '👑' : 
                        role === 'co-admin' ? '🔧' : '👤';
        
        const roleColor = role === 'owner' ? 'var(--success)' : 
                         role === 'co-admin' ? 'var(--secondary)' : '#888';
        
        return `
            <div class="user-item">
                <div>
                    <div style="font-weight:bold; color:var(--secondary);">${escapeHtml(user)}</div>
                    <div style="font-size:11px; color:#666;">${data.xp || 0} XP • Level ${data.level || 1}</div>
                </div>
                <span style="color:${roleColor}; font-size:12px; font-weight:bold;">
                    ${roleIcon} ${role.toUpperCase()}
                </span>
            </div>
        `;
    }).join('');
}

// ===== UTILITY =====
function checkSession() {
    const saved = sessionStorage.getItem('arise_current_user');
    if (!saved) return;
    
    if (users[saved]) {
        currentUser = saved;
        showScreen('main-screen');
        updateUI();
        setTimeout(initEditor, 500);
    } else {
        sessionStorage.removeItem('arise_current_user');
    }
}

function updateUI() {
    if (!currentUser || !userData[currentUser]) return;
    
    const userEl = document.getElementById('display-username');
    const levelEl = document.getElementById('display-level');
    const xpEl = document.getElementById('display-xp');
    
    if (userEl) userEl.innerText = currentUser;
    if (levelEl) levelEl.innerText = userData[currentUser].level;
    if (xpEl) xpEl.innerText = userData[currentUser].xp;
    
    updateHistoryUI();
}

function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    const target = document.getElementById(screenId);
    if (target) target.classList.add('active');
}

function clearOutput() {
    const output = document.getElementById('output');
    if (output) {
        output.innerText = 'Click "Execute Code" to see results...';
        output.className = '';
    }
}

function logout() {
    // Update Firebase status
    if (currentUser === CONFIG.ADMIN_NAME && db) {
        try {
            db.ref('users/' + currentUser + '/status').set('offline');
        } catch (e) {}
    }
    
    // Clear session
    sessionStorage.removeItem('arise_current_user');
    currentUser = null;
    attempts = CONFIG.MAX_ATTEMPTS;
    isBlocked = false;
    isEditorReady = false;
    
    // Cleanup editor
    if (editor && editor.dispose) {
        try {
            editor.dispose();
        } catch (e) {}
    }
    editor = null;
    
    // Reload
    location.reload();
}

function saveData() {
    try {
        localStorage.setItem('arise_users', JSON.stringify(users));
        localStorage.setItem('arise_userdata', JSON.stringify(userData));
    } catch (e) {
        console.warn("Save error:", e);
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl+Enter to run code
    if (e.ctrlKey && e.key === 'Enter') {
        const mainScreen = document.getElementById('main-screen');
        if (mainScreen?.classList.contains('active')) {
            runCode();
        }
    }
    
    // Escape to close admin
    if (e.key === 'Escape') {
        closeAdmin();
    }
});
