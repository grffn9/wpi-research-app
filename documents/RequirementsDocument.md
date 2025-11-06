# Software Requirements and Use Cases

## Your Project Title
--------
Prepared by:

* `Sandra Akram, Worcester Polytechnic Institute`
* `Griffin Munhall, Worcester Polytechnic Institute`
* `Tiffany Semexant, Worcester Polytechnic Institute`
* `Devin Orareo, Worcester Polytechnic Institute`


---

**Course** : CS 3733 - Software Engineering

**Instructor**: Sakire Arslan Ay

---

## Table of Contents
- [1. Introduction](#1-introduction)
- [2. Requirements Specification](#2-requirements-specification)
  - [2.1 Customer, Users, and Stakeholders](#21-customer-users-and-stakeholders)
  - [2.2 User Stories](#22-user-stories)
  - [2.3 Use Cases](#23-use-cases)
- [3. User Interface](#3-user-interface)
- [4. Product Backlog](#4-product-backlog)
- [4. References](#4-references)
- [Appendix: Grading Rubric](#appendix-grading-rubric)

<a name="revision-history"> </a>

## Document Revision History

| Name | Date | Changes | Version |
| ------ | ------ | --------- | --------- |
|Revision 1 |2024-11-07 |Initial draft | 1.0        |
|Revision 2 |2025-11-06 |Part 1 Update |2.0         |
|      |      |         |         |

----
# 1. Introduction

<t> As a team we are aiming to create an application that will connect WPI undergraduate students looking for research opportunities with WPI faculty that have open research positions. It’s our hope that this application will simplify the research application process for students, and that faculty will also have an easier time hiring qualified students for their research projects. Additionally, the application should make it easier for students to find research opportunities and for faculty to advertise their research opportunities since currently there is no similar application being used. Each user will be able to log into or register their own account, verifying that they are affiliated with WPI. From there, students can view all the available positions including ones that are recommended to them based on their skill set, and they can apply to the positions. Faculty will be able to maintain and add their research positions and confirm or reject student applications.

----
# 2. Requirements Specification

## 2.1 Customer, Users, and Stakeholders

Customer 
-	WPI (Who want to improve communication between faculty and undergraduate students) 

Stakeholders 
-	WPI (who implements and maintains the software) 
-	WPI Faculty (Who want to post and manage research opportunities for undergraduate students)
-	WPI Undergraduate Students (Who want to view and apply for research opportunities)

Users 
-	WPI Faculty
-	WPI Undergraduate Students

----
## 2.2 User Stories
This section will include the user stories you identified for your project. Make sure to write your user stories in the form : 
"As a **[Role]**, I want **[Feature]** so that **[Reason/Benefit]** "

### Student:
-	As a Student, I want to create an account and enter my profile information (including GPA, majors, and coursework) so that I can get research positions.
-	As a Student, I want to log in using my WPI email and password (or SSO) so that I can access my saved information securely.
### Use Case: View Account (Tiffany)
-	As a Student, I want to view and edit all my profile details so that I can best reflect my current experiences and interests.
### Use Case: Applying for a Position (Tifffany)
-	As a Student, I want to browse all available research positions so that I can find positions that best suit my interests.
-	As a Student, I want to select a position to view its full details (including team size, required GPA, and expected coursework) so that I can thoroughly evaluate if I’m qualified and interested before applying.
-	As a Student, I want the system to automatically display a list of recommended research positions, ranked by relevance so that I can efficiently find the best opportunities for me.
-	As a Student, I want to apply to multiple research positions so that I can have the best chances of getting a role.
-	As a Student, I want to submit a short statement of interest with my application so that professors are aware of my intent.
-	As a Student, I want to provide a faculty reference for a position that requires one.
-	Use Case: Status & Withdrawal (Griffin)
-	As a Student, I want to view the status of all research applications I have submitted (Pending, Approved, Rejected) so that I know how my current applications are being viewed.
-	As a Student, I want to view the status of my reference requests (Awaiting approval, Recommended, Not Recommended) so that I can further understand the state of my applications.
-	As a Student, I want to withdraw an application that is still in the "Pending" state so that I can no longer be in the pool of applicants for a position I don’t want.
### Faculty:
-	As a Faculty, I want to activate my preloaded account and complete my profile information so that I can use the system to post research positions efficiently.
-	As a Faculty, I want to receive a confirmation email for account activation so that my identity is tied to my account.
-	As a Faculty, I want to log in using my WPI email and password (or SSO) so that I can access my saved information securely.
-	Use Case: View Account (Griffin)
-	As a Faculty, I want to view my account profile information so that I can ensure my information is correct and review it as needed.
-	As a Faculty, I want to view any recommendation requests I have received directly on my profile page so I can simply and efficiently approve or reject them.
### Use Case: Managing Positions (Sandra)
-	As a Faculty, I want to create one or more undergraduate research positions and enter all required details and qualifications so that students can see and apply for the opportunity.
-	As a Faculty, I want to have administrative privileges to add, update, or remove items from the predefined system lists (e.g., research topics, programming languages) so that my posted opportunities best reflect my research.
### Use Case: Managing Applications (Devin)
-	As a Faculty, I want to see a list of all students who have applied for my research positions so that I can determine and select the best-suited applicants.
-	As a Faculty, I want to view the full profile and qualifications of a student applicant (including GPA, coursework, and reference status) so that I am able to fully evaluate how qualified they are.
-	As a Faculty, I want to approve applications for one or more students so that the selected student(s) is aware that they have been accepted to the research position.
-	As a Faculty, I want the system to limit the number of approved students to the maximum team size I specified so that I don’t accidentally hire too many students.
-	As a Faculty, I want to update a student’s application status to "Rejected" so that I can inform the student that they either didn’t meet the qualifications or were not able to be selected at this time.

----
## 2.3 Use Cases                         
| Use case #                  |   |
| ----------------------------|---|  
| Name                        |  |
| Participating actors        |  |
| Entry condition(s)          |	 |
| Exit condition(s)           |  |
| Flow of events              | |
| Alternative flow of events  | |
| Iteration                   |	1 |

| Use case # 1               |   |
| ---------------------------|---|
| Name              	     | Edit Account |
| Participating actor        | Student |
| Entry condition(s)         | The student is logged in;  |
| Exit condition(s)          | The student’s profile has been updated with the information they provided. |
| Flow of events 	         | 1. The student selects the option to view their profile. 2. The system displays the details of the student’s profile and the option to edit their profile. 3. The student views their profile and selects the option to edit their profile. 4. The system prompts the user to provide the information needed to change the details of their profile. 5. The student enters their new profile information and confirms the information. 6. The system confirms that the profile information has been edited successfully and displays the updated profile information to the user.|
| Alternative flow of events |1. The student may terminate the use case at any step before confirmation. (This will essentially act as the use case “View Profile”) 2. In step 6, the system may not confirm that the profile has been edited successfully. It will then communicate this to the user, and give them the option to try again. |
| Iteration #                | 2 |

                         
| Use case # 2                |   |
| ----------------------------|---|
| Name              		  | Applying for a Position |
| Participating actor         | Student |
| Entry condition(s)          | The student is logged in; Positions are available to be applied to |
| Exit condition(s)           | The selected position has been applied to by the student. |
| Flow of events 	          | 1. The student selects a position to apply to from the available ones listed. 2. The system displays the details of the position and its application requirements, and then prompts the user to enter the required details for the application. 3. The student enters the statement required for the application, then submits it. 4. The system confirms that the necessary information has been completed, and then sends the application to the corresponding faculty member who posted the position. |
| Alternative flow of events  | 1. If in Step 3 the application requires a recommendation from a faculty member, the student will have the option to select a registered faculty member from the system. 2. If the student hadn’t submitted the required information in step 3, then in step 4 the system will tell the user such and give them the opportunity to re-enter the information. 3. The student may terminate this use case at any step before confirmation. |
| Iteration #                 | 2 |

                          
| Use case # 3                |   |
| ----------------------------|---|
| Name                        | Managing Positions |
| Participating actors        | Faculty member |
| Entry condition(s)          |	The user logged into the System and opened the Managing positions page |
| Exit condition(s)           | The selected research position is added/updated to the users profile |
| Flow of events              | 1. The user selects to add a new position 2. The system will prompt the user to enter all required details and qualifications for the position from predefined parameters 3. The user enters the necessary details and submits the new position4. The system saves the position as “open” and makes the position visible to students and shows message “Position is now posted” |
| Alternative flow of events  | 1. In step 1 If the user selects to edit an existing position, the user updates any of the required details and qualifications and saves the changes. Alternatively, the user can delete an existing position. The system will save the position as “closed”, and it will no longer be visible for students. 2. In step 3, if the user selects to edit the predefined list; the system gives the user access to edit, then saves the changes. 3. In step 4 If the user tries to submit but does not fill out the necessary details, the system will allert them to the mistake and they will be able to try again  4. Alternatively, the user may choose to terminate this use case at any step before confirmation |
| Iteration                   |	1 |

                         
| Use case # 4                |   |
| ----------------------------|---|
| Name                        | Managing Recommendation Requests |
| Participating actors        | Faculty member |
| Entry condition(s)          |	The user logged into the System and there are recommendations for the user to review |
| Exit condition(s)           | The selected student's recommendation status is updated, and the student recommendation request is archived  |
| Flow of events              | 1. The user selects a student's recommendation request 2. The system shows the details of the recommendation request 3. The system prompts the user to choose “recommend” or “not recommended” 4. The user chooses the status option and submits their choice 5. The system updates the student's recommended status and archives the request and shows message “recommendation request choice recorded” |
| Alternative flow of events  | 1. In step 4 if the user wants to change the status, the system allows them to change their choice and saves the new choice 2. Alternatively, the user may choose to terminate this use case at any step before Step 4|
| Iteration                   |	3 |


| Use case # 5                |   |
| ----------------------------|---|
| Name                        | Manage Research Applications |
| Participating actors        | Faculty Member(primary) Student(secondary) |
| Entry condition(s)          |	Faculty logs in; open research position exists and students have applied to position |
| Exit condition(s)           | Selected students’ applications are updated to either “accepted” or “rejected” respective to the positions available |
| Flow of events              | 1.	The faculty selects a research position from their list of positions. 2. The system displays a list of all student applicants for the selected position. 3. The faculty selects a student applicant to review. 4. The system displays the student’s full profile, including GPA, coursework, and reference status. 5. The faculty reviews the applicant’s information and chooses to approve or reject the application. 6. The system prompts the faculty to confirm the decision. 7. Faculty confirms the approval or rejection. 8. The system updates the student’s application status accordingly and displays a confirmation message. 9. The system checks that the total number of approved students does not exceed the position’s maximum team size. 10. If within the limit, the system finalizes the approval; if the limit is exceeded, the system displays a warning message and prevents additional approvals. |
| Alternative flow of events  | 1. In Step 9, if approving a student exceeds the maximum team size, the system prevents the approval and displays an error message: “Maximum team size reached. Cannot approve additional students.” 2. In Step 3, if there are no student applications for the selected position, the system displays: “No applications have been submitted for this position.” 3. In Step 4, if the system fails to load a student’s profile, the system displays: “Unable to retrieve student profile. Please try again later.” 4. At any step before confirmation, the faculty may cancel the process, and the system returns to the applicant list without saving any changes.|
| Iteration                   |	1 |

| Use case # 6                |   |
| ----------------------------|---|  
| Name                        |  |
| Participating actors        |  |
| Entry condition(s)          |	 |
| Exit condition(s)           |  |
| Flow of events              | |
| Alternative flow of events  | |
| Iteration                   |	1 |

| Use case # 7                |   |
| ----------------------------|---|  
| Name                        |  |
| Participating actors        |  |
| Entry condition(s)          |	 |
| Exit condition(s)           |  |
| Flow of events              | |
| Alternative flow of events  | |
| Iteration                   |	1 |

----
# 3. User Interface

Here you should include the sketches or mockups for the main parts of the interface.
You may use Figma to design your interface:

  Example image. The image file is in the `./images` directory.
  <kbd>
      <img src="images/figma.jpg"  border="2">
  </kbd>
  
----
# 4. Product Backlog

<a href="https://github.com/WPI-CS3733-2025B/team-teampy/issues"> A Link to our Product Backlog </a>

----
# 5. References

Cite your references here.

For the papers you cite give the authors, the title of the article, the journal name, journal volume number, date of publication and inclusive page numbers. Giving only the URL for the journal is not appropriate.

For the websites, give the title, author (if applicable) and the website URL.

----
----
