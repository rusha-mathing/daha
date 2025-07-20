## Development
### Kanban board
[link](https://github.com/orgs/team-42-daha/projects/3/views/1)
#### Entry criteria
##### To Do
- The issue was updated (e.g., via an LLM) to conform to the type "Task" issue form template
- The type "Task" was assigned to the issue
- Relevant labels were assigned to the issue
- The issue was made a sub-issue of a type "Backlog" issue
##### In Progress
- The issue description was revised to provide missing details
- The issue field "Ideal Hours" was filled in
- The issue was added to the current sprint
- The issue was assigned
- If necessary, a branch for the issue was created via the "create a branch" button on the issue page
##### Ready For Review
- A pull request for the issue was created using a relevant template
- Implementation in the pull request was completed
- CI pipeline with automated tests succeeded on the pull request branch
- All sections in the pull request description were updated to match implementation
- A review of the pull request was requested
##### Ready To Merge
- All acceptance criteria specified in the issue were met on the pull request branch
- The pull request was approved
##### Done
- The pull request was merged into the target branch
- If no pull request was required to complete the issue: All acceptance criteria specified in the issue were met

### Git workflow
Based on [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)

#### Creating issues
Issues are created using pre-defined templates:
- [bug report template](.github/ISSUE_TEMPLATE/bug-report-template.md)
- [technical task template](.github/ISSUE_TEMPLATE/tech-task-template.md)
- [user story template](.github/ISSUE_TEMPLATE/user-story-template.md)

Each issue must correspond to a template. Otherwise, a new template must be created (only after discussion with all project members).

#### Labeling issues
Each issue by default has a type (Backlog or Task).
Backlog issues must have label corresponding to its actual type (User Story or Bug)
Tech Tasks must have labels showing`` their relation to technical parts of the project (Frontend, Backend, Database, TG-bot).

#### Assigning issues to team members
Issues are assigned to team members depending on their hard skills and free time. There should not be a situation where all issues are assigned to the same team member.

#### Creating, naming, merging branches
New branches are created for each major feature added to the project. Branch names must reflect their purpose, be short, and written in `snake_case`.  
Merging branches is allowed only after creating a proper pull request and reviewing it.

#### Commit messages format
Commit messages must be short and descriptive. There must be a single commit per any significant code change. Commits should be written in the infinitive form of the verb (e.g., “fix a typo” or “change the code for asynchronous operation”).

#### Creating a pull request
Pull requests are created using a pre-defined template:
- [pull request template](.github/PULL_REQUEST_TEMPLATE.md)

#### Code reviews
Each pull request must be reviewed before approval. Reviews are assigned to a team member with the corresponding technical skills.  
Self-reviewing is strictly prohibited. Reviews must contain comments and suggestions.

#### Merging pull requests
Pull requests can be approved only after a code review. Each pull request must be made from a specific branch and contain major features.

#### Resolving issues
Resolving issues depends on their type:
- User Stories can be marked as resolved only after creating all corresponding functionality and testing acceptance criteria.
- Tech Tasks can be marked as resolved only after completing the task with all subtasks and merging changes into the stable branch.
- Bugs can be marked as resolved only after fixing the bug and merging changes into the stable branch.

#### Git graph diagram
``` mermaid
---
config:
  theme: base
---
%%{init: { 'gitGraph': { 'mainBranchName': 'main', 'showCommitLabel': true } }%%
gitGraph
    commit id: "f98f21b" tag: "init commit"
    branch prototype
    checkout prototype
    commit id: "b6bfec3" tag: "Rebase repo to prototype provided. Migrate to vite."
    commit id: "e9b6183" tag: "Add test blank script to pass gitlab pipeline."
    checkout main
    merge prototype id: "524f9c6" tag: "Merge branch 'prototype' into 'main'"
    commit id: "879ab2e" tag: "Add README.md. Update .gitignore"
    branch dev
    branch dynamic_data
    checkout dynamic_data
    commit id: "c6c854f" tag: "Update .gitignore. Start migrating from mock resources to actual dynamic data."
    commit id: "05642e1" tag: "Factor out all future dynamically loaded content into Resources.ts."
    commit id: "f5b777c" tag: "Strip unnecessary files and defs. (ResourceType.COURSE)"
    commit id: "20545ff" tag: "Refactor dynamic content into api-like functions."
    commit id: "e0cde68" tag: "Resources.ts -> resources.ts. Refactor types into types.ts."
    commit id: "0e6ba31" tag: "Optimize filters to Filter.tsx. Reorganization."
    commit id: "0d837ee" tag: "Very raw outline of frontend + backend (modify_models)"
    commit id: "008d2a0" tag: "Modfiy prototype to work with latest backend update"
    commit id: "b3151d8" tag: "Update README.md"
    commit id: "dfd06c5" tag: "Refactor resources.ts"
    checkout dev
    merge dynamic_data id: "7124185" tag: "Merge branch 'dynamic_data' into 'dev'"
    checkout main
    commit id: "dd22bdb" tag: "Update .gitignore"
    commit id: "8057a53" tag: "prepare to migrate to GitHub"
    checkout dev
    commit id: "c37a42c" tag: "first commit"
    branch models
    checkout models
    commit id: "13515e1" tag: "Models"
    checkout dev
    merge models id: "ec1e9be" tag: "Merge branch 'models' into 'dev'"
    commit id: "cc6fd80" tag: "add: create models, add project skelethon"
    branch modify_models
    checkout modify_models
    commit id: "81f1c8f" tag: "Update base models and database models accordingly for frontend compatibility."
    commit id: "a50fee9" tag: "ruff format"
    commit id: "befbfee" tag: "Partial tests addition and refactoring."
    commit id: "2a2fa8b" tag: "Fixed grades in mock data"
    commit id: "439309e" tag: "Fix 8/9 test cases"
    commit id: "8fd5d9c" tag: "Fix test cases entirely."
    commit id: "1b15f42" tag: "ruff format"
    commit id: "c11a28c" tag: "Port original mock data. Add cors middleware. Reorganize base/database models for auto serialization(validation)."
    commit id: "3a5b4a2" tag: "Add some varying data"
    checkout dev
    merge modify_models id: "812460c" tag: "Merge branch 'modify_models' into 'dev'"
    commit id: "e6a8be5" tag: "Add requirements.txt. Update .gitignore"
    commit id: "aa2dbb9" tag: "ruff format"
    commit id: "0887924" tag: "ruff check --fix --unsafe-fixes"
    branch postgres
    checkout postgres
    commit id: "4cac484" tag: "changed models.py to work with PostgreSQL"
    commit id: "20f6b85" tag: "updated requirements.txt"
    commit id: "4b4109d" tag: "added script for postgres setup, minor fix of variable name"
    commit id: "ae43614" tag: "fixed password in db_url"
    commit id: "a43f763" tag: "rewrote for async usage of db"
    commit id: "3e9079f" tag: "minor fix"
    commit id: "817aa50" tag: "fixed setup script"
    commit id: "aa19b8c" tag: "ruff format"
    commit id: "b0c387b" tag: "ruff check --fix --unsafe-fixes"
    commit id: "e668930" tag: "ruff format"
    commit id: "0c696ea" tag: "update pyproject.toml, uv.lock and fix requirements.txt for new async engine"
    commit id: "cad2d6a" tag: "requirements.txt - basic running deps uv.lock, pyproject.toml - with tests, adjust .gitlab-ci.yml and fix test cases to work with new postgresql async engine"
    commit id: "944755a" tag: "ruff format"
    commit id: "37494cf" tag: ".gitlab-ci.yml: making gitlab ci work with postgresql tests"
    checkout dev
    merge postgres id: "ffa83ad" tag: "Merge branch 'postgres' into 'dev'"
    branch dev-backend
    checkout dev-backend
    commit id: "3a4fbe7" tag: "prepate to migrate backend to GitHub"
    checkout dev
    merge dev-backend id: "49ee3e1" tag: "Merge branch 'dev-backend' into dev"
    branch dev-bot
    checkout dev-bot
    commit id: "fbf3dc5" tag: "Initial commit"
    commit id: "d3336b8" tag: "prepare to migrate bot to GitHub"
    checkout dev
    merge dev-bot id: "2ce18fe" tag: "Merge branch 'dev-bot' into dev"
    commit id: "dc08b26" tag: "Create README.md"
    commit id: "86d2df7" tag: "Migrate gitlab CI to github CI"
    branch proper_readme
    checkout proper_readme
    commit id: "38dcdca" tag: "Added proper REAMDE.md, templates and documentation"
    commit id: "66a73a4" tag: "Added proper REAMDE.md, templates and documentation"
    checkout dev
    merge proper_readme id: "4d2854c" tag: "Merge pull request #20 from team-42-daha/proper_readme"
    commit id: "dd774ee" tag: "Remove duplicate workflows (#22)"
    commit id: "33dbcfc" tag: "Create pull request template"
    commit id: "6c7e20d" tag: "Delete .github/PULL_REQUEST_TEMPLATE directory"
    branch admin_endpoints
    checkout admin_endpoints
    commit id: "2fe8a19" tag: "outline basic create endpoints"
    commit id: "a171f8a" tag: "added tests for creation endpoints"
    commit id: "f94fe5a" tag: "Fixed problems with create_course"
    commit id: "ac973c4" tag: "ruff format"
    commit id: "0870461" tag: "Refactor endpoints, add test cases"
    commit id: "3c7487f" tag: "Modified course creation endpoint for partial autofill => test cases. Outline update and delete endpoints."
    commit id: "6658ec2" tag: "expire_on_commit=False"
    commit id: "b41f12e" tag: "ruff format"
    commit id: "34db08a" tag: "Finalize admin_endpoints, more tests, needs review"
    branch unit_tests
    checkout unit_tests
    commit id: "48ef5e0" tag: "Full vibecoding, needs refactoring"
    commit id: "ef23d3f" tag: "Vibe refactoring"
    commit id: "21f0448" tag: "ruff format && ruff check"
    commit id: "38b392d" tag: "Unit tests"
    checkout admin_endpoints
    commit id: "f6838b8" tag: "Add Kanban board, gitgraph diagram, testing info, change labeling criteria"
    commit id: "975aedf" tag: "Add user acceptance tests"
    checkout dev
    merge admin_endpoints id: "53a84e2" tag: "Merge pull request #24 from team-42-daha/admin_endpoints"
    branch frontend_overhaul
    checkout frontend_overhaul
    commit id: "b14e755" tag: "Branch existing code into testsrc/, rollback to static and factor out"
    commit id: "fe41c4" tag: "src/main.tsx remove duplicate themeprovider and cssbaseline"
    commit id: "e53a335" tag: "Add general props"
    commit id: "1c476d6" tag: "Add DynamicSvg.jsx, depends on  => update package.json"
    commit id: "b14e28c" tag: "Further factor out whole element tree into new components."
    commit id: "57905aa" tag: "Fix the color situation to 'good enough' state"
    commit id: "2e69f92" tag: "Restructure elementTree into encapsulated, somewhat object oriented, blocks"
    commit id: "aaa1d28" tag: "Dynamic loading, custom hooks, restructure"
    commit id: "e470be1" tag: "Working filters, refactor types"
    commit id: "fb5d90a" tag: "add temporary fix: scrollTo top on removing filters"
    commit id: "452bb50" tag: "Upstream overhaul to previous version with scrollTo patch"
    commit id: "e6bb195" tag: "Replace src with testsrc, fix filtering logic error"
    checkout dev
    merge frontend_overhaul id: "f635c39" tag: "Merge pull request #21 from team-42-daha/frontend_overhaul"
    branch bot_prototype
    checkout bot_prototype
    commit id: "40a6b39" tag: "Create basic bot prototype (needs changes in backend)"
    checkout dev
    merge bot_prototype id: "4abfcc2" tag: "Merge pull request #25 from team-42-daha/bot_prototype"
    branch admin_panel
    checkout admin_panel
    commit id: "c5439af" tag: "src/theme/theme.ts -> src/theme/index.ts"
    commit id: "ef38c32" tag: "admin_panel prototype"
    checkout dev
    merge admin_panel id: "65748f3" tag: "Merge pull request #26 from team-42-daha/admin_panel"

```
### Secrets management
We follow strict practices to manage and protect secrets such as API keys, database credentials, and other sensitive configuration values:
- For local setups, all sensitive information must be stored in environment variables (`.env` file added to `.gitignore`), so that they are never hardcoded in the source code or committed to version control.
- For production setups, environment variables are set and managed securely at the system level (e.g., through systemd service files), ensuring they’re never exposed in logs or accessible to the public.

## Quality assurance

### Quality attribute scenarios
[link](docs/quality-assurance/quality-attribute-scenarios.md)

### User acceptance tests
[link](docs/quality-assurance/user-acceptance-tests.md)

### Automated tests
- **Tools Used for Testing:**\
The project uses `pytest` along with `pytest-asyncio` for asynchronous test execution. HTTP requests are performed using `httpx.AsyncClient`, and PostgreSQL test databases are managed with `pytest-postgresql`. `SQLAlchemy` and `SQLModel` are used for ORM and session handling.
- **Types of Tests Implemented**:
    - Integration tests for different API endpoints:
      - CRUD operations for courses, subjects, grades, difficulties, and organizations.
      - Validation of relationships (e.g. courses with multiple subjects and grades).
      - Error handling for not found resources or invalid inputs.
    - Unit tests:
        - TBD
- **Test locations:**\
All tests are located in `backend/app/core/test_router.py`

## Build and deployment

### Continuous Integration
- [Backend workflow](.github/workflows/backend.yml)
  - Static analysis tools:
    - **Ruff**\
      Used to perform static code analysis on Python files to enforce code style, check formatting, and catch common programming errors.
  - Testing Tools
    - **pytest**\
      Used to run automated test cases in the Python backend.
- Frontend workflow:
    - TBD
### Continuous Deployment
*TBD*

## Architecture

### Static view
![static-view.png](docs/architecture/static-view/static-view.png)

#### Coupling and cohesion
The system shows moderate coupling — the frontend, backend, bot, and database are modular but still tightly interdependent through direct connections. Changes in the database schema or bot behavior could easily impact multiple backend modules due to the lack of abstraction layers.\
Each component (e.g. /login, /courses, Telegram Bot) performs a focused, single responsibility, which contributes to high cohesion. However, as the backend grows, cohesion could degrade if responsibilities aren’t clearly separated.

#### Maintainability
The architecture is reasonably maintainable, thanks to modular separation between frontend, backend, and external services. Yet, maintainability could suffer without better abstraction (e.g. service layers, message queues) and encapsulation of cross-cutting concerns like notifications.
### Dynamic view
![dynamic-view.png](docs/architecture/dynamic-view/dynamic-view.png)

#### Test report for "admin adds a course and user gets notification scenario"
*TBD when codebase is ready*

### Deployment view
![deployment-view.png](docs/architecture/deployment-view/deployment-view.png)

#### Deployment Choices
The Daha platform is deployed on a single VPS running Ubuntu, with all core services hosted together:
- Frontend (Vite-built static assets) served via Nginx on `https://daha.pro`
- Backend (FastAPI + Uvicorn) exposed at `https://api.daha.pro`
- PostgreSQL runs locally on the same VPS
- Telegram Bot runs as a background service and listens on a public webhook
- Reverse proxy (Nginx) routes HTTPS traffic to the correct internal services
- Let's Encrypt provides SSL certificates for secure connections
- All services are managed with systemd, ensuring automatic startup and recovery

Such a setup was chosen because of its simplicity. It is suitable for MVPs and can be changed after the product release to ensure greater stability and security.

#### Customer-side Deployment
For the current setup, the customer needs a Linux-based VPS or another type of server having/supporting the following:
- Public IP address (for public access and domain binding)
- Python environment (for FastAPI + bot)
- Node.js (for frontend build and Vite)
- PostgreSQL (as data storage)
- Nginx (or similar utility with reverse proxy functionality)
- systemd (for creating services that can be used to manage all components)

## Usage
For now, you can use only the static part on [daha.pro](https://daha.pro) and try out Telegram bot ([@dahapro_bot](https://t.me/dahapro_bot)). Admin panel part is currently not deployed due to lack of security features (e.g. absence of authentification).

**Maintenance Guide (for customer)**
This section is important because it allows the customer to independently maintain the site after the transfer, minimizing dependence on the team and ensuring long-term stability.
- Regularly update dependencies (e.g. via npm update or similar).
- Monitor server logs for errors.
- Backup: Use Git for version control.

**Ideas for future improvements (for customer)**
This section is useful for planning, as it provides suggestions for how to develop the site if the customer decides to expand the project in the future.
- Add user authentication.
- Integrate analytics (e.g. Google Analytics).
- Optimize for mobile devices, if not already done.
