---
sidebar_position: 10
title: "Visual Identity and Diagramming Standards"
---

# Visual Identity and Diagramming Standards

## Creating Consistent Visual Communications

This document establishes the visual identity and diagramming standards for Module 1: The Robotic Nervous System. These standards ensure consistency across all visual materials and help students understand concepts more effectively through standardized representations.

## Color Palette

### Primary Colors
- **Robot Blue**: #2E86AB (used for robot functions and nodes)
- **Communication Green**: #A23B72 (used for communication channels and topics)
- **Action Orange**: #F18F01 (used for services and actions)
- **Information Yellow**: #C73E1D (used for data and messages)

### Secondary Colors
- **Support Gray**: #8A8988 (used for supporting elements and backgrounds)
- **Success Green**: #5CB85C (used for successful connections and operations)
- **Warning Amber**: #F0AD4E (used for warnings and cautionary elements)
- **Error Red**: #D9534F (used for error conditions and failures)

### Color Usage Guidelines
- Use Robot Blue consistently for all robot function representations
- Use Communication Green for all communication channel visualizations
- Use Action Orange for all service and action representations
- Maintain high contrast ratios for accessibility (minimum 4.5:1)
- Ensure color choices work in both color and grayscale printing

## Iconography Standards

### Robot Function Icons
- Circular icons with department-like symbols
- Consistent 24px padding within 64x64px canvas
- Use simple geometric shapes to represent function types
- Include text labels when space permits

### Communication Channel Icons
- Arrow symbols indicating direction of information flow
- Bidirectional arrows for two-way communication
- Wavy lines for broadcast communication
- Solid lines for direct communication

### Service Request Icons
- Question mark bubble for requests
- Checkmark bubble for responses
- Clock symbol for timing-sensitive operations

## Diagramming Standards

### Node Representation
```
┌─────────────────┐
│   Navigation    │ ← Department-style label
│    Department   │
└─────────────────┘
```

- Rounded rectangles with consistent corner radius (8px)
- Dark text on light background for readability
- Consistent sizing for similar node types
- Include node name and brief function description

### Communication Flow Representation
```
Publisher Node ────── Topic Channel ──────→ Subscriber Node
                     (broadcast arrow)
```

- Solid arrows for direct communication (services)
- Dashed arrows for broadcast communication (topics)
- Dotted arrows for feedback during actions
- Labels indicating message type and frequency

### System Architecture Diagrams
- Use layered approach: Sensors → Processing → Communication → Actuation
- Consistent spacing between layers (40px vertical, 60px horizontal)
- Color coding to indicate different system components
- Legend included in all complex diagrams

## Typography Standards

### Headings
- **H1**: 32px, Bold, Robot Blue (#2E86AB)
- **H2**: 24px, Semi-bold, Communication Green (#A23B72)
- **H3**: 20px, Medium, Action Orange (#F18F01)
- **H4**: 18px, Regular, Information Yellow (#C73E1D)

### Body Text
- **Primary**: 16px, Regular, Dark Gray (#333333)
- **Secondary**: 14px, Regular, Medium Gray (#666666)
- **Captions**: 12px, Regular, Light Gray (#888888)

### Code Elements
- **Inline code**: 14px, Monospace, Robot Blue background
- **Code blocks**: 14px, Monospace, Light gray background
- **Comments**: 14px, Monospace, Green text
- **Keywords**: 14px, Monospace, Purple text

## Layout Guidelines

### Page Structure
- **Header**: Module title and navigation
- **Content Area**: Main educational content (75% width)
- **Sidebar**: Quick navigation and related links (25% width)
- **Footer**: Additional resources and next steps

### Diagram Placement
- Center-align all diagrams within content area
- Maintain 24px margin above and below diagrams
- Include descriptive captions below each diagram
- Number diagrams sequentially (Diagram 1, Diagram 2, etc.)

### Content Blocks
- **Learning Objectives**: Blue background (#E6F2F7)
- **Real-World Analogies**: Green background (#F7EBF0)
- **Technical Connections**: Orange background (#FFF7E8)
- **Check Your Understanding**: Yellow background (#FEF2EC)

## Accessibility Standards

### Visual Hierarchy
- Maintain clear visual hierarchy with consistent spacing
- Use sufficient white space (minimum 16px between elements)
- Ensure all text has adequate contrast against backgrounds
- Provide alternative text for all diagrams and images

### Alternative Representations
- Include text descriptions for all visual elements
- Use consistent patterns that can be recognized by screen readers
- Provide SVG versions of diagrams for scalability
- Include color-independent identification methods

### Responsive Design
- Ensure diagrams remain readable on mobile devices
- Maintain aspect ratios when scaling
- Provide zoom functionality for complex diagrams
- Optimize for both portrait and landscape orientations

## Diagram Types and Templates

### Communication Flow Diagrams
Template for showing how information flows between robot functions:
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Publisher   │───▶│ Information │───▶│ Subscriber  │
│ Function    │    │ Channel     │    │ Function    │
└─────────────┘    └─────────────┘    └─────────────┘
```

### System Architecture Diagrams
Template for showing the overall structure of a robot system:
```
┌─────────────────────────────────────────┐
│              Sensors Layer              │
├─────────────────────────────────────────┤
│            Processing Layer             │
├─────────────────────────────────────────┤
│          Communication Layer            │
├─────────────────────────────────────────┤
│            Actuation Layer              │
└─────────────────────────────────────────┘
```

### Interaction Pattern Diagrams
Template for showing different communication patterns:
```
Topics (Broadcast):     Services (Request-Response):    Actions (Extended Operations):
  A ────▶ B,C,D               A ⟷ B                      A ⟳ B
  (One-to-Many)           (Direct Request)           (With Feedback)
```

## Consistency Checks

Before finalizing any visual content, verify:

- [ ] Colors match the defined palette
- [ ] Typography follows established guidelines
- [ ] Icons are consistent in style and size
- [ ] Diagrams use standard symbols and notation
- [ ] All visual elements have appropriate alt text
- [ ] Contrast ratios meet accessibility standards
- [ ] Layout follows established grid system
- [ ] File sizes are optimized for web delivery

## File Format Standards

### Images
- **Photographs**: JPEG format, maximum 1MB
- **Diagrams**: SVG format for scalability
- **Icons**: PNG format with transparency
- **Screenshots**: PNG format for clarity

### Naming Convention
- Use lowercase letters with hyphens: `robot-navigation-flow.svg`
- Include descriptive names: `communication-analogy-company-department.svg`
- Version control: `filename-v1.svg`, `filename-v2.svg`

## Quality Assurance

### Review Checklist
- [ ] All diagrams support the learning objectives
- [ ] Visual elements enhance rather than distract from content
- [ ] Consistent style maintained throughout module
- [ ] Visual hierarchy guides reader attention appropriately
- [ ] All visual elements are accessible to diverse learners

## Style Evolution

These standards may evolve as the module develops. When proposing changes:
1. Document the reason for the proposed change
2. Show how the change improves learning effectiveness
3. Update all existing materials to match new standards
4. Communicate changes to all content creators

## References

These standards align with:
- Web Content Accessibility Guidelines (WCAG) 2.1
- Docusaurus documentation best practices
- Educational design principles for STEM learning
- Industry standards for technical communication