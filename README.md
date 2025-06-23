Overview:
You are tasked with building a backend service that integrates with the Ticketmaster
public API to collect events, store them locally, and allow authenticated users to save
and retrieve personal favorite events.
Functional Requirements
Authentication
● Implement user authentication using a third-party identity provider.
● Only authenticated users should be able to:
○ Save events to their personal list.
○ Retrieve their saved events.
● Unauthenticated users should still be able to browse public events.
External API Integration
● Integrate with Ticketmaster Discovery API.
● Choose which endpoints and data fields you want to retrieve.
● Persist relevant event data into your local database.
● Design your data model thoughtfully.
Event Fetching Strategy
● Define your own strategy for fetching and updating events:
○ Scheduled background jobs?
○ On-demand fetching?
○ Combination?
● Justify your approach in your documentation.
API Endpoints
At minimum, your system should expose:
Method Path Description
GET /events/ List public events (paginated, allow
filtering/querying)
POST /events/{event_id}/save Save an event to the authenticated
user’s personal list.
GET /my/events/ Retrieve the authenticated user’s
saved events.
The API should follow RESTful principles and be self-explanatory.
Technical Requirements
Technology Stack
Your solution should be built primarily with:
● Python 3.11+
● A modern Python web framework suitable for building web APIs (e.g. FastAPI)
● A relational database (e.g. PostgreSQL)
● The App should be deployable using docker-compose
You are free to choose specific libraries, packages, and tools that you believe are appropriate —
be prepared to explain your decisions.
Authentication should rely on a third-party identity provider (e.g., Auth0 or equivalent).
Design Expectations
Structure your code in a way that facilitates maintainability, testability, and future scalability.
Apply appropriate software engineering principles such as:
● Separation of concerns
● Dependency injection where meaningful
● Error handling and consistent exception management
● Logging and observability
● Thoughtful use of design patterns where applicable
● Async programming where it makes sense
Testing
● Include unit tests covering critical parts of your business logic.
● Focus on areas such as:
○ Data access
○ Business logic
● You may use any testing framework you’re comfortable with (e.g. pytest).
Deliverables
● Complete codebase in a Git repository.
● A clear and complete `README.md` that includes:
○ Setup and run instructions (including Docker Compose)
○ Auth provider setup instructions (how to configure your identity provider)
○ API usage guide
○ Design and architecture explanation
○ Justification for major design and technology decisions
# Example using PyPDF2
import PyPDF2

with open('c:/Users/PC/Downloads/BE Technical Challenge.pdf', 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        print(page.extract_text())