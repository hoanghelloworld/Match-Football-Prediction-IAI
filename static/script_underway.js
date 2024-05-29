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
        const ht_home = document.getElementById('ht_home').value;
        const ht_away = document.getElementById('ht_away').value;
        const ft_home = document.getElementById('ft_home').value;
        const ft_away = document.getElementById('ft_away').value;
        const hs = document.getElementById('hs').value;
        const as = document.getElementById('as').value;
        const hst = document.getElementById('hst').value;
        const ast = document.getElementById('ast').value;
        const hc = document.getElementById('hc').value;
        const ac = document.getElementById('ac').value;
        const hf = document.getElementById('hf').value;
        const af = document.getElementById('af').value;
        const hy = document.getElementById('hy').value;
        const ay = document.getElementById('ay').value;
        const hr = document.getElementById('hr').value;
        const ar = document.getElementById('ar').value;

        fetch('http://127.0.0.1:5000/predict/underaway', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                hometeam: hometeam,
                awayteam: awayteam,
                ht_home: ht_home,
                ht_away: ht_away,
                ft_home: ft_home,
                ft_away: ft_away,
                hs: hs,
                as: as,
                hst: hst,
                ast: ast,
                hc: hc,
                ac: ac,
                hf: hf,
                af: af,
                hy: hy,
                ay: ay,
                hr: hr,
                ar: ar
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
