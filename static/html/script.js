

// Random Roll Call
const rollCallBtn = document.getElementById('roll-call-btn');
const studentName = document.getElementById('student-name');
const students = ['Alice', 'Bob', 'Charlie', 'David', 'Emily', 'Frank', 'Grace', 'Henry', 'Isabella', 'Jack'];

rollCallBtn.addEventListener('click', () => {
	const randomIndex = Math.floor(Math.random() * students.length);
	studentName.textContent = students[randomIndex];
});

// Adding and Removing Students
const addStudentsInput = document.getElementById('add-students');
const removeStudentsInput = document.getElementById('remove-students');
const totalStudents = document.getElementById('total-students');
let numStudents = students.length;

totalStudents.textContent = numStudents;

document.querySelector('form').addEventListener('submit', (event) => {
	event.preventDefault();
	const numToAdd = parseInt(addStudentsInput.value);
	const numToRemove = parseInt(removeStudentsInput.value);

	if (!isNaN(numToAdd)) {
		for (let i = 0; i < numToAdd; i++) {
			students.push(`Student ${numStudents + 1}`);
			numStudents++;
		}
	}

	if (!isNaN(numToRemove)) {
		students.splice(students.length - numToRemove, numToRemove);
		numStudents -= numToRemove;
	}

	totalStudents.textContent = numStudents;
	addStudentsInput.value = '';
	removeStudentsInput.value = '';
});