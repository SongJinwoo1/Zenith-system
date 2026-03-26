const config = {
    apiKey: "AIzaSyAz8CIPuN8u_8dTWpF1A6Ab65pz045GSf8",
    databaseURL: "https://arise-tech-system-default-rtdb.firebaseio.com",
    projectId: "arise-tech-system"
};
firebase.initializeApp(config);
const db = firebase.database();
let py = null;

// تحميل بايثون في الخلفية فور فتح الموقع
async function loadPy() {
    py = await loadPyodide();
    console.log("Python Engine Loaded");
}
loadPy();

function handleLogin() {
    const u = document.getElementById('uid').value;
    const p = document.getElementById('pwd').value;
    if(u === "song.arise" && p === "1322010") {
        document.getElementById('login-screen').classList.remove('active');
        document.getElementById('main-system').classList.add('active');
        db.ref('users/song.arise/xp').on('value', s => { document.getElementById('xp-val').innerText = s.val() || 0; });
    } else { alert("Error: Unauthorized Access"); }
}

async function runPython() {
    const code = document.getElementById('editor').value;
    const con = document.getElementById('console');
    const btn = document.getElementById('run-btn');
    
    if(!py) { con.innerText = "> System: Engine Loading... Please wait."; return; }
    
    btn.innerText = "EXECUTING...";
    con.innerText = "> Running script...";
    
    try {
        py.runPython(`import sys, io; sys.stdout = io.StringIO()`);
        await py.runPythonAsync(code);
        let output = py.runPython("sys.stdout.getvalue()");
        con.style.color = "#adff2f";
        con.innerText = output || "> Success (No Output)";
        // زيادة XP فعلياً في السحابة
        db.ref('users/song.arise/xp').transaction(xp => (xp || 0) + 10);
    } catch (err) {
        con.style.color = "#ff4444";
        con.innerText = "> ERROR: " + err + "\n\nنصيحة: تأكد من كتابة الكود بشكل صحيح أو تواصل مع الدعم.";
    }
    btn.innerText = "RUN NEURAL SCRIPT";
}
