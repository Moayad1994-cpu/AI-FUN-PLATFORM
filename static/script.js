document.addEventListener('DOMContentLoaded', () => {
            const themeToggle = document.getElementById('theme-toggle');
            themeToggle.addEventListener('click', () => {
                document.body.classList.toggle('dark-mode');
                const icon = themeToggle.querySelector('i');
                icon.classList.toggle('fa-moon');
                icon.classList.toggle('fa-sun');
            });
        });

        async function getThought(lang) {
            try {
                const response = await fetch(`/thought/${lang}`);
                const data = await response.json();
                document.getElementById('thought-display').innerText = data.thought;
            } catch (error) {
                console.error('Error fetching thought:', error);
                document.getElementById('thought-display').innerText = 'Error fetching thought.';
            }
        }

        async function getTriviaQuestion(lang) {
            try {
                const response = await fetch(`/trivia_question/${lang}`);
                const data = await response.json();
                if (data.error) {
                    document.getElementById('trivia-result').innerText = data.error;
                    return;
                }
                document.getElementById('trivia-question').innerText = data.question;
                const optionsContainer = document.getElementById('trivia-options');
                optionsContainer.innerHTML = '';
                data.options.forEach((option) => {
                    const button = document.createElement('button');
                    button.innerText = option;
                    button.onclick = () => checkAnswer(data.question_id, option);
                    optionsContainer.appendChild(button);
                });
                document.getElementById('trivia-result').innerText = '';
            } catch (error) {
                console.error('Error fetching trivia question:', error);
                document.getElementById('trivia-result').innerText = 'Error fetching question.';
            }
        }

        async function checkAnswer(questionId, selectedOption) {
            try {
                const response = await fetch('/trivia', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ question_id: questionId, selected_option: selectedOption })
                });
                const data = await response.json();
                const resultText = data.is_correct ? 'Correct!' : `Wrong! The correct answer is: ${data.correct_answer}`;
                document.getElementById('trivia-result').innerText = resultText;
            } catch (error) {
                console.error('Error checking answer:', error);
                document.getElementById('trivia-result').innerText = 'Error checking answer.';
            }
        }