function testRandomRollCall() {
    // Set up the class list and exclusion list
    const classList = 'Alice\nBob\nCharlie\nDave\nEve';
    const exclusionList = 'Charlie\nDave';
  
    // Set textarea values
    document.getElementById('class-list').value = classList;
    document.getElementById('exclusion-list').value = exclusionList;
  
    // Call rollCall function
    rollCall();
  
    // Get the selected student
    const selectedStudent = document.getElementById('student-name').textContent;
  
    // Check if the selected student is not in the exclusion list
    const notInExclusionList = !exclusionList.includes(selectedStudent);
    if (notInExclusionList) {
      console.log('Test passed: Selected student is not in the exclusion list');
    } else {
      console.log('Test failed: Selected student is in the exclusion list');
    }
  }
  
  testRandomRollCall();
  