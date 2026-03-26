// إعدادات السحابة
const firebaseConfig = {
    apiKey: "AIzaSyAz8CIPuN8u_8dTWpF1A6Ab65pz045GSf8",
    databaseURL: "https://arise-tech-system-default-rtdb.firebaseio.com",
    projectId: "arise-tech-system"
};
firebase.initializeApp(firebaseConfig);
const db = firebase.database();

let py; let editor; let attempts = 3;

// تحميل المحرك في الخلفية (بدون شاشة تحميل معطلة)
async function bootSystem() {
    py = await loadPyodide();
}
bootSystem();

// إعداد المحرر (Monaco)
require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs' }});
require(['vs/editor/editor.main'], function() {
    editor = monaco.editor.create(document.getElementById('editor-container'), {
        value: "# Arise Core Online\nprint('System Ready')",
        language: 'python', theme: 'vs-dark', automaticLayout: true
    });
});

// نظام الدخول والحماية المطور
function handleLogin() {
    const u = document.getElementById('login-user').value.trim();
    const p = document.getElementById('login-pass').value.trim();
    const info = document.getElementById('attempts-info');
    const toast = document.getElementById('security-alert');

    // التحقق من حساب الأدمن المباشر
    if (u === "song.arise" && p === "1322010") {
        enterSystem(u);
        return;
    }

    // لو البيانات غلط
    attempts--;
    info.innerText = `المحاولات المتاحة: ${attempts}`;
    info.style.color = "red";

    if (attempts > 0) {
        showToast("خطأ في البيانات! يرجى التأكد من اسم المستخدم أو كلمة السر.");
    } else {
        // التحويل النهائي عند استنفاد المحاولات
        showToast("لقد لاحظنا أمناً غير اعتيادي.. جاري تحويلك للإدارة.");
        setTimeout(redirectToSupport, 2000);
    }
}

function showToast(msg) {
    const toast = document.getElementById('security-alert');
    toast.innerText = msg;
    toast.classList.add('toast-active');
    setTimeout(() => toast.classList.remove('toast-active'), 3000);
}

function redirectToSupport() {
    // الأرقام المطلوبة (المؤسس والمساعد)
    const links = [
        "https://wa.me/201021484674", // المساعد (المصري)
        "https://wa.me/96555132201"   // المؤسس (الكويتي)
    ];
    // اختيار عشوائي 50/50
    const randomLink = links[Math.floor(Math.random() * links.length)];
    window.location.href = randomLink;
}

function enterSystem(user) {
    document.getElementById('login-screen').classList.remove('active');
    document.getElementById('main-screen').classList.add('active');
    document.getElementById('display-username').innerText = user;
    
    // ربط النقاط بالسحابة
    db.ref('users/' + user + '/xp').on('value', s => {
        document.getElementById('display-xp').innerText = s.val() || 0;
    });
}

async function runCode() {
    if(!py) { alert("النظام ما زال يجمع البيانات.. انتظر ثانية"); return; }
    const out = document.getElementById('output');
    try {
        py.runPython(`import sys, io; sys.stdout = io.StringIO()`);
        await py.runPythonAsync(editor.getValue());
        out.innerText = py.runPython("sys.stdout.getvalue()") || "تم التنفيذ.";
        out.style.color = "#adff2f";
        // زيادة نقاط XP
        const user = document.getElementById('display-username').innerText;
        db.ref('users/' + user + '/xp').transaction(x => (x || 0) + 10);
    } catch (e) {
        out.innerText = "⚠️ خطأ: " + e.message;
        out.style.color = "#ff4444";
    }
}
