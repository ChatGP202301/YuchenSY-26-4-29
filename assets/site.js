/* Express Water Interactive JS */

function toggleLangMenu() {
    const menu = document.getElementById('langMenu');
    if (!menu) return;
    menu.classList.toggle('open');
}

// Close menus when clicking outside
document.addEventListener('click', function(e) {
    const langSwitcher = document.querySelector('.lang-switcher');
    const langMenu = document.getElementById('langMenu');
    if (langSwitcher && langMenu && !langSwitcher.contains(e.target)) {
        langMenu.classList.remove('open');
    }
});

// FAQ Accordion
document.querySelectorAll('.faq-q').forEach(button => {
    button.addEventListener('click', () => {
        const item = button.parentElement;
        item.classList.toggle('open');
    });
});

// Category Filter (for products.html)
function filterCat(cat, btn) {
    document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');
    
    document.querySelectorAll('.product-card').forEach(card => {
        const cardCat = card.getAttribute('data-cat');
        const badge = card.querySelector('.product-cat-badge');
        const badgeText = badge ? badge.textContent.trim() : '';
        if (cat === 'all' || cardCat === cat || badgeText === cat) {
            card.hidden = false;
            card.style.display = '';
        } else {
            card.hidden = true;
        }
    });
}

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        const langMenu = document.getElementById('langMenu');
        const nav = document.querySelector('.nav');
        if (langMenu) langMenu.classList.remove('open');
        if (nav) nav.classList.remove('open');
    }
});
