document.addEventListener('DOMContentLoaded', function () {

    // ==========================================
    // 1. ИНИЦИАЛИЗАЦИЯ SOCKET.IO
    // ==========================================
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
        console.log('Ошибка сокета:', data.msg);
    });

    // Извлекаем ID комнаты из URL
    const urlParts = window.location.pathname.split('/');
    const GROUP_ID = urlParts[urlParts.length - 1];

    // Находим элементы интерфейса сообщений
    const sendBtn = document.getElementById('send-button');
    const msgInput = document.getElementById('message-input');
    const messagesDisplay = document.getElementById('chat-messages-display');

    // Функция автоматического скролла вниз
    function scrollToBottom() {
        if (messagesDisplay) {
            messagesDisplay.scrollTop = messagesDisplay.scrollHeight;
        }
    }

    // Сразу скроллим вниз при загрузке страницы, если мы внутри чата
    scrollToBottom();

    // ==========================================
    // 2. ЛОГИКА ОТПРАВКИ И ПРИЕМА СООБЩЕНИЙ
    // ==========================================
    // ДОПОЛНЕНО: Добавлена проверка && msgInput. 
    // Если висит окно "Приєднатися", сокет не будет слать join_room и вызывать ошибку доступа.
    if (GROUP_ID && !isNaN(GROUP_ID) && msgInput) {
        
        // Подключаемся к комнате на сервере
        socket.emit('join_room', { groupId: parseInt(GROUP_ID) });

        function SendMessage() {
            const inputValue = msgInput.value.trim();
            if (!inputValue) return;

            // Отправляем сообщение вместе с ID текущей комнаты
            socket.emit('message', { content: inputValue, group_id: GROUP_ID });
            msgInput.value = '';
        }

        // Слушатель клика по кнопке отправки
        sendBtn.addEventListener('click', SendMessage);

        // ДОПОЛНЕНО: Слушатель нажатия клавиши Enter для отправки
        msgInput.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault(); // Предотвращаем перенос строки в input
                SendMessage();
            }
        });
    }

    // Слушаем сервер и выводим сообщения
    socket.on('message', (data) => {
        if (data.group_id == GROUP_ID) {
            console.log(`[Комната ${data.group_id}] Пользователь ${data.username} (ID: ${data.user_id}): ${data.message}`);
            
            // Тут в будущем будет твой код рендеринга сообщения на экран:
            // appendMessageToUI(data); 

            // ДОПОЛНЕНО: Скроллим вниз при получении нового сообщения
            scrollToBottom();
        }
    });

    // ==========================================
    // 3. ПЕРЕХОД ПО ЧАТАМ (ВХОД В КОМНАТУ)
    // ==========================================
    document.querySelectorAll('.chat-link').forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();  // Останавливаем моментальный переход

            const groupId = this.dataset.groupId;  // Берём из data-атрибута
            console.log('Clicking chat, groupId:', groupId);

            socket.emit('join_room', { groupId: groupId });  

            // Перенаправляем пользователя
            window.location.href = this.href;
        });
    });

    // ==========================================
    // 4. МОДАЛЬНОЕ ОКНО СОЗДАНИЯ ЧАТА
    // ==========================================
    const openModalBtn = document.getElementById('open_modal_btn');
    const closeModalBtn = document.getElementById('close_modal_btn');
    const createChatArea = document.getElementById('create_chat-area');

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

    // ==========================================
    // 5. ЖИВОЙ ПОИСК ЧАТОВ
    // ==========================================
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

    // ==========================================
    // 6. МОДАЛЬНОЕ ОКНО УДАЛЕНИЯ ЧАТА
    // ==========================================
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

    // Закрытие окна удаления при клике в пустую область вокруг него
    window.addEventListener('click', function(event) {
        if (event.target === deleteModal) {
            deleteModal.style.display = 'none';
        }
    });

});