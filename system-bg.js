// محرك الخلفية الهادئة لنظام Zenith OS
const canvas = document.getElementById('system-bg');
const ctx = canvas.getContext('2d');

let particles = [];

function init() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    particles = [];
    // كثافة أقل قليلاً لراحة العين أثناء العمل
    for (let i = 0; i < 70; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            vx: (Math.random() - 0.5) * 0.3,
            vy: (Math.random() - 0.5) * 0.3,
            size: Math.random() * 1.5 + 0.5,
            color: Math.random() > 0.5 ? '#00f2ff33' : '#bc47ff33' // شفافية 20% (Hex + 33)
        });
    }
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    particles.forEach((p, i) => {
        p.x += p.vx;
        p.y += p.vy;

        if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
        if (p.y < 0 || p.y > canvas.height) p.vy *= -1;

        ctx.fillStyle = p.color;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fill();

        // ربط الجزيئات بخطوط رفيعة جداً
        for (let j = i + 1; j < particles.length; j++) {
            const p2 = particles[j];
            const dist = Math.hypot(p.x - p2.x, p.y - p2.y);
            if (dist < 150) {
                ctx.strokeStyle = `rgba(0, 242, 255, ${0.1 - dist / 1500})`;
                ctx.lineWidth = 0.4;
                ctx.beginPath();
                ctx.moveTo(p.x, p.y);
                ctx.lineTo(p2.x, p2.y);
                ctx.stroke();
            }
        }
    });
    requestAnimationFrame(draw);
}

window.addEventListener('resize', init);
init();
draw();
