# Project Design Document
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
- [2. Software Design](#2-software-design)
- [2.1 Database Model](#21-model)
- [2.2 Modules and Interfaces](#22-modules-and-interfaces)
- [2.2.1 Overview](#221-overview)
- [2.2.2 Interfaces](#222-interfaces)
- [2.3 User Interface Design](#23-view-and-user-interface-design)
- [3. References](#3-references)
- [Appendix: Grading Rubric](#appendix-grading-rubric)
<a name="revision-history"> </a>
### Document Revision History
| Name | Date | Changes | Version |
| ------ | ------ | --------- | --------- |
|Revision 1 |2025-11-14 |Initial draft | 1.0 |
|           |           |              |     |


# 1. Introduction
TThis document outlines the high-level design of the application’s backend architecture and user interface. Its purpose is to clearly define the system’s data model, software modules, and external interfaces prior to implementation. Section 2.1 provides a detailed description of the database schema, including all SQLAlchemy models, their roles, and an accompanying UML diagram that illustrates the relationships among tables. Section 2.2 describes the major software modules and blueprints, explains how they interact within the system architecture, and specifies the routes and interfaces that each module exposes. Finally, Section 2.3 presents initial user interface designs for the primary user workflows, including student and faculty interactions with positions, applications, and profile management. Together, these components establish a cohesive blueprint for the application’s functionality and guide the development of a consistent, scalable system.
# 2. Software Design

## 2.1 Database Model
Provide a list of your tables (i.e., SQL Alchemy classes) in your
database model and briefly explain the role of each table.
Provide a UML diagram of your database model showing the
associations and relationships among tables.

| Model | Role |
|-------|------|
| User | Defines shared database model for both student and faculty |
| Student  | represents student user |
| Faculty | represents faculty user|
| Application | Tracks application status and decision | 
| Position | Contains requirements for research positions |
| AdvancedCourses | Upper level courses needed for some positions and can be displayed on student profiles |
| Programming Languages | programming languages needed for student/faculty profiles and psoitions
| ResearchTopics | research topics for student interest and position topics |
| Major | academic major for stuident major, facult domain and psition requirements
| Grades | grades needed for position criteria 
| Courses | Courses taken by students and potential position criteria

Database UML diagram :
<kbd>
      <img src="images/dbUML.png"  border="2">
</kbd>


## 2.2 Modules and Interfaces
### 2.2.1 Overview
Describe the high-level architecture of your software: i.e., the
major modules/blueprints and how they fit together. Provide a UML
component diagram that illustrates the architecture of your
software. Briefly mention the role of each module in your
architectural design. Please refer to the "System Level Design"
lectures in Week 4.

| Model | Role |
|-------|------|
| Models | Defines Shared database models|
| Student  | Manages student specific routes and logic |
| Faculty | Manages faculty specific routes and logic|
| Auth | Handles user authentication, login, and registration |
| Error Handlers | Manages invalid requests or exceptions |

System UML Diagram:
<kbd>
      <img src="images/systemUML.png"  border="2">
</kbd>



### 2.2.2 Interfaces
Include a detailed description of the routes your application
will implement.
* Brainstorm with your team members and identify all routes you
need to implement for the **completed** application.
* For each route specify its , , and .
* You can use the following table template to list your route
specifications.
* Organize this section according to your module decomposition,
i.e., include a sub-section for each module/blueprint and list
all routes for that sub-section in a table.
#### 2.2.2.1 \<Auth> Routes
| | Methods | URL Path | Description |
|:--|:------------------|:-----------|:-------------|
|1.|GET,POST|/student/register|resgisters a new student user|
|2.|GET,POST|/faculty/activation|activates a premade faculty account |
|3.|GET,POST|/user/login|logs a user in (student or faculty)|
|4.|GET,POST|/user/logout |logs a user out of the system(student and faculty)|

#### 2.2.2.2 \<Main/student> Routes
| | Methods | URL Path | Description |
|:--|:------------------|:-----------|:-------------|
|1. |GET |/student/index |homepage for student user |
|2. |GET |/student/position/<position_id>/details |view the details of a position |
|3. |POST |/student/position/<position_id>/apply | apply for a position |
|4. |GET |/student/position/<position_id>/<application_id>/view |view an application status |
|5. |GET |/student/profile/view |view your student profile |
|6. |GET,POST |/student/editprofile |edit your student profile |

#### 2.2.2.3 \<Main/faculty> Routes
| | Methods | URL Path | Description |
|:--|:------------------|:-----------|:-------------|
|1. |GET |/faculty/index |faculty user home page |
|2. |GET,POST |/faculty/position/create |create a new position |
|3. |GET |/faculty/profile |view profile |
|4. |GET |/faculty/position/<position_id>/application/view_all |view all aplications for a position |
|5. |POST |/faculty/position/position<id>/application/<application_id>/approve |approve a specific application |
|6. |POST |faculty/ position/position<id>/application/<application_id>/reject |reject a specific application |
|7. |POST | /faculty/recommendation/<recommendation_id>/approve |approve a reccomendation for an application |
|8. |POST |/faculty/recommendation/<recommendation_id>/deny|deny a recommendation for an application |
|9. |GET,POST |/faculty/position/edit_options |edit a posted position |

Repeat the above for other modules you included in your
application.

### 2.3 User Interface Design
Provide UI sketches or screenshots for the following pages:
* Faculty main page
* Student main page (show how you will display "all positions" vs
"recommended positions")
* Faculty creating a position
* Faculty accepting /rejecting an application
* Student applying a position

<kbd>
      <img src="images/faculty_main.png"  border="2">
      <img src="images/student_main.png"  border="2">
      <img src="images/faculty_create.png" border="2">
      <img src="images/faculty_create.png"  border="2">
      <img src="images/faculty_app_result.png"  border="2">
      <img src="images/student_apply.png"  border="2">
</kbd>

# 3. References
Cite your references here.
For the papers you cite give the authors, the title of the
article, the journal name, journal volume number, date of
publication and inclusive page numbers. Giving only the URL for
the journal is not appropriate.
For the websites, give the title, author (if applicable) and the
website URL.
----
