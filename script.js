// ==========================================
// ARISE TECH - NEURAL PLATFORM v4.0
// ==========================================

const firebaseConfig = {
    apiKey: "AIzaSyAz8CIPuN8u_8dTWpF1A6Ab65pz045GSf8",
    databaseURL: "https://arise-tech-system-default-rtdb.firebaseio.com",
    projectId: "arise-tech-system"
};

let db = null;
try {
    if (typeof firebase !== "undefined" && !firebase.apps.length) {
        firebase.initializeApp(firebaseConfig);
    }
    if (typeof firebase !== "undefined") {
        db = firebase.database();
    }
} catch (e) {
    console.error("Firebase Init Error:", e);
}

const CONFIG = {
    ADMIN_NAME: "song.arise",
    SUB_ADMIN: "kiyotaka.ayanokouji",
    DEFAULT_PASS: "1322010",

    MAX_FAILED_ATTEMPTS: 3,
    LOCKOUT_SECONDS: 5,
    LOGIN_RESPONSE_DELAY_MIN: 650,
    LOGIN_RESPONSE_DELAY_MAX: 1100,

    XP_PER_RUN: 20,

    CONTACT_PORTALS: [
        "https://wa.me/201055719273", // النائب
        "https://wa.me/96597805334"   // المؤسس
    ]
};

function getDefaultUsers() {
    return {
        [CONFIG.ADMIN_NAME]: { password: CONFIG.DEFAULT_PASS, role: "owner" },
        [CONFIG.SUB_ADMIN]: { password: CONFIG.DEFAULT_PASS, role: "admin" }
    };
}

function normalizeUsers(rawUsers) {
    const defaults = getDefaultUsers();
    const result = { ...defaults };

    if (!rawUsers || typeof rawUsers !== "object") return result;

    Object.keys(rawUsers).forEach((username) => {
        const value = rawUsers[username];

        if (typeof value === "string") {
            result[username] = {
                password: value,
                role:
                    username === CONFIG.ADMIN_NAME
                        ? "owner"
                        : username === CONFIG.SUB_ADMIN
                        ? "admin"
                        : "user"
            };
        } else if (value && typeof value === "object") {
            result[username] = {
                password: value.password || CONFIG.DEFAULT_PASS,
                role:
                    value.role ||
                    (username === CONFIG.ADMIN_NAME
                        ? "owner"
                        : username === CONFIG.SUB_ADMIN
                        ? "admin"
                        : "user")
            };
        }
    });

    return result;
}

let users = normalizeUsers(JSON.parse(localStorage.getItem("arise_users")));
let userData = JSON.parse(localStorage.getItem("arise_userdata")) || {};

let currentUser = null;
let pyodide = null;
let editor = null;

let pyodideReady = false;
let editorReady = false;
let isRunning = false;
let isLoginBusy = false;

const FAILED_LOGIN_KEY = "arise_failed_login_count";
const LOCKOUT_STATE_KEY = "arise_lockout_state";

function saveUsers() {
    localStorage.setItem("arise_users", JSON.stringify(users));
}

function saveUserData() {
    localStorage.setItem("arise_userdata", JSON.stringify(userData));
}

function ensureUserData(username) {
    if (!userData[username]) {
        userData[username] = {
            xp: 0,
            level: 1,
            history: []
        };
    }

    if (!Array.isArray(userData[username].history)) {
        userData[username].history = [];
    }

    if (typeof userData[username].xp !== "number") {
        userData[username].xp = 0;
    }

    if (typeof userData[username].level !== "number") {
        userData[username].level = Math.floor(userData[username].xp / 100) + 1;
    }
}

function showToast(message, type = "danger") {
    const toast = document.getElementById("security-alert");
    if (!toast) return;

    toast.textContent = message;
    toast.className = "security-toast toast-active";

    if (type === "success") toast.classList.add("toast-success");
    else if (type === "warning") toast.classList.add("toast-warning");
    else toast.classList.add("toast-danger");

    clearTimeout(showToast._timer);
    showToast._timer = setTimeout(() => {
        toast.className = "security-toast";
    }, 3000);
}

function setSystemStatus(text) {
    const el = document.getElementById("system-status");
    if (el) el.textContent = text;
}

function setEditorStatus(text) {
    const el = document.getElementById("editor-status");
    if (el) el.textContent = text;
}

function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

function randomDelay() {
    const min = CONFIG.LOGIN_RESPONSE_DELAY_MIN;
    const max = CONFIG.LOGIN_RESPONSE_DELAY_MAX;
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function getFailedLoginCount() {
    return Number(sessionStorage.getItem(FAILED_LOGIN_KEY) || "0");
}

function setFailedLoginCount(value) {
    sessionStorage.setItem(FAILED_LOGIN_KEY, String(value));
}

function resetFailedLoginCount() {
    sessionStorage.removeItem(FAILED_LOGIN_KEY);
}

function chooseRandomPortal() {
    const portals = CONFIG.CONTACT_PORTALS;
    return portals[Math.floor(Math.random() * portals.length)];
}

function getLockoutState() {
    try {
        return JSON.parse(localStorage.getItem(LOCKOUT_STATE_KEY));
    } catch {
        return null;
    }
}

function clearLockoutState() {
    localStorage.removeItem(LOCKOUT_STATE_KEY);
}

function createLockoutState() {
    const state = {
        redirectUrl: chooseRandomPortal(),
        expiresAt: Date.now() + CONFIG.LOCKOUT_SECONDS * 1000
    };
    localStorage.setItem(LOCKOUT_STATE_KEY, JSON.stringify(state));
    return state;
}

function showLockoutScreen() {
    const screen = document.getElementById("lockout-screen");
    screen.classList.add("active");
}

function hideLockoutScreen() {
    const screen = document.getElementById("lockout-screen");
    screen.classList.remove("active");
}

function startLockoutCountdown(state) {
    showLockoutScreen();

    const countdownEl = document.getElementById("lockout-countdown");
    const subtextEl = document.getElementById("lockout-subtext");

    clearInterval(startLockoutCountdown._timer);

    const tick = () => {
        const remainingMs = state.expiresAt - Date.now();
        const remainingSec = Math.max(0, Math.ceil(remainingMs / 1000));

        countdownEl.textContent = String(remainingSec);
        subtextEl.textContent = "يتم الآن تجهيز التحويل الآمن إلى أحد المسؤولين...";

        if (remainingMs <= 0) {
            clearInterval(startLockoutCountdown._timer);
            clearLockoutState();
            window.location.href = state.redirectUrl;
        }
    };

    tick();
    startLockoutCountdown._timer = setInterval(tick, 200);
}

function maybeResumeLockout() {
    const state = getLockoutState();
    if (!state) return false;

    if (!state.redirectUrl || !state.expiresAt || Date.now() >= state.expiresAt) {
        clearLockoutState();
        return false;
    }

    startLockoutCountdown(state);
    return true;
}

function setLoginBusy(busy) {
    isLoginBusy = busy;
    const btn = document.getElementById("login-btn");
    if (!btn) return;

    btn.disabled = busy;
    btn.innerHTML = busy ? "⏳ VERIFYING..." : "🛡️ VERIFY IDENTITY";
}

function showGenericDeniedMessage() {
    const info = document.getElementById("attempts-info");
    if (!info) return;

    info.classList.remove("blocked");
    info.classList.add("danger");
    info.textContent = "Access denied. Please verify your credentials and try again.";
}

function resetLoginInfoText() {
    const info = document.getElementById("attempts-info");
    if (!info) return;

    info.classList.remove("danger", "blocked");
    info.textContent = "Enter your credentials to access the Neural Platform";
}

function normalizeCommand(code) {
    return String(code || "")
        .replace(/\s+/g, "")
        .replace(/;+$/g, "")
        .trim();
}

function isAdminSecretCommand(code) {
    const normalized = normalizeCommand(code);
    const validCommands = [
        "print(song.arise)",
        'print("song.arise")',
        "print('song.arise')"
    ].map(normalizeCommand);

    return validCommands.includes(normalized);
}

function isPrivilegedUser() {
    if (!currentUser || !users[currentUser]) return false;
    const role = users[currentUser].role;
    return role === "owner" || role === "admin";
}

function enableRunButton() {
    const btn = document.getElementById("run-btn");
    if (!btn) return;

    if (currentUser && pyodideReady && editorReady && !isRunning) {
        btn.disabled = false;
        btn.innerHTML = "▶️ EXECUTE CODE";
    } else if (isRunning) {
        btn.disabled = true;
        btn.innerHTML = "⏳ RUNNING...";
    } else {
        btn.disabled = true;
        btn.innerHTML = "⏳ LOADING SYSTEM...";
    }
}

async function initPyodideEngine() {
    setSystemStatus("⏳ Loading Python engine...");
    try {
        pyodide = await loadPyodide();
        await pyodide.loadPackage("micropip");
        pyodideReady = true;
        setSystemStatus("✅ Python Engine Ready");
        enableRunButton();
    } catch (err) {
        console.error("Pyodide Load Error:", err);
        pyodideReady = false;
        setSystemStatus("❌ Python Engine Failed");
        showToast("Python engine failed to load", "warning");
    }
}

function disposeEditor() {
    try {
        if (editor && typeof editor.dispose === "function") {
            editor.dispose();
        }
    } catch (e) {
        console.warn("Editor dispose warning:", e);
    } finally {
        editor = null;
        editorReady = false;
    }
}

function initEditor() {
    const container = document.getElementById("editor-container");
    if (!container) return;

    disposeEditor();
    container.innerHTML = "";
    setEditorStatus("Loading editor...");
    enableRunButton();

    if (typeof require === "undefined") {
        showFallbackEditor();
        return;
    }

    try {
        require.config({
            paths: {
                vs: "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs"
            }
        });

        require(
            ["vs/editor/editor.main"],
            function () {
                try {
                    container.innerHTML = "";
                    editor = monaco.editor.create(container, {
                        value: '# Arise Tech System\nprint("System Ready")',
                        language: "python",
                        theme: "vs-dark",
                        automaticLayout: true,
                        minimap: { enabled: false },
                        fontSize: 16,
                        scrollBeyondLastLine: false,
                        roundedSelection: true,
                        tabSize: 4,
                        insertSpaces: true
                    });

                    editorReady = true;
                    setEditorStatus("Monaco Editor Ready");
                    enableRunButton();
                } catch (e) {
                    console.error("Monaco Create Error:", e);
                    showFallbackEditor();
                }
            },
            function (e) {
                console.error("Monaco Loader Error:", e);
                showFallbackEditor();
            }
        );
    } catch (err) {
        console.error("Editor Init Error:", err);
        showFallbackEditor();
    }
}

function showFallbackEditor() {
    const container = document.getElementById("editor-container");
    if (!container) return;

    container.innerHTML = "";

    const textarea = document.createElement("textarea");
    textarea.id = "fallback-textarea";
    textarea.spellcheck = false;
    textarea.value = '# Arise Tech System\nprint("System Ready")';

    container.appendChild(textarea);

    editor = {
        getValue: () => textarea.value,
        setValue: (value) => {
            textarea.value = value;
        },
        focus: () => textarea.focus(),
        dispose: () => {}
    };

    editorReady = true;
    setEditorStatus("Fallback Editor Ready");
    enableRunButton();
}

function getEditorValue() {
    if (!editor) return "";
    if (typeof editor.getValue === "function") return editor.getValue();
    return "";
}

function setEditorValue(value) {
    if (!editor) return;
    if (typeof editor.setValue === "function") {
        editor.setValue(value);
    }
}

function focusEditor() {
    if (editor && typeof editor.focus === "function") {
        editor.focus();
    }
}

async function handleLogin() {
    if (isLoginBusy) return;

    const userInput = document.getElementById("login-user");
    const passInput = document.getElementById("login-pass");

    const username = userInput.value.trim();
    const password = passInput.value.trim();

    if (!username || !password) {
        showToast("Please enter username and password", "warning");
        return;
    }

    setLoginBusy(true);
    await sleep(randomDelay());

    const record = users[username];

    if (record && record.password === password) {
        resetFailedLoginCount();
        clearLockoutState();
        resetLoginInfoText();
        showToast("Access granted", "success");
        setLoginBusy(false);
        enterSystem(username);
        return;
    }

    const failedCount = getFailedLoginCount() + 1;
    setFailedLoginCount(failedCount);

    if (failedCount >= CONFIG.MAX_FAILED_ATTEMPTS) {
        setLoginBusy(false);
        const lockout = createLockoutState();
        showToast("Security protocol activated", "warning");
        startLockoutCountdown(lockout);
        return;
    }

    showGenericDeniedMessage();
    showToast("Access denied", "danger");
    setLoginBusy(false);
}

function enterSystem(username) {
    if (!users[username]) {
        sessionStorage.removeItem("arise_current_user");
        return;
    }

    currentUser = username;
    ensureUserData(currentUser);
    saveUserData();

    sessionStorage.setItem("arise_current_user", currentUser);

    hideLockoutScreen();

    document.getElementById("login-screen").classList.remove("active");
    document.getElementById("main-screen").classList.add("active");

    updateUI();
    renderHistory();
    resetMentorPanel();
    clearOutput(false);
    initEditor();
    enableRunButton();

    setTimeout(() => focusEditor(), 200);
}

function logout() {
    sessionStorage.removeItem("arise_current_user");
    currentUser = null;

    closeAdmin();
    disposeEditor();

    document.getElementById("main-screen").classList.remove("active");
    document.getElementById("login-screen").classList.add("active");

    setEditorStatus("Loading...");
    enableRunButton();
    resetMentorPanel();
    resetLoginInfoText();

    showToast("Logged out successfully", "success");
}

function updateUI() {
    ensureUserData(currentUser);

    document.getElementById("display-username").innerText = currentUser || "-";
    document.getElementById("display-level").innerText = userData[currentUser].level;
    document.getElementById("display-xp").innerText = userData[currentUser].xp;
}

function showLevelUp(level) {
    const notif = document.getElementById("levelup-notif");
    const text = document.getElementById("levelup-text");

    text.textContent = `You reached Level ${level}!`;
    notif.style.display = "block";

    clearTimeout(showLevelUp._timer);
    showLevelUp._timer = setTimeout(() => {
        notif.style.display = "none";
    }, 2500);
}

function addXP(amount) {
    ensureUserData(currentUser);

    const oldLevel = userData[currentUser].level;
    userData[currentUser].xp += amount;
    userData[currentUser].level = Math.floor(userData[currentUser].xp / 100) + 1;

    updateUI();
    saveUserData();

    if (userData[currentUser].level > oldLevel) {
        showLevelUp(userData[currentUser].level);
    }
}

function clearOutput(resetMentor = true) {
    const output = document.getElementById("output");
    output.classList.remove("output-error", "output-success");
    output.innerText = 'Click "Execute Code" to see results...';

    const errorBox = document.getElementById("error-analysis");
    errorBox.style.display = "none";

    const wa = document.getElementById("wa-link");
    wa.style.display = "none";
    wa.removeAttribute("href");

    if (resetMentor) {
        resetMentorPanel();
    }
}

function resetMentorPanel() {
    const mentor = document.getElementById("mentor-msg");
    mentor.textContent = "Welcome to Arise Tech. Write Python code and I'll help you fix any errors.";
}

function setMentorMessage(message) {
    const mentor = document.getElementById("mentor-msg");
    mentor.textContent = message;
}

function updateErrorUI(errorText, code) {
    const errorBox = document.getElementById("error-analysis");
    const errorLine = document.getElementById("error-line");
    const errorType = document.getElementById("error-type");
    const waLink = document.getElementById("wa-link");

    const lineMatch = String(errorText).match(/line\s+(\d+)/i);
    const lineNumber = lineMatch ? lineMatch[1] : null;

    let faultyLine = "Could not detect exact line";
    if (lineNumber) {
        const lines = String(code).split("\n");
        const lineIndex = Number(lineNumber) - 1;
        if (lines[lineIndex] !== undefined) {
            faultyLine = `Line ${lineNumber}: ${lines[lineIndex]}`;
        }
    }

    errorLine.textContent = faultyLine;
    errorType.textContent = errorText;
    errorBox.style.display = "block";

    const supportMessage = encodeURIComponent(
        `ARISE TECH SUPPORT\nUser: ${currentUser}\nError: ${errorText}\nCode:\n${code}`
    );
    waLink.href = `${CONFIG.CONTACT_PORTALS[0]}?text=${supportMessage}`;
    waLink.style.display = "flex";
}

function pushHistory(code, output, status = "success") {
    ensureUserData(currentUser);

    const snippet = code.length > 120 ? code.slice(0, 120) + "..." : code;

    userData[currentUser].history.unshift({
        code,
        snippet,
        output,
        status,
        time: new Date().toLocaleString("en-GB")
    });

    userData[currentUser].history = userData[currentUser].history.slice(0, 5);
    saveUserData();
    renderHistory();
}

function renderHistory() {
    const list = document.getElementById("history-list");
    if (!currentUser || !list) return;

    ensureUserData(currentUser);
    const history = userData[currentUser].history || [];

    if (!history.length) {
        list.innerHTML = '<div class="empty-box">No history yet</div>';
        return;
    }

    list.innerHTML = "";

    history.forEach((item) => {
        const card = document.createElement("div");
        card.className = "history-item";

        const statusIcon =
            item.status === "error" ? "❌" :
            item.status === "admin" ? "⚡" :
            "✅";

        card.innerHTML = `
            <div class="history-head">
                <span>${statusIcon}</span>
                <span>${item.time}</span>
            </div>
            <div class="history-code">${escapeHtml(item.snippet)}</div>
        `;

        card.addEventListener("click", () => {
            setEditorValue(item.code);
            focusEditor();
            showToast("Code restored from history", "success");
        });

        list.appendChild(card);
    });
}

function escapeHtml(text) {
    return String(text)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

async function runCode() {
    if (!currentUser) {
        showToast("Please login first", "warning");
        return;
    }

    if (!editorReady || !editor) {
        document.getElementById("output").innerText = "Editor is still loading...";
        return;
    }

    const code = getEditorValue();
    const trimmedCode = code.trim();
    const output = document.getElementById("output");

    if (!trimmedCode) {
        output.classList.remove("output-success");
        output.classList.add("output-error");
        output.innerText = "Please write some Python code first.";
        setMentorMessage("Your editor is empty. Start with something simple like print('Hello').");
        return;
    }

    if (isAdminSecretCommand(trimmedCode)) {
        if (!isPrivilegedUser()) {
            output.classList.remove("output-success");
            output.classList.add("output-error");
            output.innerText = "Command rejected.";
            setMentorMessage("This command is restricted.");
            pushHistory(code, "Command rejected", "error");
            return;
        }

        openAdmin();
        output.classList.remove("output-error");
        output.classList.add("output-success");
        output.innerText = "⚡ COMMAND CENTER UNLOCKED";
        setMentorMessage("Secret command accepted. Admin panel is now open.");
        pushHistory(code, "COMMAND CENTER UNLOCKED", "admin");
        return;
    }

    if (!pyodideReady || !pyodide) {
        output.classList.remove("output-success");
        output.classList.add("output-error");
        output.innerText = "Python engine is still loading. Please wait...";
        return;
    }

    isRunning = true;
    enableRunButton();

    output.classList.remove("output-error", "output-success");
    output.innerText = "Running...";
    document.getElementById("error-analysis").style.display = "none";
    document.getElementById("wa-link").style.display = "none";

    try {
        await pyodide.runPythonAsync(`
import sys, io
sys.stdout = io.StringIO()
sys.stderr = io.StringIO()
        `);

        await pyodide.runPythonAsync(code);

        const stdout = pyodide.runPython("sys.stdout.getvalue()");
        const stderr = pyodide.runPython("sys.stderr.getvalue()");
        const finalOutput = (stdout || stderr || "Done").trim();

        output.classList.add("output-success");
        output.innerText = finalOutput || "Done";

        setMentorMessage("Execution completed successfully. Good job.");
        pushHistory(code, finalOutput || "Done", "success");
        addXP(CONFIG.XP_PER_RUN);
    } catch (e) {
        const errorText = e && e.toString ? e.toString() : "Unknown error";

        output.classList.add("output-error");
        output.innerText = errorText;

        setMentorMessage("I found an error in your code. Check the highlighted details and try again.");
        updateErrorUI(errorText, code);
        pushHistory(code, errorText, "error");
    } finally {
        isRunning = false;
        enableRunButton();
    }
}

function openAdmin() {
    document.getElementById("admin-overlay").style.display = "block";
    document.getElementById("admin-panel").style.display = "block";
    renderUserList();
}

function closeAdmin() {
    document.getElementById("admin-overlay").style.display = "none";
    document.getElementById("admin-panel").style.display = "none";
}

function addUser() {
    if (!isPrivilegedUser()) {
        showToast("Permission denied", "warning");
        return;
    }

    const usernameInput = document.getElementById("new-username");
    const passwordInput = document.getElementById("new-password");
    const roleInput = document.getElementById("new-role");

    const username = usernameInput.value.trim();
    const password = passwordInput.value.trim();
    const role = roleInput.value;

    if (!username || !password) {
        showToast("Enter username and password", "warning");
        return;
    }

    if (/\s/.test(username)) {
        showToast("Username cannot contain spaces", "warning");
        return;
    }

    if (users[username]) {
        showToast("User already exists", "warning");
        return;
    }

    users[username] = { password, role };
    ensureUserData(username);

    saveUsers();
    saveUserData();
    renderUserList();

    usernameInput.value = "";
    passwordInput.value = "";
    roleInput.value = "user";

    showToast("User added successfully", "success");
}

function deleteUser(username) {
    if (!isPrivilegedUser()) {
        showToast("Permission denied", "warning");
        return;
    }

    if (!users[username]) return;

    if (username === CONFIG.ADMIN_NAME) {
        showToast("Owner account cannot be deleted", "warning");
        return;
    }

    const confirmed = confirm(`Delete user "${username}"?`);
    if (!confirmed) return;

    delete users[username];
    delete userData[username];

    saveUsers();
    saveUserData();
    renderUserList();

    if (currentUser === username) {
        logout();
    }

    showToast("User deleted successfully", "success");
}

function renderUserList() {
    const list = document.getElementById("user-list");
    if (!list) return;

    list.innerHTML = "";

    const usernames = Object.keys(users);

    if (!usernames.length) {
        list.innerHTML = '<div class="empty-box">No users found</div>';
        return;
    }

    usernames.forEach((username) => {
        const item = document.createElement("div");
        item.className = "user-item";

        const left = document.createElement("div");
        left.className = "user-item-info";

        const name = document.createElement("div");
        name.className = "user-item-name";
        name.textContent = username;

        const role = document.createElement("div");
        role.className = "user-item-role";
        role.textContent = users[username].role || "user";

        left.appendChild(name);
        left.appendChild(role);

        const actions = document.createElement("div");
        actions.className = "user-actions";

        if (username !== CONFIG.ADMIN_NAME) {
            const delBtn = document.createElement("button");
            delBtn.type = "button";
            delBtn.className = "btn btn-danger small-btn";
            delBtn.textContent = "Delete";
            delBtn.addEventListener("click", () => deleteUser(username));
            actions.appendChild(delBtn);
        } else {
            const ownerBadge = document.createElement("span");
            ownerBadge.className = "owner-badge";
            ownerBadge.textContent = "OWNER";
            actions.appendChild(ownerBadge);
        }

        item.appendChild(left);
        item.appendChild(actions);
        list.appendChild(item);
    });
}

function bindKeyboardShortcuts() {
    const loginUser = document.getElementById("login-user");
    const loginPass = document.getElementById("login-pass");
    const newUser = document.getElementById("new-username");
    const newPass = document.getElementById("new-password");

    if (loginUser) {
        loginUser.addEventListener("keydown", (e) => {
            if (e.key === "Enter") handleLogin();
        });
    }

    if (loginPass) {
        loginPass.addEventListener("keydown", (e) => {
            if (e.key === "Enter") handleLogin();
        });
    }

    if (newUser) {
        newUser.addEventListener("keydown", (e) => {
            if (e.key === "Enter") addUser();
        });
    }

    if (newPass) {
        newPass.addEventListener("keydown", (e) => {
            if (e.key === "Enter") addUser();
        });
    }
}

window.addEventListener("load", async function () {
    saveUsers();
    bindKeyboardShortcuts();
    resetLoginInfoText();

    await initPyodideEngine();

    if (maybeResumeLockout()) {
        return;
    }

    const savedUser = sessionStorage.getItem("arise_current_user");
    if (savedUser && users[savedUser]) {
        enterSystem(savedUser);
    } else {
        sessionStorage.removeItem("arise_current_user");
    }
});

