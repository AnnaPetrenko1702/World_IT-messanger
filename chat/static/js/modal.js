

const settingsBtn = document.getElementById('settings-btn');
const settingsModal = document.getElementById('settings-modal');
const closeModalBtn = document.getElementById('close-modal-btn');
const cancelModalBtn = document.getElementById('cancel-modal-btn');
const saveModalBtn = document.getElementById('save-modal-btn');


if (settingsBtn && settingsModal) {
    settingsBtn.addEventListener('click', function() {
        settingsModal.style.display = 'flex'; 
    });
}

function closeModal() {
    if (settingsModal) {
        settingsModal.style.display = 'none';
    }
}

if (closeModalBtn) {
    closeModalBtn.addEventListener('click', closeModal);
}

if (cancelModalBtn) {
    cancelModalBtn.addEventListener('click', closeModal);
}

window.addEventListener('click', function(event) {
    if (event.target === settingsModal) {
        closeModal();
    }
});