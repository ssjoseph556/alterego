async function prebuilt_handler(){
    selected_persona = document.getElementById('persona').value

    // Send data as JSON
    fetch('/prebuilt', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'  // Set JSON content type
        },
        body: JSON.stringify({persona: selected_persona})  // Send JSON payload
    })
    .then(response => {
            if (response.ok) {
                // Redirect to the chat screen after successful submission
                window.location.href = '/chat';
            } else {
                console.error('Failed to submit persona:', response.statusText);
            }
    })
    .catch(error => console.error('Error:', error));
}