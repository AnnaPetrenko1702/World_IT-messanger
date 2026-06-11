

// const settingsBtn = document.getElementById('settings-btn');
// const settingsModal = document.getElementById('settings-modal');
// const closeModalBtn = document.getElementById('close-modal-btn');
// const cancelModalBtn = document.getElementById('cancel-modal-btn');
// const saveModalBtn = document.getElementById('save-modal-btn');


// if (settingsBtn && settingsModal) {
//     settingsBtn.addEventListener('click', function() {
//         settingsModal.style.display = 'flex'; 
//     });
// }

// function closeModal() {
//     if (settingsModal) {
//         settingsModal.style.display = 'none';
//     }
// }

// if (closeModalBtn) {
//     closeModalBtn.addEventListener('click', closeModal);
// }

// if (cancelModalBtn) {
//     cancelModalBtn.addEventListener('click', closeModal);
// }



// window.addEventListener('click', function(event) {
//     if (event.target === settingsModal) {
//         closeModal();
//     }
// });
// document.addEventListener("DOMContentLoaded", function () {
//     const openBtn = document.getElementById("open_modal_btn");
//     const closeBtn = document.getElementById("close_modal_btn");
//     const modalArea = document.getElementById("create_chat-area");

//     // Показываем окошко
//     openBtn.addEventListener("click", function () {
//         modalArea.style.display = "block";
//     });

//     // Скрываем окошко
//     closeBtn.addEventListener("click", function () {
//         modalArea.style.display = "none";
//     });
// });
document.addEventListener("DOMContentLoaded", function () {
    
    // ==========================================
    // 1. ЛОГИКА ДЛЯ ОКНА НАСТРОЕК ПРОФИЛЯ
    // ==========================================
    const settingsBtn = document.getElementById('settings-btn');
    const settingsModal = document.getElementById('settings-modal');
    const closeModalBtn = document.getElementById('close-modal-btn');
    const cancelModalBtn = document.getElementById('cancel-modal-btn');

    // Функция закрытия окна настроек
    function closeModal() {
        if (settingsModal) {
            settingsModal.style.display = 'none';
        }
    }

    // Открытие окна настроек
    if (settingsBtn && settingsModal) {
        settingsBtn.addEventListener('click', function() {
            settingsModal.style.display = 'flex'; 
        });
    }

    // Кнопки закрытия окна настроек
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', closeModal);
    }

    if (cancelModalBtn) {
        cancelModalBtn.addEventListener('click', closeModal);
    }

    // Закрытие окна при клике на серую область вокруг него
    window.addEventListener('click', function(event) {
        if (event.target === settingsModal) {
            closeModal();
        }
    });


    // ==========================================
    // 2. ЛОГИКА ДЛЯ ОКНА СОЗДАНИЯ ЧАТА
    // ==========================================
    const openChatBtn = document.getElementById("open_modal_btn");
    const closeChatBtn = document.getElementById("close_modal_btn");
    const chatModalArea = document.getElementById("create_chat-area");

    // Открытие окна создания чата
    if (openChatBtn && chatModalArea) {
        openChatBtn.addEventListener("click", function (event) {
            event.preventDefault(); // Защита от случайной отправки скрытых форм
            chatModalArea.style.display = "block";
        });
    }

    // Закрытие окна создания чата
    if (closeChatBtn && chatModalArea) {
        closeChatBtn.addEventListener("click", function (event) {
            event.preventDefault(); // Защита от перезагрузки страницы
            chatModalArea.style.display = "none";
            
            // Сбрасываем текст в инпуте, если пользователь передумал
            const inputField = chatModalArea.querySelector("input[type='text']");
            if (inputField) {
                inputField.value = "";
            }
        });
    }

});