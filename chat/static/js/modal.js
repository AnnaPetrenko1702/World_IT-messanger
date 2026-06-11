
document.addEventListener('DOMContentLoaded', function () {

    const socket = io();

    socket.on('connect', () => {
        console.log('Connected');
    });

    socket.on('disconnect', () => {
        console.log('Disconnected');
    });

    socket.on('joined', (data) => {
        console.log('Вошёл в комнату:', data.room);
    });

    socket.on('error', (data) => {
        console.log('Ошибка:', data.msg);
    });

    // вешаем на все чаты
    document.querySelectorAll('.chat-link').forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();  // останавливаем переход

            const groupId = this.dataset.groupId;  // берём из data-атрибута
            console.log('Clicking chat, groupId:', groupId);

            socket.emit('join_room', { groupId: groupId });  // передаём groupId

            // потом переходим
            window.location.href = this.href;
        });
    });

    if (openModalBtn && createChatArea) {
        openModalBtn.addEventListener('click', function () {
            createChatArea.style.display = 'block';
        });
    }

    if (closeModalBtn && createChatArea) {
        closeModalBtn.addEventListener('click', function () {
            createChatArea.style.display = 'none';
        });
    }

    const searchInput = document.getElementById('chat-search');
    
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


    
    const deleteBtn = document.querySelector('.delete-chat-btn');
    const deleteModal = document.getElementById('delete-confirm-modal');
    const cancelDeleteBtn = document.getElementById('cancel-delete-btn');

    if (deleteBtn && deleteModal) {
        deleteBtn.addEventListener('click', function(event) {
            event.preventDefault();  
            event.stopPropagation(); 
            
            deleteModal.style.display = 'flex'; 
        });
    }

    if (cancelDeleteBtn && deleteModal) {
        cancelDeleteBtn.addEventListener('click', function() {
            deleteModal.style.display = 'none';
        });
    }

    window.addEventListener('click', function(event) {
        if (event.target === deleteModal) {
            deleteModal.style.display = 'none';
        }
    });

});