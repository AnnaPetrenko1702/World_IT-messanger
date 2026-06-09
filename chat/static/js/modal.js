// static/js/modal.js

const settingsBtn = document.getElementById('settings-btn');
const settingsModal = document.getElementById('settings-modal');
const closeModalBtn = document.getElementById('close-modal-btn');
const cancelModalBtn = document.getElementById('cancel-modal-btn');

// Открываем модалку при нажатии на шестерёнку
if (settingsBtn && settingsModal) {
    settingsBtn.addEventListener('click', function() {
        settingsModal.style.display = 'flex'; 
    });
}

// Функция для закрытия окна
function closeModal() {
    if (settingsModal) {
        settingsModal.style.display = 'none';
    }
}

// Закрываем модалку при нажатии на крестик
if (closeModalBtn) {
    closeModalBtn.addEventListener('click', closeModal);
}

// Закрываем модалку при нажатии на кнопку "Скасувати"
if (cancelModalBtn) {
    cancelModalBtn.addEventListener('click', closeModal);
}

// Закрываем окно, если пользователь кликнул на темную область вокруг окна
window.addEventListener('click', function(event) {
    if (event.target === settingsModal) {
        closeModal();
    }
});