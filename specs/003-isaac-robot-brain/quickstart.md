# Quickstart Guide: AI-Robot Brain Educational Module

## Prerequisites
- Node.js 18+ installed
- Git installed
- Access to NVIDIA Isaac documentation (for reference)

## Setup

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Navigate to the project directory**:
   ```bash
   cd my-website
   ```

3. **Install dependencies**:
   ```bash
   npm install
   ```

4. **Start the development server**:
   ```bash
   npm start
   ```
   This will start the Docusaurus development server and open your site in a browser at `http://localhost:3000`.

## Adding the AI-Robot Brain Content

1. **Create the module directory**:
   ```bash
   mkdir -p docs/module-3-ai-robot-brain
   ```

2. **Add the three chapters**:
   ```bash
   touch docs/module-3-ai-robot-brain/chapter-1-photorealistic-intelligence.md
   touch docs/module-3-ai-robot-brain/chapter-2-seeing-navigating.md
   touch docs/module-3-ai-robot-brain/chapter-3-motion-planning.md
   ```

3. **Update the sidebar configuration** in `my-website/sidebars.ts`:
   Add the new module to the sidebar navigation.

## Building Content

1. **Chapter 1: Photorealistic Intelligence with NVIDIA Isaac Sim**
   - Create realistic virtual world explanations
   - Add synthetic data generation examples
   - Include safety benefits of simulation

2. **Chapter 2: Seeing and Navigating with Isaac ROS**
   - Explain VSLAM concepts in accessible language
   - Demonstrate real-time localization
   - Show mapping examples

3. **Chapter 3: Intelligent Motion Planning with Nav2**
   - Cover high-level decision making
   - Explain obstacle avoidance
   - Show coordination between perception and action

## Adding Interactive Elements

1. **SVG Diagrams**: Place in `static/img/` directory
2. **Interactive HTML Examples**: Place in `static/interactive-examples/`
3. **Update Docusaurus config** to serve static assets

## Running Tests

1. **Check for broken links**:
   ```bash
   npm run build
   ```

2. **Lint the content**:
   ```bash
   npm run lint
   ```

## Deployment

1. **Build the site**:
   ```bash
   npm run build
   ```

2. **Deploy to GitHub Pages** (as configured in `docusaurus.config.js`)

## Development Workflow

1. Edit content in the `docs/module-3-ai-robot-brain/` directory
2. Preview changes live at `http://localhost:3000`
3. Add diagrams and interactive elements as needed
4. Verify all links and content before committing
5. Submit pull request for review