# 🛠️ Design System Maintenance Guide

## Overview

Este guia fornece instruções para manter e estender o design system do **Cognix com Zyra**.

---

## Table of Contents
1. [Adding New Components](#adding-new-components)
2. [Modifying Existing Components](#modifying-existing-components)
3. [Color Palette Usage](#color-palette-usage)
4. [Typography Standards](#typography-standards)
5. [Spacing Guidelines](#spacing-guidelines)
6. [Icon Usage](#icon-usage)
7. [Common Tasks](#common-tasks)
8. [Troubleshooting](#troubleshooting)

---

## Adding New Components

### Step 1: Define in CSS

```css
/* In static/style.css - Add to appropriate section */

.my-component {
  background: white;
  border-radius: var(--radius-lg);
  border: 1px solid var(--gray-200);
  box-shadow: var(--shadow-sm);
  padding: var(--spacing-lg);
  transition: all 0.3s ease;
}

.my-component:hover {
  border-color: var(--primary);
  box-shadow: var(--shadow-md);
}
```

### Step 2: Use in Templates

```html
<div class="my-component">
  <h3>Component Title</h3>
  <p>Component content...</p>
</div>
```

### Step 3: Document in COMPONENT_LIBRARY.md

```markdown
### My Component
\`\`\`html
<div class="my-component">
  <h3>Title</h3>
  <p>Description</p>
</div>
\`\`\`
```

---

## Modifying Existing Components

### Best Practices

✅ **Do:**
- Use CSS variables for colors, spacing
- Follow BEM naming (block__element--modifier)
- Test responsive versions
- Keep semantic HTML
- Document changes

❌ **Don't:**
- Add inline styles
- Hardcode colors/spacing
- Break existing component structure
- Skip responsive design
- Undocument changes

### Example Modification

```css
/* ❌ Wrong */
.card { padding: 20px; color: #3b82f6; }

/* ✅ Correct */
.card {
  padding: var(--spacing-lg);
  color: var(--primary);
}
```

---

## Color Palette Usage

### Available Colors

```css
/* Primary */
--primary: #3b82f6           /* Use for: CTAs, active states, primary actions */
--primary-light: #60a5fa     /* Use for: Hover states, highlighted */
--primary-dark: #1e40af      /* Use for: Active/pressed states */

/* Semantic */
--success: #10b981          /* Use for: Positive actions, confirmations */
--warning: #f59e0b          /* Use for: Alerts, cautions */  
--danger: #ef4444           /* Use for: Errors, deletions */
--info: #3b82f6             /* Use for: Information, neutral actions */

/* Neutral */
--gray-50 to --gray-900     /* Use for: Backgrounds, borders, text */
```

### Usage Examples

```html
<!-- Button with primary color -->
<button class="btn btn--primary">Action</button>

<!-- Badge with success color -->
<span class="badge--success">Approved</span>

<!-- Alert with danger color -->
<div class="alert alert--danger">Error occurred</div>

<!-- Text with secondary color -->
<p style="color: var(--gray-600);">Secondary text</p>
```

---

## Typography Standards

### Font Families
- **Headers (h1-h6)**: Poppins, sans-serif
- **Body/Text**: Inter, sans-serif
- **Monospace**: System default (for code)

### Font Sizes

```css
h1 { font-size: 2rem;        /* 32px */ }
h2 { font-size: 1.5rem;      /* 24px */ }
h3 { font-size: 1.25rem;     /* 20px */ }
h4 { font-size: 1.125rem;    /* 18px */ }
h5, h6 { font-size: 1rem;    /* 16px */ }

p { font-size: 1rem;         /* 16px - default */ }
.text-sm { font-size: 0.875rem;  /* 14px */ }
.text-xs { font-size: 0.75rem;   /* 12px */ }
```

### Font Weights

```css
/* Headers - Always bold */
h1, h2, h3, h4, h5, h6 { font-weight: 600; }

/* Body */
p { font-weight: 400; }          /* Regular */
strong { font-weight: 600; }     /* Bold */

/* Labels/Captions */
.form-label { font-weight: 500; } /* Medium */
```

### Line Height

```css
h1, h2, h3, h4, h5, h6 { line-height: 1.2; }
p { line-height: 1.6; }
```

---

## Spacing Guidelines

### Spacing System

```css
--spacing-xs: 0.25rem;   /*  4px - Between inline elements */
--spacing-sm: 0.5rem;    /*  8px - Small gaps */
--spacing-md: 1rem;      /* 16px - Standard gap */
--spacing-lg: 1.5rem;    /* 24px - Between sections */
--spacing-xl: 2rem;      /* 32px - Major spacing */
--spacing-2xl: 3rem;     /* 48px - Page sections */
```

### Where to Use

| Spacing | Usage |
|---------|-------|
| `xs` | Icon-text gap, badge padding |
| `sm` | Between form elements, button margins |
| `md` | Card padding, list gaps, standard gaps |
| `lg` | Section padding, card-to-card spacing |
| `xl` | Major component spacing |
| `2xl` | Page sections, top-level spacing |

### Examples

```html
<!-- Small gap between icon and text -->
<div class="flex gap-md">
  <i class="fas fa-icon"></i>
  <span>Label</span>
</div>

<!-- Section spacing -->
<section class="page-section" style="margin-bottom: var(--spacing-2xl);">
  ...
</section>

<!-- Card padding -->
<div class="card" style="padding: var(--spacing-lg);">
  ...
</div>
```

---

## Icon Usage

### Font Awesome Integration

System uses **Font Awesome 6.4.0** (CDN)

### Icon Classes

```html
<!-- Basic usage -->
<i class="fas fa-icon-name"></i>

<!-- Sized icons -->
<i class="fas fa-icon" style="font-size: 1.5rem;"></i>
<i class="fas fa-icon" style="font-size: 2rem;"></i>
<i class="fas fa-icon" style="font-size: 3rem;"></i>

<!-- Colored icons -->
<i class="fas fa-icon" style="color: var(--primary);"></i>
<i class="fas fa-icon" style="color: var(--success);"></i>
```

### Common Icons

```html
<!-- Navigation -->
<i class="fas fa-chart-line"></i>      <!-- Dashboard -->
<i class="fas fa-robot"></i>           <!-- AI/Bot -->
<i class="fas fa-box"></i>             <!-- Products/Inventory -->
<i class="fas fa-credit-card"></i>     <!-- Payments/Transactions -->
<i class="fas fa-users"></i>           <!-- Clients/Groups -->

<!-- Actions -->
<i class="fas fa-plus"></i>            <!-- Add/Create -->
<i class="fas fa-edit"></i>            <!-- Edit -->
<i class="fas fa-trash"></i>           <!-- Delete -->
<i class="fas fa-save"></i>            <!-- Save -->

<!-- Status -->
<i class="fas fa-check-circle"></i>    <!-- Success -->
<i class="fas fa-exclamation-circle"></i> <!-- Warning -->
<i class="fas fa-times-circle"></i>    <!-- Error -->
<i class="fas fa-info-circle"></i>     <!-- Info -->

<!-- Other -->
<i class="fas fa-bell"></i>            <!-- Notifications -->
<i class="fas fa-cog"></i>             <!-- Settings -->
<i class="fas fa-lock"></i>            <!-- Security -->
```

### Finding Icons

Visit: https://fontawesome.com/icons

---

## Common Tasks

### Changing a Button Style

```html
<!-- Before -->
<button class="btn btn--primary">Save</button>

<!-- After (Change style) -->
<button class="btn btn--success">Save</button>

<!-- With Icon -->
<button class="btn btn--primary">
  <i class="fas fa-save"></i> Save
</button>
```

### Creating a New Card

```html
<div class="card">
  <h3>Card Title</h3>
  <p>Card content goes here...</p>
  <button class="btn btn--ghost">Learn More</button>
</div>
```

### Adding Alert Message

```html
<div class="alert alert--success">
  <div class="alert__icon">
    <i class="fas fa-check-circle"></i>
  </div>
  <div class="alert__content">
    <div class="alert__title">Success</div>
    <p>Operation completed successfully.</p>
  </div>
</div>
```

### Creating Empty State

```html
<div class="empty-state">
  <div class="empty-state__icon">
    <i class="fas fa-inbox"></i>
  </div>
  <h3 class="empty-state__title">No Items</h3>
  <p class="empty-state__text">No items found. Start by creating one.</p>
  <button class="btn btn--primary">Create Item</button>
</div>
```

### Making Responsive Grid

```html
<!-- 4-column on desktop, 1-column on mobile -->
<div class="kpi-grid">
  <div class="kpi-card">...</div>
  <div class="kpi-card">...</div>
  <div class="kpi-card">...</div>
  <div class="kpi-card">...</div>
</div>
```

---

## Troubleshooting

### Issue: Component Styling Not Applied

**Solution:**
1. Verify CSS class name spelling
2. Check if Font Awesome CSS is loaded
3. Verify CSS variable names
4. Check for conflicting inline styles

```html
<!-- ❌ Wrong -->
<button class="btn primary-btn">Click</button>

<!-- ✅ Correct -->
<button class="btn btn--primary">Click</button>
```

### Issue: Colors Look Different

**Solution:**
- Use CSS variables instead of hardcoded colors
- Ensure browser cache is cleared
- Verify CSS file is being loaded

```css
/* ❌ Don't */
background-color: #3b82f6;

/* ✅ Do */
background-color: var(--primary);
```

### Issue: Icons Not Showing

**Solution:**
1. Verify Font Awesome CDN is loaded in HTML head
2. Check icon class name is correct
3. Verify using `fas` prefix (solid icons)

```html
<!-- ❌ Wrong -->
<i class="icon-chart"></i>

<!-- ✅ Correct -->
<i class="fas fa-chart-line"></i>
```

### Issue: Responsive Design Breaking

**Solution:**
- Test on mobile viewport (DevTools)
- Check media queries in CSS
- Verify grid/flex classes applied

```css
/* Mobile responsive */
@media (max-width: 768px) {
  .grid { grid-template-columns: 1fr; }
}
```

### Issue: Spacing Looks Wrong

**Solution:**
- Use spacing variables instead of hardcoded values
- Check parent container margins
- Verify margin/padding not conflicting

```html
<!-- ❌ Wrong -->
<div style="margin-bottom: 30px;">

<!-- ✅ Correct -->
<div style="margin-bottom: var(--spacing-xl);">
```

---

## CSS File Location

**Main Stylesheet**: `static/style.css`

### Organization
```
1. Imports & Variables
2. Reset & Base Styles
3. Typography
4. Layout & Grid
5. Sidebar
6. Header
7. Cards
8. KPI Cards
9. Buttons
10. Tables
11. Forms
12. Alerts
13. Badges
14. Other Components
15. Responsive Design
```

---

## Template Structure

### Main Layout

```html
<div class="layout">
  <aside class="layout__sidebar">
    {% include 'components/sidebar.html' %}
  </aside>
  
  <div class="layout__main">
    <header class="layout__header">
      {% include 'components/header.html' %}
    </header>
    
    <div class="layout__content">
      <!-- Page content goes here -->
    </div>
  </div>
</div>
```

### Page Template

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Title</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <div class="layout">
        {% include 'components/sidebar.html' %}
        <div class="layout__main">
            {% include 'components/header.html' %}
            <div class="layout__content">
                <!-- Your content here -->
            </div>
        </div>
    </div>
</body>
</html>
```

---

## Updating the System

### To Add New Features

1. Create HTML in template
2. Add CSS to `style.css` (at end with others forms)
3. Follow BEM naming pattern
4. Use CSS variables
5. Test responsive design
6. Document in COMPONENT_LIBRARY.md

### To Modify Existing

1. Edit CSS in `style.css`
2. Don't use inline styles in HTML
3. Test all breakpoints
4. Update documentation
5. Test in all browsers

### To Fix Bug

1. Identify the component
2. Edit CSS or HTML
3. Test fix thoroughly
4. Document change
5. Verify no side effects

---

## Style Guide Summary

| Rule | Details |
|------|---------|
| **Colors** | Use var(--color-name) |
| **Spacing** | Use var(--spacing-size) |
| **Typography** | Use established font/size rules |
| **Icons** | Use Font Awesome fas fa-* |
| **Classes** | Follow BEM (block__element--modifier) |
| **HTML** | Semantic tags (section, article, etc.) |
| **Responsive** | Mobile-first, then tablet, then desktop |
| **Browser** | Support last 2 versions |

---

## Resources

- **Component Library**: See `COMPONENT_LIBRARY.md`
- **Full Report**: See `DESIGN_OVERHAUL_REPORT.md`
- **Summary**: See `DESIGN_SUMMARY.md`
- **Font Awesome**: https://fontawesome.com/icons
- **CSS Variables**: https://developer.mozilla.org/en-US/docs/Web/CSS/--*

---

## Questions?

Refer to:
1. **COMPONENT_LIBRARY.md** for component usage
2. **style.css** for CSS implementation
3. **Existing components** as examples
4. **Font Awesome docs** for icon names

---

**Last Updated**: Current Session  
**Version**: 1.0  
**Status**: ✅ Active

*Happy coding! Remember: Consistency is key to maintaining professional design.*
