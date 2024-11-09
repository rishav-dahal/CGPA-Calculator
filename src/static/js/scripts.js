document.querySelectorAll('[data-modal-toggle]').forEach(button => {
    button.addEventListener('click', () => {
        const modalId = button.getAttribute('data-modal-toggle');
        const modal = document.getElementById(modalId);
        if (modal) modal.classList.toggle('hidden');
    });
});

document.querySelectorAll('[data-modal-hide]').forEach(button => {
    button.addEventListener('click', () => {
        const modalId = button.getAttribute('data-modal-hide');
        const modal = document.getElementById(modalId);
        if (modal) modal.classList.add('hidden');
    });
});

document.getElementById('year').textContent = new Date().getFullYear();