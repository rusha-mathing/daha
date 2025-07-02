# Daha
## Features
- **Vite**: Next-generation frontend tooling for fast development and builds.
- **React**: JavaScript library for building user interfaces.
- **TypeScript**: Adds static types to JavaScript for better tooling and maintainability.
- **ESLint**: Linting for consistent code quality.

## Prerequisites
- Node.js (v18 or higher recommended)
- npm (v9 or higher)

## Getting Started

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <project-folder>
```

### 2. Install Dependencies
Using npm:
```bash
npm install
```
### 3. .env configuration
```text
VITE_API_URL=
```
## Scripts
- `dev`: Starts the development server with HMR.
- `build`: Creates a production-ready build.
- `preview`: Serves the production build locally.
- `lint`: Runs ESLint to check for code issues.

## Project Structure
```
├── public/                # Static assets
├── src/                   # Source code
│   ├── components/        # Reusable React components
│   ├── App.tsx            # Main app component
│   ├── main.tsx           # Entry point
│   ├── vite-env.d.ts      # Vite TypeScript declarations
├── eslint.config.js       # ESLint configuration
├── index.html             # HTML entry point
├── package.json           # Project metadata and scripts
├── tsconfig.*json          # TypeScript configuration
├── vite.config.ts         # Vite configuration
```

## Customization
- **TypeScript**: Modify `tsconfig.json` for stricter or looser type checking.
- **ESLint**: Update `eslint.config.js` to adjust linting rules.
- **Vite**: Adjust `vite.config.ts` for plugins or build options.
