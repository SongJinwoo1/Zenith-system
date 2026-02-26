// استيراد أدوات التحقق من Firebase
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { getAuth, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";
import { firebaseConfig } from "./firebase-config.js";

// بدء تشغيل الحارس
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// مراقبة حالة المستخدم بشكل لحظي
onAuthStateChanged(auth, (user) => {
    if (!user) {
        // إذا لم يكن هناك مستخدم مسجل، يتم طرده فوراً لصفحة الدخول
        console.warn("Access Denied: No Active Session.");
        window.location.href = "Login.html";
    } else {
        // تحديث بيانات الملك في الواجهة
        const nameElem = document.getElementById('uName');
        const picElem = document.getElementById('uPic');
        
        if(nameElem) nameElem.innerText = user.displayName || "ZENITH USER";
        if(picElem && user.photoURL) picElem.src = user.photoURL;
        
        console.log("Welcome back,", user.displayName);
    }
});
