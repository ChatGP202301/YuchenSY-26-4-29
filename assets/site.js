/* Express Water Interactive JS */

function toggleLangMenu() {
    const menu = document.getElementById('langMenu');
    menu.classList.toggle('open');
}

// Close menus when clicking outside
document.addEventListener('click', function(e) {
    const langSwitcher = document.querySelector('.lang-switcher');
    if (langSwitcher && !langSwitcher.contains(e.target)) {
        document.getElementById('langMenu').classList.remove('open');
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
    btn.classList.add('active');
    
    document.querySelectorAll('.product-card').forEach(card => {
        if (cat === 'all' || card.getAttribute('data-cat') === cat) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}
