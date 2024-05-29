document.addEventListener('DOMContentLoaded', function() {
    const submitBtn = document.getElementById('submitBtn');
    const resultBox = document.getElementById('result');

     // Đặt ảnh mặc định khi trang tải
    const defaultImg = document.createElement("img");
    defaultImg.src = "static/logos/vs.png"; // Đường dẫn tới ảnh mặc định
    resultBox.appendChild(defaultImg);

    submitBtn.addEventListener('click', function(event) {
        event.preventDefault();

        const hometeam = document.getElementById('hometeam').value;
        const awayteam = document.getElementById('awayteam').value;

        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                hometeam: hometeam,
                awayteam: awayteam
            })
        })
        .then(response => response.json())
        .then(data => {
            resultBox.innerHTML = ""; // Xóa nội dung cũ

            if (data.error) {
                resultBox.innerHTML = `<p>Error: ${data.error}</p>`;
            } else {
                // Tạo và chèn logo
                if (Array.isArray(data.logo)) {
                    data.logo.forEach(function(logo) {
                        const img = document.createElement("img");
                        img.src = logo;
                        resultBox.appendChild(img);
                    });
                } else {
                    const img = document.createElement("img");
                    img.src = data.logo;
                    resultBox.appendChild(img);
                }

            const predictionText = document.createElement("p");
            predictionText.textContent = `Prediction: ${data.prediction}`;
            resultBox.appendChild(predictionText);

            }
        })
        .catch(error => {
            resultBox.innerHTML = `<p>Error: ${error.message}</p>`;
        });
    });
});

