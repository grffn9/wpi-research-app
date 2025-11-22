# Project Group Report - 1

## Team: TeamPy

List team members and their GitHub usernames

* Griffin Munhall, grffn9
* Sandra Akram, SandraAkram356
* Tiffany Semexant, tiffany-t-s
* Devin Orareo, devore002

---
**Course** : CS 3733 - Software Engineering

**Instructor**: Sakire Arslan Ay

----
## 1. Iteration 1 - Summary

 * List the user stories completed in `Iteration-1`. Mention who worked on those user stories. 

Completed User Stories - Iteration 1

* As a Student, I want to create an account and enter my profile information (including GPA, majors, and coursework) so that I can get research positions. - Griffin
* As a Student, I want to log in using my WPI email and password so that I can access my saved information securely. - Griffin
* As a Student, I want to view and edit all my profile details so that I can best reflect my current experiences and interests. - Griffin
* As a Student, I want to browse all available research positions so that I can find positions that best suit my interests. - Tiffany
* As a Faculty, I want to activate my preloaded account and complete my profile information so that I can use the system to post research positions efficiently. - Sandra
* As a Faculty, I want to receive a confirmation email for account activation so that my identity is tied to my account. - Sandra
* As a Faculty, I want to log in using my WPI email and password so that I can access my saved information securely. - Sandra
* As a Faculty, I want to view my account profile information so that I can ensure my information is correct and review it as needed. - Tiffany
* As a Faculty, I want to create one or more undergraduate research positions and enter all required details and qualifications so that students can see and apply for the opportunity. - Devin
* As a Faculty, I want to have administrative privileges to add, update, or remove items from the predefined system lists (e.g., research topics, programming languages) so that my posted opportunities best reflect my research. - Devin

----
## 2. Iteration 1 - Sprint Retrospective

 * Include the outcome of your `Iteration-1 Scrum retrospective meetings`. 
 * Mention the changes the team will be doing to improve itself as a result of the Scrum reflections.

### What Went Well
* We are all very responsive with one another.
* We are willing to take work from each other if someone is struggling.
* We are dividing up the workload quite well.
* We work very well together and meet often for check-ins to ensure everyone is doing well.

### What We Can Improve
* More frequent commits to Git and more pulling to our local repo so that we stay up-to-date with the current code.
* We all agreed to have better backward planning, by which we mean beginning our work sooner, so we are not cramming for the deadline.

### Our Planned Changes for Improvement
1.  Daily Pulls/Commits: We will aim for daily a pull/commit once/day to minimize conflicts.
2.  Start-of-Sprint Planning: We will have more structured time at the beginning of the sprint to frontload work.

----
## 3. Product Backlog refinement

 * Have you made any changes to your `product backlog` after `Iteration-1`? If so, please explain the changes here. 

No, we have made no changes to the product backlog after Iteration 1.

----
## 4. Iteration 2 - Sprint Backlog

Include a draft of your `Iteration-2 sprint backlog`. 
 * List the user stories you plan to complete in `Iteration-2`. Make sure to break down the larger user stories into smaller size stories. Mention the team member(s) who will work on each user story. 
 * Make sure to update the "issues" on your GitHub repo accordingly.  

### Draft Iteration 2 - Sprint Backlog

* As a Faculty, I want to update a student’s application status to "Rejected" so that I can inform the student that they either didn’t meet the qualifications or were not able to be selected at this time. - Devin
    * Update student's application status from pending to rejected
    * Create pop up confirming rejection to prevent miss click
* As a Faculty, I want the system to limit the number of approved students to the maximum team size I specified so that I don’t accidentally hire too many students. - Devin
    * Check max size of research project team
    * Prevent approval of application if it would exceed max size of position
* As a Faculty, I want to approve applications for one or more students so that the selected student(s) is aware that they have been accepted to the research position. - Devin
    * Update student's pending application to approved
    * Prevent Approval off application if project size is at max
    * Create pop up confirming approval to prevent miss click
* As a Faculty, I want to view the full profile and qualifications of a student applicant (including GPA, coursework, and reference status) so that I am able to fully evaluate how qualified they are. - Sandra
    * Add to faculty, create a route to view an applicants details
    * Create html template to view a single applicants details
* As a Faculty, I want to see a list of all students who have applied for my research positions so that I can determine and select the best-suited applicants. - Sandra
    * Add to faculty routes, create a route to view all applicants of a researchPosition
    * Create html template for viewing applicant list where faculty can select a student
* As a Student, I want to view the status of my reference requests (Awaiting approval, Recommended, Not Recommended) so that I can further understand the state of my applications. - Griffin
    * Update the HTML
* As a Student, I want to view the status of all research applications I have submitted (Pending, Approved, Rejected) so that I know how my current applications are being viewed. - Griffin
    * Create My Applications Route
    * Create Template
    * Add Apply Route
    * Update the HTML
* As a Student, I want to provide a faculty reference for a position that requires one. - Tiffany
    * Determine if an Application requires a reference
    * If an Application requires a reference, create way to select a Faculty memeber
    * Ensure that Faculty member options are ones that are registered
* As a Student, I want to submit a short statement of interest with my application so that professors are aware of my intent. - Tiffany
    * Create Application Model
    * Add field to Application to allow short statement
* As a Student, I want to apply to multiple research positions so that I can have the best chances of getting a role. - Griffin
    * Update Student Index Route
    * Create Apply Route
    * Update Student Index Template
* As a Student, I want to select a position to view its full details (including team size, required GPA, and expected coursework) so that I can thoroughly evaluate if I’m qualified and interested before applying. - Tiffany
    * Add the route to view the position
    * Implement the HTML to render the db information