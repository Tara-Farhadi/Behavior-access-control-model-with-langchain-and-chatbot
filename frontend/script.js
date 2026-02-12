async function askQuestion() {
    // Get the question from the textarea
    const questionInput = document.getElementById('questionInput');
    const question = questionInput.value.trim();
    
    // Check if question is empty
    if (!question) {
        alert('Please enter a question!');
        return;
    }
    
    // Get elements
    const messagesDiv = document.getElementById('messages');
    const sendButton = document.getElementById('sendButton');
    
    // Display the user's question
    addMessage('question', question);
    
    // Clear input and disable button
    questionInput.value = '';
    sendButton.disabled = true;
    sendButton.textContent = 'Thinking...';
    
    // Show loading message
    const loadingId = addMessage('loading', 'Searching documents and generating answer...');

    
    try {
        // Send question to the API
        const response = await fetch('/qa/invoke', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ input: question })
        });
        
        // Check if request was successful
        if (!response.ok) {
            throw new Error('Failed to get answer');
        }
        
        // Get the answer
        const data = await response.json();
        
        // Remove loading message
        document.getElementById(loadingId).remove();
        
        // Display the answer
        addMessage('answer', data.output);

            
    } catch (error) {
        // Remove loading message
        document.getElementById(loadingId).remove();
        
        // Show error
        addMessage('answer', 'Sorry, something went wrong. Please try again.');
        console.error('Error:', error);
    } finally {
        // Re-enable button
        sendButton.disabled = false;
        sendButton.textContent = 'Ask Question';
    }
}


function addMessage(type, text) {
    const messagesDiv = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    const messageId = 'msg-' + Date.now();
    
    messageDiv.id = messageId;
    messageDiv.className = 'message ' + type;
    messageDiv.textContent = text;
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    
    return messageId;
}


// Allow Enter key to send (Shift+Enter for new line)
document.addEventListener('DOMContentLoaded', function() {
    const textarea = document.getElementById('questionInput');
    textarea.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            askQuestion();
        }
    });
});