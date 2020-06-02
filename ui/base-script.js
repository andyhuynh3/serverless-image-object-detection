"use strict";

const serverUrl = "%s"

async function uploadImage() {
    // encode input file as base64 string for upload
    let file = document.getElementById("file").files[0];
    let converter = new Promise(function(resolve, reject) {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result
            .toString().replace(/^data:(.*,)?/, ''));
        reader.onerror = (error) => reject(error);
    });
    let encodedString = await converter;

    document.getElementById("file").value = "";

    document.getElementById("state").innerHTML = "Processing file..."

    return fetch(serverUrl + "upload", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({filename: file.name, filebytes: encodedString})
    }).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new HttpError(response);
        }
    })
}

function displayResults(response) {
    let imageElem = document.getElementById("image");
    imageElem.src = "data:image/jpg;base64," + response["output_file_bytes"];
    let predictions = response["prediction"];
    let predictionsElem = document.getElementById("predictions");
    const keys = Object.keys(predictions);
    predictionsElem.innerHTML = ''
    let ul = document.createElement('ul');
    for(let i = 0; i < keys.length; i++) {
        const key = keys[i];
        const data = predictions[key];
        const color = data['color'];
        const confidence = data['confidence'];
        const text = key + " (" + confidence + "%%)"
        const li = document.createElement('li');
        li.style.color = color;
        li.appendChild(document.createTextNode(text));
        ul.appendChild(li)
    }
    predictionsElem.appendChild(ul);
    document.getElementById("state").innerHTML = "Processing complete!"
}

function handler() {
    uploadImage()
        .then(response => displayResults(response))
        .catch(error => {
            alert("Error: " + error);
        })
}

class HttpError extends Error {
    constructor(response) {
        super(`Unsupported file type.`);
        this.name = "HttpError";
        this.response = response;
    }
}
