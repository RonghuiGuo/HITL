

const numStudents = document.getElementById("numStudents");
const rollCallBtn = document.getElementById("rollCallBtn");
const selectedStudent = document.getElementById("selectedStudent");

let students = ["John", "Jane", "Bob", "Sue", "Mike", "Lisa", "Tom", "Mary", "David", "Karen", "Chris", "Amy", "Mark", "Julie", "Steve", "Emily", "Paul", "Anna", "Eric", "Megan"];

rollCallBtn.addEventListener("click", function() {
	let randomIndex = Math.floor(Math.random() * students.length);
	selectedStudent.textContent = students[randomIndex];
});

// Adding and Removing Students
// Not implemented in this version

// Exclusion List
// Not implemented in this version