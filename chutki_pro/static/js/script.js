document.addEventListener('DOMContentLoaded', function () {
    const micBtn = document.getElementById('MicBtn');
    const siriWaveSection = document.getElementById('SiriWave');
    const siriContainer = document.getElementById('siri-container');
    const ovalSection = document.getElementById('Oval');
    const chatbox = document.getElementById('chatbox');
    const chatBtn = document.getElementById('ChatBtn');
    const chatCanvasBody = document.getElementById('chat-canvas-body');

    // Initialize SiriWave
    const siriWave = new SiriWave({
        container: siriContainer,
        width: 600,
        height: 200,
        style: 'ios9',
        amplitude: 1,
        speed: 0.2,
        frequency: 2
    });

    let recentCommands = [];

    micBtn.addEventListener('click', function () {
        // Show SiriWave and start listening
        siriWaveSection.hidden = false;
        siriWave.start();
        ovalSection.hidden = true;

        // Initialize speech recognition
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
            processCommand(transcript);
            recentCommands.push(transcript);
            updateChatCanvas(transcript);
        };

        recognition.onspeechend = function () {
            siriWave.stop();
            siriWaveSection.hidden = true;
            ovalSection.hidden = false;
            recognition.stop();
            console.log('Speech recognition stopped');
        };

        recognition.onerror = function (event) {
            console.error('Speech recognition error:', event.error);
            siriWave.stop();
            siriWaveSection.hidden = true;
            ovalSection.hidden = false;
        };

        recognition.start();
    });

    chatBtn.addEventListener('click', function () {
        updateChatCanvas();
    });

    function processCommand(command) {
        fetch('/process_command', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ command })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.response);
            alert(data.response);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    function updateChatCanvas(newCommand) {
        chatCanvasBody.innerHTML = '';
        recentCommands.forEach(command => {
            const commandElement = document.createElement('div');
            commandElement.classList.add('receiver_message', 'width-size', 'mb-2');
            commandElement.innerText = command;
            chatCanvasBody.appendChild(commandElement);
        });
    }
});
