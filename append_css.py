with open('static/css/style.css', 'a', encoding='utf-8') as f:
    f.write('''\n
/* ═══════════════════════════════
   PREMIUM ENHANCEMENTS & UNIQUE CSS
═══════════════════════════════ */
.hover-scale {
    transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.3s ease, background-color 0.3s ease;
}

.hover-scale:hover {
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 12px 24px rgba(46, 125, 50, 0.25) !important;
}

.card {
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    transform: translateY(0);
}

.card:hover {
    box-shadow: 0 20px 40px rgba(46, 125, 50, 0.08) !important;
    transform: translateY(-4px);
    border-color: rgba(46, 125, 50, 0.2) !important;
}

.form-control {
    border-radius: 10px;
    border: 2px solid #e2e8f0;
    transition: all 0.3s ease;
    background-color: #f8fafc;
}

.form-control:focus {
    box-shadow: 0 0 0 4px rgba(46, 125, 50, 0.15) !important;
    border-color: #2E7D32 !important;
    background-color: #ffffff !important;
    transform: translateY(-2px);
}

.form-label {
    letter-spacing: 0.5px;
    font-size: 0.9rem;
    text-transform: uppercase;
}

.category-title {
    background: linear-gradient(135deg, var(--accent-primary), #1B5E20);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
''')
