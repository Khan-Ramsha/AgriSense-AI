document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.getElementById('upload-form');
    const chatForm = document.getElementById('chat-form');
    const fileUploadArea = document.getElementById('file-upload-area');
    const chatArea = document.getElementById('chat-area');
    const chatHistory = document.getElementById('chat-history');

    let sessionId = null;

    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(uploadForm);
        
        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();

            if (response.ok) {
                sessionId = data.session_id;
                fileUploadArea.style.display = 'none';
                chatArea.style.display = 'block';
                addMessageToChat('user', formData.get('query'));
                addMessageToChat('assistant', data.response);
            } else {
                alert(data.error || 'An error occurred');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while uploading');
        }
    });

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const query = document.getElementById('chat-query').value.trim();
        
        if (!query) return;

        addMessageToChat('user', query);
        document.getElementById('chat-query').value = '';

        try {
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query, session_id: sessionId })
            });
            const data = await response.json();

            if (response.ok) {
                addMessageToChat('assistant', data.response);
            } else {
                alert(data.error || 'An error occurred');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while asking a question');
        }
    });

    function addMessageToChat(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('chat-message', `${sender}-message`);
        messageElement.textContent = message;
        chatHistory.appendChild(messageElement);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
});