// محرك الجزيئات الرقمي لنظام Zenith
const canvas = document.getElementById('p');
const ctx = canvas.getContext('2d');

let particles = [];
const particleCount = 100; // يمكنك زيادة العدد لزيادة الكثافة

// وظيفة ضبط حجم الكانفاس ليناسب الشاشة (iPad أو Redmi)
function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

// إنشاء الجزيئات بخصائص عشوائية
function createParticles() {
    particles = [];
    for (let i = 0; i < particleCount; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            vx: (Math.random() - 0.5) * 0.5, // السرعة الأفقية
            vy: (Math.random() - 0.5) * 0.5, // السرعة الرأسية
            color: Math.random() > 0.5 ? '#00f2ff' : '#bc47ff' // ألوان النيون الخاصة بك
        });
    }
}

// رسم وتحريك الجزيئات والخطوط
function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    particles.forEach((p, i) => {
        // تحديث الموقع
        p.x += p.vx;
        p.y += p.vy;

        // الارتداد عند حواف الشاشة
        if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
        if (p.y < 0 || p.y > canvas.height) p.vy *= -1;

        // رسم الجزيء
        ctx.fillStyle = p.color;
        ctx.globalAlpha = 0.6;
        ctx.beginPath();
        ctx.arc(p.x, p.y, 1.2, 0, Math.PI * 2);
        ctx.fill();

        // رسم الخطوط المتصلة (الشبكة)
        for (let j = i + 1; j < particles.length; j++) {
            const p2 = particles[j];
            const dist = Math.hypot(p.x - p2.x, p.y - p2.y);

            if (dist < 120) {
                ctx.strokeStyle = p.color;
                ctx.globalAlpha = 1 - dist / 120; // يتلاشى الخط كلما زادت المسافة
                ctx.lineWidth = 0.5;
                ctx.beginPath();
                ctx.moveTo(p.x, p.y);
                ctx.lineTo(p2.x, p2.y);
                ctx.stroke();
            }
        }
    });

    requestAnimationFrame(animate);
}

// تشغيل المحرك
window.addEventListener('resize', () => {
    resize();
    createParticles();
});

resize();
createParticles();
animate();
