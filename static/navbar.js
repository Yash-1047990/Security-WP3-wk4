//THe code to open the Side navigation barr
$(document).ready(function() {
  $('#menu-toggle').click(function() {
    $('.sidenav').toggleClass('sidenav-open');
    $('.main-content').toggleClass('main-content-open');
    if ($('.main-content').hasClass('main-content-open')) {
      $('.sidenav a').delay(200).fadeTo(400, 1);
    } else {
      $('.sidenav a').css('opacity', 0);

    }
  });
});

//Checks if you are an SLCer and if so adds the management button!
$(document).ready(function(){
  $.ajax({
    url: "/slcer",
    type: "GET",
    success: function(response) {
      console.log('test slcer checkin', response);

      // Check the value of IsSLC
      var isSLC = response.SLCer[0].IsSLC;
       
      // Perform different actions based on the value of IsSLC
      if (isSLC === 1) {
        // Do something if IsSLC is 1
        console.log('IsSLC is 1');
        $('.sidenav').append('<a href="#" id="management-button"> &#9821; Management </a>')
      
      } else if (isSLC === 0) {
        // Do something else if IsSLC is 0
        console.log('IsSLC is 0');

      } else {
        // Handle unexpected value of IsSLC
        console.log('Unexpected value of IsSLC: ' + isSLC);
      }
    }
  });
});

//Show the Create meetings tab
$(document).ready(function() {
  $("#create-meetings-button").click(function() {
    $("#create-meeting-form").show();
    $('.main-content').empty();
  });

  $("#previous-meetings-button, #class-button, #management-button").click(function() {
    $("#create-meeting-form").hide();
  });

  $(document).on('click', '#management-button', function() {
    $("#create-meeting-form").hide();
  });
});

//The Class Code (your brain might melt trying to read this code so beware(this is most definitely my proudest work as coder ))
$(document).ready(function() { 
  $('#class-button').click(function() {  //this is the trigger for when the button is clicked 
    $.ajax({
      url: "/class", //this is the same url as in our route
      method: "GET",
      success: function(response) { //if its a success
        var class_data = response['class'];  //extracts class data server response and stores it in class_data variable.
        var table_body = '';  //creates an empty string for the table body
        $('.main-content').empty();
        //for loop that iterates over the class_data array.
        for (var i = 0; i < class_data.length; i++) {
          //HTML table row opening tag as a string and assigns it to a variable named row.
          var row = '<tr>';
          //appends HTML table data cell containing the value of the ClassName & SLCer key from the current object in the class_data array to the row variable.
          row += '<td>' + class_data[i]['ClassName'] + '</td>';
          row += '<td>' + class_data[i]['SLCer'] + '</td>';
          row += '</tr>';
          table_body += row;
        }
        //This code creates an HTML table string with the table_body contents. 
        //The table also has a header row with column names.
        var table = '<table id="class-table">'; 
        table += '<thead><tr id="non_working_tr"><th>Class Name</th><th>SLCer</th></tr></thead>';
        table += '<tbody>' + table_body + '</tbody></table>';
        //This code sets the HTML contents of the element with the class main-content to the table string. 
        //The table is then displayed on the page.
        $('.main-content #class-table').remove(); //This code removes the old table before appending the new one.
        $('.main-content').append(table); 
       
        //Clicking on the table row to get the students
        $("tr").not('#non_working_tr').on("click", function(){
          var class_name = $(this).find('td:first').text();
          $.ajax({
              url: "/students?class_name=" + class_name, // pass class_name as query parameter
              method: "GET",
              success: function(response) {
                  var student_data = response['students'];
                  var popup_content = '<div id="popup"> <span id="close">&times;</span><h3>Students of ' + class_name + '</h3>';
                  if (student_data.length > 0) {
                      popup_content += '<ul>';
                      for (var i = 0; i < student_data.length; i++) {
                          popup_content += '<li>' + student_data[i]['Name'] + '</li>';
                      }
                      popup_content += '</ul>';
                  } else {
                      popup_content += '<p>There are no students in this class.</p>';
                  }
                  popup_content += '</div>';
                  $('body').append(popup_content);
                  $('#close').on('click', function() {
                      $('#popup').remove();
                  });
              }
          });
          console.log('clicked!!!', class_name)
      });


        $(document).on('click', '#search-button', function() { //This code adds a click event listener to the search button.
          console.log("Search button working");
          var query = $('#search-bar').val();  
          $.ajax({
            url: "/class?q=" + query, //this is the same url as in our route, with the search query added to the query string
            method: "GET",
           
            success: function(response) {
              var class_data = response['class'];
              var table_body = '';
              for (var i = 0; i < class_data.length; i++) {
                var row = '<tr>';
                row += '<td>' + class_data[i]['ClassName'] + '</td>';
                row += '<td>' + class_data[i]['SLCer'] + '</td>';
                row += '</tr>';
                table_body += row;
              }
              var table = '<table id="class-table">';
              table += '<thead><tr id="non_working_tr"><th>Class Name</th><th>SLCer</th></tr></thead>';
              table += '<tbody>' + table_body + '</tbody></table>';
              $('.main-content #class-table').remove(); //This code removes the old table before appending the new one.
              $('.main-content').append(table);

              $("tr").not('#non_working_tr').on("click", function(){
                var class_name = $(this).find('td:first').text();
                $.ajax({
                    url: "/students?class_name=" + class_name, // pass class_name as query parameter
                    method: "GET",
                    success: function(response) {
                        var student_data = response['students'];
                        var popup_content = '<div id="popup"> <span id="close">&times;</span><h3>Students of ' + class_name + '</h3>';
                        if (student_data.length > 0) {
                            popup_content += '<ul>';
                            for (var i = 0; i < student_data.length; i++) {
                                popup_content += '<li>' + student_data[i]['Name'] + '</li>';
                            }
                            popup_content += '</ul>';
                        } else {
                            popup_content += '<p>There are no students in this class.</p>';
                        }
                        popup_content += '</div>';
                        $('body').append(popup_content);
                        $('#close').on('click', function() {
                            $('#popup').remove();
                        });
                    }
                });
                console.log('clicked!!!', class_name)
            });
            },
            
            error: function(error) {
              console.log(error);
            }
          });
        });
      },
      error: function(error) { //error for if it doesn't work
        console.log(error);
      }
    });
  });
});

//Old Meetings 
$(document).ready(function() {
  $('#previous-meetings-button').click(function() {  
    console.log('clicked!!!')
    function fetchPreviousMeetings() {
      $.ajax({
        url: "/previous_meetings", 
        method: "GET",
        success: function(response) {
          var previous_meetings_data = response['previous_meetings'];  
          var table_body = '';
          console.log(previous_meetings_data)
          
          // remove any previous content from the main-content div
          $('.main-content').empty();
          
          // create a table to display the previous meetings
          var table = '<table>';
          table += '<tr><th>Class</th><th>Subject</th><th>Teacher</th><th>Classroom</th><th>Date</th><th>Start Time</th><th>End Time</th><th>Password</th></tr>';
          for (var i = 0; i < previous_meetings_data.length; i++) {
            table += '<tr>';
            table += '<td>' + previous_meetings_data[i]['class'] + '</td>';
            table += '<td>' + previous_meetings_data[i]['subject'] + '</td>';
            table += '<td>' + previous_meetings_data[i]['teacher'] + '</td>';
            table += '<td>' + previous_meetings_data[i]['classroom'] + '</td>';
            table += '<td>' + previous_meetings_data[i]['date'] + '</td>';
            table += '<td>' + previous_meetings_data[i]['start_time'] + '</td>';
            table += '<td>' + previous_meetings_data[i]['end_time'] + '</td>';
            table += '<td>' + previous_meetings_data[i]['Password'] + '</td>';
            table += '</tr>';
          }
          table += '</table>';
          
          // append the table to the main-content div
          $('.main-content').append(table);
        }
      });
    }
    
    // call the function initially to display the data
    fetchPreviousMeetings();
    
    // refresh the data every 30 seconds
    var intervalId = setInterval(fetchPreviousMeetings, 5000);

    // stop the interval when the user clicks another button
    $('#create-meetings-button, #class-button, .logo, .logout-button').click(function() {
      console.log("clicked the buttons again ey!")
      clearInterval(intervalId);
    });
    // do something else when the button is clicked
    $(document).on('click', '#management-button', function() {
      console.log("clicked the buttons again ey!")
      clearInterval(intervalId);
    });
  });
});

//Upcoming Meetinga
$(document).ready(function(){
  function fetchUpcomingMeetings(){
    $.ajax({
      url: '/upcoming_meetings',
      type: 'GET',
      success: function(response){
        console.log('Your upcoming meetings info', response);
        var meetings = response.upcoming_meetings;
        var table = '<table>';
        
        $('.main-content').children().not('.popup-attendance').remove();

        for (var i = 0; i < meetings.length; i++) {
          table += '<tr  id="non_working_tr"><th>Class</th><th>Subject</th><th>Teacher</th><th>Classroom</th><th>Date</th><th>Start Time</th><th>End Time</th><th>Password</th></tr>';
          table += '<tr>';
          table += '<td style="display:none;">' + meetings[i]['meeting_id'] + '</td>';
          table += '<td>' + meetings[i]['class'] + '</td>';
          table += '<td>' + meetings[i]['subject'] + '</td>';
          table += '<td>' + meetings[i]['teacher'] + '</td>';
          table += '<td>' + meetings[i]['classroom'] + '</td>';
          table += '<td>' + meetings[i]['date'] + '</td>';
          table += '<td>' + meetings[i]['start_time'] + '</td>';
          table += '<td>' + meetings[i]['end_time'] + '</td>';
          table += '<td>' + meetings[i]['Password'] + '</td>';
          table += '</tr>';
        }
        table += '</table>';
        // append the table to the main-content div
        $('.main-content').append(table);
        $("tr").not('#non_working_tr').on("click", function() {
          var meeting_id = $(this).find('td:first').text();
          console.log("click tr!", meeting_id)
          var popup = '<div class="popup-attendance"><div class="popup-content-attendance"><div class="close-btn-attendance">&times;</div><h3 class="Attendance-h3">Attendance</h3><div class="present-list"><h4>Present:</h4></div><div class="absent-list"><h4>Absent:</h4></div></div></div>';
          $('.main-content').append(popup);
        
          function fetchAttendance() {
            $.ajax({
              url: "/attendance?meeting_id=" + meeting_id,
              method: 'GET',
              success: function(response) {
                console.log(response);
                var presentList = $('.popup-attendance .present-list');
                var absentList = $('.popup-attendance .absent-list');
                presentList.empty();
                absentList.empty();
                for (var i = 0; i < response.attendance.length; i++) {
                  var student_id = response.attendance[i].student_id;
                  var present = response.attendance[i].present;
                  if (present == 1) {
                    presentList.append('<div>' + student_id + '</div>');
                  } else {
                    absentList.append('<div>' + student_id + '</div>');
                  }
                }
              }
            });
          }
          fetchAttendance();
        
          var intervalID = setInterval(fetchAttendance, 5000);
        
          $('.popup-attendance .close-btn-attendance').on('click', function() {
            clearInterval(intervalID);
            $('.popup-attendance').remove();
          });
          
          $("tr").not('#non_working_tr').on("click", function() {
            clearInterval(intervalID);
            $('.popup-attendance').remove();
          });
        });
      }
    })
  }
  fetchUpcomingMeetings();

  var intervalID = setInterval(fetchUpcomingMeetings, 5000);

  $('#create-meetings-button, #previous-meetings-button, #class-button, .logo, .logout-button').click(function() {
    console.log("clicked the buttons again ey!")
    clearInterval(intervalID);
  });
  // do something else when the button is clicked
  $(document).on('click', '#management-button', function() {
    console.log("clicked the buttons again ey!")
    clearInterval(intervalId);
  });
})

//Get classnames
$(document).ready(function() {
  // Retrieve class options with AJAX
  $.ajax({
    url: "/class_name",
    type: "GET",
    success: function(response) {
      // Add options to class dropdown menu
      $.each(response.className, function(index, value) {
        console.log( value)
        $("#class").append("<option value='" + value.ClassName + "'>" + value.ClassName + "</option>");
      });
    },
  });
});

var new_meeting_data;
//Takes the create meeting data 
function createMeeting() {
  // Extract the values of the input fields
  var class_name = $('#class').val();
  var start_time = $('#start-time-input').val();
  var end_time = $('#end-time-input').val();
  var date = $('#date-input').val();
  var subject = $('#subject-input').val();
  var teacher = $('#teacher-input').val();
  var classroom = $('#classroom-select').val();
  var password = Math.random().toString(36).substring(2, 7);
  console.log(password)

  if (!class_name || !start_time || !end_time || !date || !subject || !teacher || !classroom) {
    alert("Please fill in all the fields");
    return;
  }


  // Create a data object with the meeting information
  new_meeting_data = {
    class_name: class_name,
    start_time: start_time,
    end_time: end_time,
    date: date,
    subject: subject,
    teacher: teacher,
    classroom: classroom,
    password: password 
  };
  return new_meeting_data

}
//Sends the create meeting data to the app.routes!
$(document).ready(function() {
  $('#submit-meeting-button').click(function() {  
    console.log('clicked!!!')
    new_data = createMeeting()
    $.ajax({
      url: '/create_meeting',
      type: 'POST',
      data: JSON.stringify(new_data),
      contentType: 'application/json',
      success: function(response) {
       //creates a popup if succesfull
                                                                               
       var popup = $('<div/>', {
          'class': 'popup-meeting-created',
          text: 'Meeting created'
        });
        $('body').append(popup);   
        popup.delay(1000).fadeOut();
        console.log(response);
      },
      error: function(error) {
        console.log(error);
      }
    }
  )}
  )
}
)

//Management section
$(document).ready(function(){
  $(document).on('click', '#management-button', function() {
    $('.main-content').empty();

  });
})

