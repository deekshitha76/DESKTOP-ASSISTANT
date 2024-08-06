document.addEventListener('DOMContentLoaded', function () {
    const chatbox = document.getElementById('chatbox');
    const micBtn = document.getElementById('MicBtn');
    const chatBtn = document.getElementById('ChatBtn');
    const chatCanvasBody = document.getElementById('chat-canvas-body');

    micBtn.addEventListener('click', function () {
        startSpeechRecognition();
    });

    chatBtn.addEventListener('click', function () {
        processCommand(chatbox.value.trim(),'text');
    });

    chatbox.addEventListener('keyup', function (event) {
        if (event.key === 'Enter') {
            processCommand(chatbox.value.trim(),'text');
        }
    });

    function startSpeechRecognition() {
        const recognition = new webkitSpeechRecognition() || new SpeechRecognition();
        recognition.lang = 'en-US';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.onstart = function () {
            console.log('Speech recognition started');
        };

        recognition.onresult = function (event) {
            const transcript = event.results[0][0].transcript.toLowerCase();
            console.log(`User said: ${transcript}`);
            chatbox.value = transcript;
            processCommand(transcript,'voice');
        };

        recognition.onspeechend = function () {
            recognition.stop();
            console.log('Speech recognition stopped');
        };

        recognition.onerror = function (event) {
            console.error('Speech recognition error:', event.error);
        };

        recognition.start();
    }

    function processCommand(command,input_type) {
        if (!command) {
            return;
        }

        const data = { command: command,input_type:input_type };

        fetch('/process_command', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
            .then(response => response.json())
            .then(data => {
                console.log('Response:', data);
                updateChatCanvas(command);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    function updateChatCanvas(command) {
        const commandElement = document.createElement('div');
        commandElement.classList.add('receiver_message', 'width-size', 'mb-2');
        commandElement.innerText = command;
        chatCanvasBody.appendChild(commandElement);

        chatbox.value = '';
    }
});
