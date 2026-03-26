// إعدادات فايربيز الرسمية من مشروعك
const firebaseConfig = {
    apiKey: "AIzaSyAz8CIPuN8u_8dTWpF1A6Ab65pz045GSf8",
    databaseURL: "https://arise-tech-system-default-rtdb.firebaseio.com",
    projectId: "arise-tech-system"
};

firebase.initializeApp(firebaseConfig);
const db = firebase.database();

// دالة الدخول الذكية
function handleLogin() {
    const user = document.getElementById('username').value.trim();
    const pass = document.getElementById('password').value.trim();
    const status = document.getElementById('status-msg');

    status.innerText = "Verifying Credentials...";

    // التحقق من حساب المالك
    if (user === "song.arise" && pass === "1322010") {
        initSession(user);
    } else {
        // التحقق من بقية المستخدمين في السحابة
        db.ref('users/' + user).once('value').then(snap => {
            if (snap.exists() && snap.val().pass === pass) {
                initSession(user);
            } else {
                status.innerText = "ACCESS DENIED ❌";
                status.style.color = "red";
            }
        });
    }
}

function initSession(userId) {
    document.getElementById('login-screen').classList.remove('active');
    document.getElementById('main-system').classList.add('active');
    
    // مراقبة الـ XP من السحابة مباشرة
    db.ref('users/' + userId + '/xp').on('value', snap => {
        document.getElementById('xp-count').innerText = snap.val() || 0;
    });
}

function executeSystemCode() {
    const code = document.getElementById('code-editor').value;
    const output = document.getElementById('terminal-output');
    
    output.innerHTML += `<br>> Executing Logic...`;
    
    // محاكاة التنفيذ وزيادة الـ XP في السحابة
    if(code.length > 5) {
        const user = "song.arise"; // للتجربة
        db.ref('users/' + user + '/xp').transaction(xp => (xp || 0) + 10);
        output.innerHTML += `<br><span style="color:#00ff00">> Success: Cloud Sync Complete +10 XP</span>`;
    }
}
