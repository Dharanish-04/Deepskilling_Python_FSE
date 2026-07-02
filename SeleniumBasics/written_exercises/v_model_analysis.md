# Hands-On 2: SDLC vs TDLC — V-Model & Agile QA Integration

## Task 1: V-Model Mapping

### 1. V-Model Diagram (ASCII Art)

```
       VERIFICATION PHASE (SDLC)                      VALIDATION PHASE (TDLC)
  ┌─────────────────────────────────┐           ┌─────────────────────────────────┐
  │      Business Requirements      │◄─────────►│   User Acceptance Testing (UAT) │
  └────────────────┬────────────────┘           └────────────────▲────────────────┘
                   │                                             │
                   ▼                                             │
  ┌─────────────────────────────────┐           ┌────────────────┴────────────────┐
  │          System Design          │◄─────────►│         System Testing          │
  └────────────────┬────────────────┘           └────────────────▲────────────────┘
                   │                                             │
                   ▼                                             │
  ┌─────────────────────────────────┐           ┌────────────────┴────────────────┐
  │       Architecture Design       │◄─────────►│       Integration Testing       │
  └────────────────┬────────────────┘           └────────────────▲────────────────┘
                   │                                             │
                   ▼                                             │
  ┌─────────────────────────────────┐           ┌────────────────┴────────────────┐
  │          Module Design          │◄─────────►│          Unit Testing           │
  └────────────────┬────────────────┘           └────────────────▲────────────────┘
                   │                                             │
                   └──────────────────►[ CODING ]────────────────┘
```

---

### 2. SDLC ↔ TDLC Phase Mapping & Test Artifacts

*   **Requirements ↔ UAT (User Acceptance Testing)**
    *   **Explanation:** The business requirements define what the user needs. UAT checks if the final app actually works for the users.
    *   **Artifact:** Acceptance Test Plan and UAT Scenarios.
*   **System Design ↔ System Testing**
    *   **Explanation:** System design details the functional specifications. System testing checks the whole app to make sure it follows these specifications.
    *   **Artifact:** System Test Plan and System Test Cases.
*   **Architecture Design ↔ Integration Testing**
    *   **Explanation:** Architecture design maps how components and APIs interact. Integration testing verifies if these parts connect and share data properly.
    *   **Artifact:** Integration Test Plan and Integration Test Cases.
*   **Module Design ↔ Unit Testing**
    *   **Explanation:** Module design details how specific functions and classes should work. Unit testing tests these functions in isolation.
    *   **Artifact:** Unit Test Cases / Specs.
*   **Coding** (Bottom Vertex)
    *   **Explanation:** Writing the code.
    *   **Artifact:** Unit Test code and Code Review checklists.

---

### 3. Entry and Exit Criteria for Testing Levels

| Testing Level | Entry Criteria | Exit Criteria |
| :--- | :--- | :--- |
| **Unit Testing** | - Code for the module is written.<br>- Code compiles without syntax errors.<br>- Unit test framework is configured. | - All planned unit tests are run.<br>- 100% pass rate.<br>- Code coverage meets target (e.g. 90% statement). |
| **Integration Testing** | - Unit testing is completed.<br>- Modules are built and deployed to the integration environment.<br>- API contracts are stable. | - All integration tests are run.<br>- Pass rate is at least 95%.<br>- No major bugs in module interfaces. |
| **System Testing** | - Integration testing is complete.<br>- Full build is deployed to the QA environment.<br>- Staging/QA database is ready. | - All system test cases are executed.<br>- Pass rate is 98% or higher.<br>- Zero open Critical or High severity bugs. |
| **User Acceptance Testing (UAT)** | - System testing is finished and approved.<br>- UAT environment is set up with test data.<br>- Business users have access and accounts. | - Core user workflows are tested.<br>- Business users verify everything works as expected.<br>- Product Owner signs off on release. |

---

### 4. Two Early QA Engagement Points

1.  **Requirements Review (During Requirements Analysis)**
    *   QA reviews user stories before development starts. For the Course Management API, QA can spot vague requirements early. For example, if a requirement says "creation should be fast," QA can clarify it to "must respond within 200ms."
2.  **API Design Review (During System/Architecture Design)**
    *   QA reviews the Swagger/OpenAPI specifications before coding. For the API, QA can verify input constraints (like unique course codes) and error responses to make sure they match business logic.

---

## Task 2: Agile QA and Shift-Left Testing

### 5. 3 Problems with Waterfall Testing for Course Management API

1.  **Bugs found too late:** If we find a database design flaw or security issue in the system testing phase, it requires rewriting a lot of code, which is expensive and slow.
2.  **Rushed testing (QA Squeeze):** If coding takes longer than planned, the testing phase is shortened to meet the release date, leading to skipped edge cases.
3.  **Slow feedback:** Developers write code weeks before QA finds a bug in it. It takes time for developers to remember how their code works to fix it.

---

### 6. QA Role in Agile Ceremonies

*   **Sprint Planning:** QA helps write acceptance criteria for user stories and estimates the effort needed for testing.
*   **Daily Standup:** QA shares what they tested, what they are doing today, and mentions any blocker issues like a broken test database.
*   **Sprint Review:** QA helps demonstrate new features to stakeholders and reports on quality status.
*   **Retrospective:** QA suggests ways to improve the team's process, like fixing issues with test environments or automated pipelines.

---

### 7. 4 Shift-Left Practices Applied to Course Management API

1.  **Reviewing Requirements:** QA checks if the course requirements specify boundaries (e.g., maximum length of course name, credit range) before code is written.
2.  **Writing Test Cases Before Code (TDD/BDD):** Writing Gherkin scenarios or API test specifications before developers start coding, so developers know exactly what to build to pass.
3.  **Static Code Analysis:** Running tool checks (like Pylint) in the CI/CD pipeline to catch syntax, style, or simple code errors automatically.
4.  **API Contract Testing:** Testing endpoint shapes and schemas (e.g., using Postman) before full integration, making sure frontend and backend sync correctly.

---

### 8. Acceptance Criteria in Given-When-Then (Gherkin) Format

User Story: *"As a college admin, I want to create a new course, so that students can enroll in it."*

#### Scenario 1: Successful Course Creation (Happy Path)
```gherkin
Given the college administrator is authenticated and authorized to manage courses
And the course code "CS101" does not exist in the system
When the administrator sends a POST request to "/api/courses/" with the following details:
  | field   | value                  |
  | code    | CS101                  |
  | name    | Intro to Computer Sci  |
  | credits | 4                      |
Then the API should return a response status code of 201 Created
And the response payload should contain a unique course ID
And the database should contain a record for course "CS101" with all the provided details
```

#### Scenario 2: Prevent Creation of Duplicate Course
```gherkin
Given the college administrator is authenticated and authorized to manage courses
And a course with the course code "CS101" already exists in the system
When the administrator sends a POST request to "/api/courses/" with the following details:
  | field   | value                      |
  | code    | CS101                      |
  | name    | Advanced Computer Science  |
  | credits | 3                          |
Then the API should return a response status code of 400 Bad Request
And the response payload should contain an error message "Course code CS101 already exists."
And the database record for "CS101" should remain unchanged
```

#### Scenario 3: Prevent Creation with Missing Required Fields
```gherkin
Given the college administrator is authenticated and authorized to manage courses
When the administrator sends a POST request to "/api/courses/" with the following details:
  | field   | value |
  | code    | CS102 |
  | credits | 3     |
Then the API should return a response status code of 400 Bad Request
And the response payload should contain a validation error message indicating "name is a required field."
And no new course record should be created in the database
```
