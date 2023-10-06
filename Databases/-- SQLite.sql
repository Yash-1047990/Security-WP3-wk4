CREATE TABLE Attendance (
    meeting_id INTEGER,
    student_id INTEGER,
    present BOOLEAN,
    FOREIGN KEY (meeting_id) REFERENCES Meetings(meeting_id),
    FOREIGN KEY (student_id) REFERENCES Students(id)
);