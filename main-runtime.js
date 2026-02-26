// استيراد البيانات من ملف البيانات (الذي سننشئه لاحقاً)
import { apps } from './app-data.js';

// العناصر الأساسية في الواجهة
const grid = document.getElementById('appGrid');
const bTitle = document.getElementById('bTitle');
const bDesc = document.getElementById('bDesc');
const bImg = document.getElementById('bImg');
const bTag = document.getElementById('bTag');

// وظيفة بناء الأيقونات في الشبكة
function initializeSystem() {
    grid.innerHTML = ''; // تنظيف الشبكة أولاً
    
    apps.forEach((app, index) => {
        // إنشاء بطاقة الأداة (App Card)
        const card = document.createElement('div');
        card.className = 'app-card';
        card.innerHTML = `
            <i data-lucide="${app.icon}"></i>
            <span>${app.tag}</span>
        `;

        // إضافة حدث عند مرور الماوس (Hover) لتحديث الـ Banner
        card.addEventListener('mouseenter', () => updateBanner(index));
        
        // إضافة حدث الضغط لفتح الرابط
        card.addEventListener('click', () => {
            window.location.href = app.link;
        });

        grid.appendChild(card);
    });

    // تفعيل أيقونات Lucide بعد رسم العناصر
    lucide.createIcons();
}

// وظيفة تحديث المستطيل العلوي (Banner)
function updateBanner(i) {
    const data = apps[i];
    
    // تأثير التلاشي السريع عند التغيير
    bImg.style.opacity = '0';
    
    setTimeout(() => {
        bTitle.innerText = data.title;
        bDesc.innerText = data.desc;
        bTag.innerText = data.tag;
        bImg.style.backgroundImage = `url('${data.img}')`;
        bImg.style.opacity = '1';
    }, 200);
}

// تشغيل النظام عند التحميل
document.addEventListener('DOMContentLoaded', () => {
    initializeSystem();
    
    // تعيين أول أداة كخلفية افتراضية للـ Banner
    if(apps.length > 0) updateBanner(0);
});
