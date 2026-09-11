const form = document.getElementById("cookedForm");

form.addEventListener("submit", async function (event) {

    event.preventDefault();

    // Get values from HTML

    const sleep =
        Number(document.getElementById("sleep").value);

    const assignments =
        Number(document.getElementById("assignments").value);

    const examDays =
        Number(document.getElementById("examDays").value);

    const attendance =
        Number(document.getElementById("attendance").value);

    const backlogs =
        Number(document.getElementById("backlogs").value);

    const screenTime =
        Number(document.getElementById("screenTime").value);

    const coffee =
        Number(document.getElementById("coffee").value);


    // Show loading message

    document.getElementById("result").innerHTML =
        "🤖 ANALYZING YOUR ACADEMIC DISASTER... 🔥";


    try {

        // Send data to Python ML model

        const response = await fetch("https://useless-project-rm33.onrender.com/predict", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                sleep: sleep,
                assignments: assignments,
                examDays: examDays,
                attendance: attendance,
                backlogs: backlogs,
                screenTime: screenTime,
                coffee: coffee

            })

        });


        const data = await response.json();


        // Check if Python returned an error

        if (data.error) {

            throw new Error(data.error);

        }


        // Show ML prediction

        document.getElementById("result").innerHTML = `

            <div class="result-box">

                <div class="result-emoji">
                    ${data.emoji}
                </div>

                <h2>${data.level}</h2>

                <div class="score">
                    🔥 Cooked Score: ${data.score}/100
                </div>


                <div class="progress">

                    <div
                        class="progress-bar"
                        style="width: ${data.score}%">
                    </div>

                </div>


                <p>
                    😈 ${data.message}
                </p>


                <h3>
                    🎯 Academic Survival Probability
                </h3>


                <h2>
                    ${data.survival}%
                </h2>


                <button
                    type="button"
                    id="retryBtn">

                    🔄 TRY AGAIN

                </button>

            </div>

        `;


        // Retry button

        document
            .getElementById("retryBtn")
            .addEventListener("click", function () {

                location.reload();

            });


    } catch (error) {

        console.error(error);

        document.getElementById("result").innerHTML = `

            <div class="result-box">

                <h2>⚠️ ERROR</h2>

                <p>
                    AI couldn't judge your academic life. 😭
                </p>

                <p>
                    Make sure app.py is running!
                </p>

            </div>

        `;

    }

});