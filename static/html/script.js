

// Function to randomly select a student's name
function rollCall() {
  // Get the list of students from the system
  var students = ["Student 1", "Student 2", "Student 3", "Student 4", "Student 5"];
  // Get a random index from the list of students
  var randomIndex = Math.floor(Math.random() * students.length);
  // Get the selected student's name
  var selectedStudent = students[randomIndex];
  // Display the selected student's name on the screen
  document.getElementById("selected-student").innerHTML = selectedStudent;
}
// Add event listener to the Roll Call button
document.querySelector(".btn").addEventListener("click", rollCall);