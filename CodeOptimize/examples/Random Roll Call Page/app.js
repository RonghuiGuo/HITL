const rollCallBtn = document.getElementById('roll-call-btn');
const rollAgainBtn = document.getElementById('roll-again-btn');
const studentName = document.getElementById('student-name');
const rollCallDisplay = document.getElementById('roll-call-display');

rollCallBtn.addEventListener('click', rollCall);
rollAgainBtn.addEventListener('click', rollAgain);

function rollCall() {
  const classList = document.getElementById('class-list').value.split('\n');
  const exclusionList = document.getElementById('exclusion-list').value.split('\n');
  let filteredClassList = classList.filter(name => !exclusionList.includes(name.trim()));
  let randomIndex = Math.floor(Math.random() * filteredClassList.length);
  let selectedStudent = filteredClassList[randomIndex];
  studentName.textContent = selectedStudent;
  rollCallDisplay.style.display = 'block';
  rollCallBtn.style.display = 'none';
}

function rollAgain() {
  const classList = document.getElementById('class-list').value.split('\n');
  const exclusionList = document.getElementById('exclusion-list').value.split('\n');
  let filteredClassList = classList.filter(name => !exclusionList.includes(name.trim()));
  let randomIndex = Math.floor(Math.random() * filteredClassList.length);
  let selectedStudent = filteredClassList[randomIndex];
  studentName.textContent = selectedStudent;
}
