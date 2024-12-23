async function validateSubmission(){
    // Collect data from input fields
    data = [
        document.getElementById("name").value,
        document.getElementById("age").value,
        document.querySelector('input[name="gender"]:checked')?.value,
        document.getElementById("background story").value,
        document.getElementById("purpose").value,
        document.querySelector('input[name="mood"]:checked')?.value,
        document.getElementById("mood variability").value,
        document.getElementById("imagination").value,
        document.querySelector('input[name="humor"]:checked')?.value,
        document.getElementById("energy").value,
        document.getElementById("empathy").value,
        document.querySelector('input[name="tone"]:checked')?.value,
        document.querySelector('input[name="sensitive topics"]:checked')?.value,
        document.querySelector('input[name="profanity"]:checked')?.value,
        document.querySelector('input[name="response length"]:checked')?.value,
        document.getElementById("sentence complexity").value,
    ]


    // Validate the input values
    for (let i = 0; i < data.length; i++) {
        if(data[i] == "" || data[i] == 0){
            alert("Please fill in all the fields")
            break;
        }
    }

    // Send data as JSON
    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'  // Set JSON content type
        },
        body: JSON.stringify({choices: data})  // Send JSON payload
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