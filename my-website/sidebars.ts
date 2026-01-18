import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Tutorial',
      items: [
        'intro',
        {
          type: 'category',
          label: 'Tutorial Basics',
          items: [
            'tutorial-basics/create-a-document',
            'tutorial-basics/create-a-page',
            'tutorial-basics/deploy-your-site',
          ],
        },
        {
          type: 'category',
          label: 'Tutorial Extras',
          items: [
            'tutorial-extras/manage-docs-versions',
            'tutorial-extras/add-custom-css',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System',
      items: [
        'module-1-robotic-nervous-system/introduction',
        'module-1-robotic-nervous-system/communication-concepts',
        'module-1-robotic-nervous-system/node-topic-service-analogies',
        'module-1-robotic-nervous-system/software-to-action-connection',
        'module-1-robotic-nervous-system/robot-physical-structure',
        'module-1-robotic-nervous-system/robot-function-entity',
        'module-1-robotic-nervous-system/robot-component-entity',
        'module-1-robotic-nervous-system/code-to-motion-traceability',
        'module-1-robotic-nervous-system/advanced-connections',
        'module-1-robotic-nervous-system/practical-examples',
        'module-1-robotic-nervous-system/visual-standards',
        'module-1-robotic-nervous-system/navigation',
        'module-1-robotic-nervous-system/software-commands-to-actions',
        'module-1-robotic-nervous-system/summary',
        'module-1-robotic-nervous-system/glossary',
        {
          type: 'category',
          label: 'Exercises',
          items: [
            'module-1-robotic-nervous-system/exercises/comprehension-questions',
            'module-1-robotic-nervous-system/exercises/scenario-based-tasks',
            'module-1-robotic-nervous-system/exercises/identify-functions-exercises',
            'module-1-robotic-nervous-system/exercises/scenario-identification-tasks',
            'module-1-robotic-nervous-system/exercises/function-identification-assessment',
            'module-1-robotic-nervous-system/exercises/predict-robot-behavior',
            'module-1-robotic-nervous-system/exercises/reverse-identification-exercises',
            'module-1-robotic-nervous-system/exercises/functions-to-components-exercises',
            'module-1-robotic-nervous-system/exercises/software-to-action-assessment',
          ],
        },
      ],
    },
  ],

  // But you can create a sidebar manually
  /*
  tutorialSidebar: [
    'intro',
    'hello',
    {
      type: 'category',
      label: 'Tutorial',
      items: ['tutorial-basics/create-a-document'],
    },
  ],
   */
};

export default sidebars;
