import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { getAuth, GoogleAuthProvider, signInWithPopup, signInWithEmailAndPassword, createUserWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";
import { getFirestore, doc, setDoc } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";

// إعدادات Firebase الخاصة بك
const firebaseConfig = {
    apiKey: "AIzaSyC-Vfw10y-xcUL-U-DGhDgoi4oUjlNbpXg",
    authDomain: "zenith-c26ae.firebaseapp.com",
    projectId: "zenith-c26ae",
    storageBucket: "zenith-c26ae.firebasestorage.app",
    messagingSenderId: "146416524485",
    appId: "1:146416524485:web:8aad935153f17f244924ac"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);
const googleProvider = new GoogleAuthProvider();

let isLoginMode = true;

// وظيفة التبديل بين الدخول والتسجيل
window.toggleForm = function() {
    isLoginMode = !isLoginMode;
    document.getElementById('form-title').innerText = isLoginMode ? "ZENITH LOGIN" : "CREATE ACCOUNT";
    document.getElementById('toggle-msg').innerText = isLoginMode ? "Don't have an account?" : "Already have an account?";
    document.getElementById('toggle-btn').innerText = isLoginMode ? "Register Now" : "Login Now";
};

// التعامل مع الدخول/التسجيل اليدوي
window.handleAuth = async function() {
    const email = document.getElementById('user-email').value;
    const pass = document.getElementById('user-pass').value;

    try {
        if (isLoginMode) {
            await signInWithEmailAndPassword(auth, email, pass);
            alert("Welcome back!");
        } else {
            const result = await createUserWithEmailAndPassword(auth, email, pass);
            // حفظ الحساب في قاعدة البيانات (Firestore)
            await setDoc(doc(db, "users", result.user.uid), {
                email: email,
                role: "User",
                createdAt: new Date()
            });
            alert("Account created successfully!");
        }
        window.location.href = "main.html";
    } catch (error) {
        alert("Error: " + error.message);
    }
};

// دخول جوجل
window.loginWithGoogle = async function() {
    try {
        const result = await signInWithPopup(auth, googleProvider);
        await setDoc(doc(db, "users", result.user.uid), {
            name: result.user.displayName,
            email: result.user.email,
            photo: result.user.photoURL
        }, { merge: true });
        window.location.href = "main.html";
    } catch (error) {
        console.error(error);
    }
};
