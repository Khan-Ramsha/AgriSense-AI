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
                console.log("SessionID: ", sessionId);
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
        if (!sessionId) {
            alert('No active session. Please upload a file first.');
            return;
        }
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
    
        const labelElement = document.createElement('strong');
        labelElement.classList.add('message-label');
        labelElement.textContent = sender === 'user' ? 'User: ' : 'Assistant: ';
    
        const messageContent = document.createElement('span');
        messageContent.classList.add('message-content');
        messageContent.textContent = message;
    
        messageElement.appendChild(labelElement);
        messageElement.appendChild(messageContent);
    
        if (sender === 'assistant') {
            const playButton = document.createElement('button');
            playButton.textContent = '🔊 Play Audio';
            playButton.classList.add('play-audio-btn');
    
            playButton.addEventListener('click', async () => {
                try {
                    playButton.disabled = true;
                    playButton.textContent = '⌛ Loading...';
    
                    const response = await fetch('/text-to-speech', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ text: message })
                    });
    
                    const data = await response.json();
    
                    if (response.ok) {
                        const audio = new Audio(data.audio_url);
                        
                        audio.onerror = () => {
                            console.error('Error loading audio file');
                            playButton.textContent = '❌ Error';
                            playButton.disabled = false;
                        };
    
                        audio.oncanplaythrough = () => {
                            playButton.textContent = '🔊 Play Audio';
                            playButton.disabled = false;
                        };
    
                        await audio.play();//plays the audio
                    } else {
                        throw new Error(data.error || 'Failed to generate audio');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    alert('An error occurred while playing audio');
                    playButton.textContent = '❌ Error';
                } finally {
                    playButton.disabled = false;
                }
            });
    
            messageElement.appendChild(playButton);
        }
    
        chatHistory.appendChild(messageElement);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
    
});