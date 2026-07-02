# Hands-On 1: QA Concepts, Functional Testing & Defect Lifecycle

## Task 1: Map Testing Types to a Real System

### 1. Test Cases for Different Testing Levels

*   **Unit Testing** (Testing a single function in isolation)
    *   **Test Case:** Verify that the helper function `validate_course_code(code)` returns `true` for valid alphanumeric codes of length 5 to 10, and returns `false` if the code has special characters or is too short/long.
    *   **Preconditions:** Run in isolation using mock inputs; no DB connection is needed.
    *   **Steps:**
        1. Call `validate_course_code("CS101")` and check response.
        2. Call `validate_course_code("CS-101!")` and check response.
        3. Call `validate_course_code("CS")` and check response.
    *   **Expected Result:** Step 1 returns `true`. Steps 2 and 3 return `false`.

*   **Integration Testing** (Testing two components working together, e.g., the API endpoint + database)
    *   **Test Case:** Verify that when we call the POST `/api/courses/` endpoint, the controller correctly calls the database repository to save the course.
    *   **Preconditions:** Test database is running and connected to the API server.
    *   **Steps:**
        1. Send a POST request to `/api/courses/` with: `{ "code": "MATH201", "name": "Calculus II", "credits": 4 }`.
        2. Check the `courses` database table directly for "MATH201".
    *   **Expected Result:** API returns `201 Created` with a new course ID. The database table contains a new row matching our inputs.

*   **System Testing** (Testing the full end-to-end flow from request to database response)
    *   **Test Case:** Verify a complete flow of creating, retrieving, and updating a course through the API.
    *   **Preconditions:** The entire system (API, database, auth middleware) is deployed and running.
    *   **Steps:**
        1. Send a POST request to `/api/courses/` to create a course.
        2. Save the course ID from the response.
        3. Send a GET request to `/api/courses/{id}` to verify details.
        4. Send a PUT request to `/api/courses/{id}` to change credits to 5.
        5. Send another GET request to check if credits updated.
    *   **Expected Result:** POST returns `201 Created`. The first GET returns `200 OK` with the course details. PUT returns `200 OK`. The final GET returns `200 OK` showing credits updated to `5`.

*   **User Acceptance Testing (UAT)** (Testing from the perspective of an actual college admin user)
    *   **Test Case:** Verify that a college administrator can set up a new course and a student can find it to enroll.
    *   **Preconditions:** QA environment is live with admin and student user accounts.
    *   **Steps:**
        1. Log in as an Administrator.
        2. Navigate to "Course Management" and fill out the course form (Code: `CS302`, Name: `Database Systems`, Credits: `4`, Dept: `Computer Science`) and click "Submit".
        3. Log out.
        4. Log in as a Student and search for "CS302" in the enrollment search.
    *   **Expected Result:** Administrator can add the course without errors and sees a success message. The student can find "CS302" in search and see correct details.

---

### 2. Functional vs. Non-Functional Classification

| Test Case Level | Classification | Rationale |
| :--- | :--- | :--- |
| **Unit Testing** | **Functional** | Verifies the logic of the validation function (checking if it accepts/rejects codes correctly). |
| **Integration Testing** | **Functional** | Checks if data flows correctly between the API controller and the database repository. |
| **System Testing** | **Functional** | Tests the entire end-to-end flow of the API CRUD functionality. |
| **User Acceptance Testing (UAT)** | **Functional** | Ensures the application supports real-world business tasks for college admins and students. |

#### Non-Functional Test Example
*   **Type:** Performance Testing (Load Testing)
*   **Test Case:** Verify how the API handles concurrent user traffic.
*   **Preconditions:** JMeter or a similar tool is set up and pointed to the staging environment.
*   **Steps:**
    1. Send requests to `GET /api/courses/` scaling from 1 to 100 concurrent users over 1 minute.
    2. Maintain 100 concurrent users for 5 minutes.
    3. Measure response times and errors.
*   **Expected Result:** Average response time stays below 200ms, and the HTTP error rate is 0% throughout the test.

---

### 3. Black-Box vs. White-Box Testing

*   **Black-Box Testing:**
    *   Testing the system without looking at the internal source code. The tester only checks if the inputs produce the correct outputs based on the requirements.
    *   **Who does it:** QA testers usually perform black-box testing because they focus on user behavior and interface specs.
*   **White-Box Testing:**
    *   Testing with full visibility of the internal code, structure, and logic.
    *   **Who does it:** Developers do white-box testing when writing unit tests to verify specific code paths, loops, and conditions.

---

### 4. Formal Test Cases for `POST /api/courses/`

| Test Case ID | Description | Preconditions | Test Steps | Expected Result | Actual Result | Pass/Fail |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC_API_001** | Create a course with valid data (Happy Path) | API is running, and admin is logged in with a valid token. | 1. Send POST to `/api/courses/` with headers `Content-Type: application/json` and `Authorization: Bearer <token>`. <br> 2. Body: `{ "code": "CS101", "name": "Intro to Programming", "credits": 4 }` | - Response code is `201 Created`. <br> - Response body shows the new course details and a generated `"id"`. | | |
| **TC_API_002** | Attempt to create a course with an existing course code | API is running, admin is logged in. Course `CS101` already exists in the database. | 1. Send POST to `/api/courses/` with auth headers. <br> 2. Body: `{ "code": "CS101", "name": "Advanced Python", "credits": 3 }` | - Response code is `400 Bad Request` or `409 Conflict`. <br> - Error message says the course code already exists. | | |
| **TC_API_003** | Attempt to create a course without the required name | API is running, admin is logged in. | 1. Send POST to `/api/courses/` with auth headers. <br> 2. Body: `{ "code": "CS102", "credits": 3 }` (missing name). | - Response code is `400 Bad Request`. <br> - Response body states that `name` is a required field. | | |

---

## Task 2: Defect Lifecycle & Severity Classification

### 5. Defect Lifecycle

```
                [ NEW ]
                   │
                   ▼
              [ ASSIGNED ]
               /   │    \
              /    │     \
     (Reject) /     │      \ (Defer)
            ▼      ▼       ▼
    [ REJECTED ] [ OPEN ] [ DEFERRED ]
                   │
                   ▼
               [ FIXED ]
                   │
                   ▼
              [ RETEST ]
               /      \
    (Failed)  /        \ (Passed)
             ▼          ▼
         [ OPEN ]   [ VERIFIED ]
                        │
                        ▼
                    [ CLOSED ]
```

*   **New:** Bug is found and reported.
*   **Assigned:** Bug is assigned to a developer to fix.
*   **Open:** Developer is looking at the bug and working on it.
*   **Rejected:** Developer rejects the bug because it's duplicate, not a bug, or works as designed.
*   **Deferred:** Valid bug but will be fixed in a later release.
*   **Fixed:** Developer has fixed the code.
*   **Retest:** QA tests the bug again. If it fails, it goes back to **Open**. If it passes, it goes to **Verified**.
*   **Verified:** QA confirms the bug is fixed.
*   **Closed:** QA closes the bug ticket.

---

### 6. Severity & Priority Classification for 4 Bugs

*   **a) `POST /api/courses/` returns 500 error for all requests.**
    *   **Severity: Critical** | **Priority: P1**
    *   **Justification:** This completely blocks the main feature (creating courses). The server crashes with no workaround, so it needs to be fixed immediately.
*   **b) Course names longer than 150 characters are silently truncated without an error.**
    *   **Severity: Medium** | **Priority: P2**
    *   **Justification:** It silently cuts off user data without warning, which is bad for data integrity. But the app doesn't crash, so it's not critical. It should be fixed before release.
*   **c) Typo in the Swagger documentation.**
    *   **Severity: Low** | **Priority: P4**
    *   **Justification:** This is just a spelling mistake in the docs. The API runs perfectly, so it's low severity and can be fixed whenever there is time.
*   **d) Login occasionally returns 401 on the first try (intermittent).**
    *   **Severity: High** | **Priority: P1**
    *   **Justification:** Authentication failing randomly is bad for user experience. Even though it is intermittent, random auth errors usually mean database connection issues or backend bugs that we need to find and fix before going live.

---

### 7. Defect Report for Bug (a)

**Defect ID:** DEF-001
**Title:** `POST /api/courses/` returns 500 error for all requests
**Environment:** Staging Server (AWS EC2)
**Build Version:** v1.2.0-rc3
**Severity:** Critical
**Priority:** P1

**Steps to Reproduce:**
1. Open Postman.
2. Send a POST request to `http://staging.coursemanager.local/api/courses/`.
3. Add headers: `Content-Type: application/json` and `Authorization: Bearer <valid_token>`.
4. Use this body:
   ```json
   {
     "code": "PHY101",
     "name": "General Physics I",
     "credits": 4
   }
   ```
5. Click send.

**Expected Result:**
Response status `201 Created` with the new course details and its database ID.

**Actual Result:**
Response status `500 Internal Server Error`. The API console logs show: `ERROR: Database relation "courses" does not exist.`

**Attachments:**
- State: 'screenshot of 500 error' (See Postman screenshot and terminal logs).

---

### 8. Severity vs. Priority Explanation

**Severity** is how much a bug breaks the system from a technical standpoint. **Priority** is how quickly the bug needs to be fixed based on business needs.

**Example of High Severity, Low Priority:**
A bug causes a legacy reports feature (e.g., "Export data from 2010 to 2012") to throw a 500 server crash. This is high severity because the server crashes. However, this feature is barely used and the whole module is being deleted next month. The business decides not to waste developer time on it, so the priority is set to Low.
