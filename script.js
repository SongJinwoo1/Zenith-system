// 1. تهيئة فايربيز
const firebaseConfig = {
    apiKey: "AIzaSyAz8CIPuN8u_8dTWpF1A6Ab65pz045GSf8",
    databaseURL: "https://arise-tech-system-default-rtdb.firebaseio.com",
    projectId: "arise-tech-system"
};
firebase.initializeApp(firebaseConfig);
const db = firebase.database();

let py;
let editor;

// 2. تحميل المحرر والمحرك
require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs' }});
require(['vs/editor/editor.main'], function() {
    editor = monaco.editor.create(document.getElementById('editor-container'), {
        value: "print('Welcome Master Ayano')\n# اكتب كود بايثون هنا",
        language: 'python', theme: 'vs-dark', automaticLayout: true
    });
});

async function startSystem() {
    py = await loadPyodide();
    document.getElementById('loading').style.display = 'none';
}
startSystem();

// 3. الدخول
function handleLogin() {
    const u = document.getElementById('login-user').value.trim();
    const p = document.getElementById('login-pass').value.trim();
    
    if (u === "song.arise" && p === "1322010") {
        enterMain(u);
    } else {
        db.ref('users/' + u).once('value').then(s => {
            if (s.exists() && s.val().pass === p) enterMain(u);
            else alert("فشل الدخول!");
        });
    }
}

function enterMain(user) {
    document.getElementById('login-screen').classList.remove('active');
    document.getElementById('main-screen').classList.add('active');
    document.getElementById('display-username').innerText = user;
    
    // مراقبة النقاط
    db.ref('users/' + user + '/xp').on('value', s => {
        document.getElementById('display-xp').innerText = s.val() || 0;
    });
}

// 4. تشغيل بايثون
async function runCode() {
    const code = editor.getValue();
    const out = document.getElementById('output');
    const msg = document.getElementById('mentor-msg');
    
    out.classList.remove('output-error');
    out.innerText = "> جاري التنفيذ...";

    try {
        py.runPython(`import sys, io; sys.stdout = io.StringIO()`);
        await py.runPythonAsync(code);
        const result = py.runPython("sys.stdout.getvalue()");
        
        out.innerText = result || "> تم التنفيذ (بدون مخرجات)";
        msg.innerText = "أحسنت! الكود يعمل كما هو مخطط له. تم تحديث نقاطك في السحابة.";
        
        const user = document.getElementById('display-username').innerText;
        db.ref('users/' + user + '/xp').transaction(x => (x || 0) + 10);
    } catch (e) {
        out.innerText = e.message;
        out.classList.add('output-error');
        msg.innerHTML = "هناك خطأ في الكود الخاص بك.. راجع البنية البرمجية أو تواصل مع المبرمج ايانو.";
    }
}
