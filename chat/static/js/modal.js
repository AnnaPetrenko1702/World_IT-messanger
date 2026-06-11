
document.addEventListener("DOMContentLoaded", function () {
    
    // ==========================================
    // 1. ЛОГИКА ДЛЯ ОКНА НАСТРОЕК ПРОФИЛЯ
    // ==========================================
    const settingsBtn = document.getElementById('settings-btn');
    const settingsModal = document.getElementById('settings-modal');
    const closeModalBtn = document.getElementById('close-modal-btn');
    const cancelModalBtn = document.getElementById('cancel-modal-btn');
    const searchInput = document.getElementById('chat-search');
    const openChatBtn = document.getElementById("open_modal_btn");
    const closeChatBtn = document.getElementById("close_modal_btn");
    const chatModalArea = document.getElementById("create_chat-area");
    // открытие и закрытие модального окна
    function closeModal() {
        if (settingsModal) {
            settingsModal.style.display = 'none';
        }
    }

    if (settingsBtn && settingsModal) {
        settingsBtn.addEventListener('click', function() {
            settingsModal.style.display = 'flex'; 
        });
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


    // создание чата
    
    if (openChatBtn && chatModalArea) {
        openChatBtn.addEventListener("click", function (event) {
            event.preventDefault(); 
            chatModalArea.style.display = "block";
        });
    }

    if (closeChatBtn && chatModalArea) {
        closeChatBtn.addEventListener("click", function (event) {
            event.preventDefault(); 
            chatModalArea.style.display = "none";
            
            const inputField = chatModalArea.querySelector("input[type='text']");
            if (inputField) {
                inputField.value = "";
            }
        });
    }
    
    // поиск
    if (searchInput) {
        searchInput.addEventListener('input', function () {
            const filter = searchInput.value.toLowerCase();
            
            const chats = document.querySelectorAll('.your_chat');

            chats.forEach(function (chat) {
                const titleElement = chat.querySelector('.chat-title');
                
                if (titleElement) {
                    const chatName = titleElement.textContent.toLowerCase();

                    if (chatName.startsWith(filter)) {
                        chat.style.display = 'flex'; 
                    } else {
                        chat.style.display = 'none'; 
                    }
                }
            });
        });
    }

});