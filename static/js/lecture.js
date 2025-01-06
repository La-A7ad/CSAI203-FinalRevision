let correctCounter = 0;
const totalQuestions = window.lectureData.totalQuestions;
const answeredQuestions = new Set();

function updateCounter(questionId) {
  if (!answeredQuestions.has(questionId)) {
    correctCounter++;
    answeredQuestions.add(questionId);
    const percentage = Math.round((correctCounter / totalQuestions) * 100);
    document.getElementById('correct-counter').innerText = 
      `Progress: ${correctCounter}/${totalQuestions} (${percentage}%)`;
  }
}

// MCQ Submissions
document.querySelectorAll('.submit-mcq').forEach(button => {
  button.addEventListener('click', function () {
    const questionId = parseInt(this.getAttribute('data-question-id'));
    const lectureId = window.lectureData.lectureId;
    const selectedOptions = Array.from(
      document.querySelectorAll(`#mcq-form-${questionId} input[name="option"]:checked`)
    ).map(input => parseInt(input.value));

    fetch('/check-mcq', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ lecture_id: lectureId, question_id: questionId, selected_options: selectedOptions })
    })
      .then(response => response.json())
      .then(data => {
        const feedback = document.getElementById(`feedback-mcq-${questionId}`);
        feedback.style.display = "block";
        feedback.innerText = data.message;
        feedback.style.color = data.correct ? "green" : "red";
        if (data.correct) {
          updateCounter(questionId);
        }
      });
  });
});

// True/False Submissions
document.querySelectorAll('.submit-tf').forEach(button => {
  button.addEventListener('click', function() {
    const questionId = parseInt(this.getAttribute('data-question-id'));
    const form = document.getElementById(`tf-form-${questionId}`);
    const selectedInput = form.querySelector('input[name="answer"]:checked');
    const feedback = document.getElementById(`feedback-tf-${questionId}`);

    // Input validation
    if (!selectedInput) {
        feedback.style.display = "block";
        feedback.innerText = "Please select an answer";
        feedback.style.color = "red";
        return;
    }

    const lectureId = window.lectureData.lectureId;
    const selectedValue = selectedInput.value === 'true';

    // Disable form during submission
    const disableForm = (disabled) => {
        button.disabled = disabled;
        form.querySelectorAll('input').forEach(input => input.disabled = disabled);
    };
    disableForm(true);

    fetch('/check-tf', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            lecture_id: lectureId,
            question_id: questionId,
            selected_value: selectedValue
        })
    })
    .then(response => response.json())
    .then(data => {
        feedback.style.display = "block";
        feedback.innerText = data.message;
        feedback.style.color = data.correct ? "green" : "red";
        
        if (data.correct) {
            updateCounter(questionId);
            button.style.display = 'none';
        } else {
            disableForm(false);
        }
    })
    .catch(error => {
        feedback.style.display = "block";
        feedback.innerText = "Error submitting answer. Please try again.";
        feedback.style.color = "red";
        disableForm(false);
    });
  });
});