# 📚 Componentes de Design System - Guia Rápido

## Índice
1. [Layout Components](#layout-components)
2. [Cards & Indicators](#cards--indicators)
3. [Typography](#typography)
4. [Buttons](#buttons)
5. [Badges & Status](#badges--status)
6. [Forms & Inputs](#forms--inputs)
7. [Tables](#tables)
8. [Alerts & Notifications](#alerts--notifications)
9. [Empty States](#empty-states)
10. [Colors & Variables](#colors--variables)

---

## Layout Components

### Main Layout
```html
<div class="layout">
  <aside class="layout__sidebar"><!-- Navigation --></aside>
  <div class="layout__main">
    <header class="layout__header"><!-- Header --></header>
    <div class="layout__content"><!-- Page Content --></div>
  </div>
</div>
```

**CSS Variables:**
- `--layout__sidebar`: 260px fixed width
- `--layout__header`: Sticky top
- `--layout__content`: Scrollable main area

### Page Section
```html
<section class="page-section">
  <h2 class="page-section__title">
    <div class="page-section__title-icon">
      <i class="fas fa-icon"></i>
    </div>
    Section Title
  </h2>
  <!-- Content -->
</section>
```

---

## Cards & Indicators

### KPI Card
```html
<div class="kpi-card">
  <div class="kpi-card__header">
    <div class="kpi-card__icon primary">
      <i class="fas fa-chart-bar"></i>
    </div>
  </div>
  <div class="kpi-card__title">Sales Today</div>
  <div class="kpi-card__value">R$ 1,234</div>
  <div class="kpi-card__change positive">
    ↑ 12% vs yesterday
  </div>
</div>
```

**Icon Colors:**
- `.primary` - Blue background
- `.success` - Green background
- `.warning` - Amber background
- `.danger` - Red background

### Card Indicator
```html
<div class="card-indicator">
  <div class="card-indicator__header">
    <div class="card-indicator__icon-wrapper">
      <i class="fas fa-icon"></i>
    </div>
  </div>
  <p class="card-indicator__label">Revenue</p>
  <h2 class="card-indicator__value">R$ 5,200.00</h2>
  <span class="card-indicator__trend">↑ 15.3%</span>
</div>
```

### Basic Card
```html
<div class="card">
  <h3>Card Title</h3>
  <p>Card content goes here...</p>
</div>
```

---

## Typography

### Headings
```html
<h1>Main Title (2rem)</h1>
<h2>Section Title (1.5rem)</h2>
<h3>Subsection (1.25rem)</h3>
<h4>Heading 4 (1.125rem)</h4>
<h5>Heading 5 (1rem)</h5>
<h6>Heading 6 (1rem)</h6>
```

### Text Classes
```html
<p class="text-primary">Primary text</p>
<p class="text-muted">Muted text (gray-500)</p>
<p class="text-small">Small text (0.85rem)</p>
```

---

## Buttons

### Button Variants
```html
<!-- Primary Button -->
<button class="btn btn--primary">
  <i class="fas fa-icon"></i> Action
</button>

<!-- Secondary -->
<button class="btn btn--secondary">Cancel</button>

<!-- Success -->
<button class="btn btn--success">Confirm</button>

<!-- Danger -->
<button class="btn btn--danger">Delete</button>

<!-- Ghost/Outline -->
<button class="btn btn--ghost">Learn More</button>
```

### Button Sizes
```html
<button class="btn btn--sm">Small</button>
<button class="btn">Default</button>
<button class="btn btn--lg">Large</button>
<button class="btn btn--block">Full Width</button>
```

### Button States
```html
<button class="btn btn--primary" disabled>Disabled</button>
```

---

## Badges & Status

### Status Badges
```html
<span class="status-badge status-badge--active">Active</span>
<span class="status-badge status-badge--pending">Pending</span>
<span class="status-badge status-badge--inactive">Inactive</span>
<span class="status-badge status-badge--error">Error</span>
```

### Regular Badges
```html
<span class="badge--primary">Primary</span>
<span class="badge--success">Success</span>
<span class="badge--warning">Warning</span>
<span class="badge--danger">Danger</span>
```

---

## Forms & Inputs

### Form Group
```html
<div class="form-group">
  <label class="form-label">Email Address</label>
  <input type="email" class="form-input" placeholder="user@example.com" />
</div>
```

### Input Types
```html
<input class="form-input" type="text" placeholder="Text input" />
<input class="form-input" type="number" placeholder="Number" />
<textarea class="form-textarea" placeholder="Message"></textarea>
<select class="form-select">
  <option>Option 1</option>
  <option>Option 2</option>
</select>
```

### Input States
```html
<input class="form-input" placeholder="Default" />
<input class="form-input" value="Text" />
<input class="form-input" disabled placeholder="Disabled" />
<input class="form-input" style="border-color: var(--danger);" />
```

---

## Tables

### Table Wrapper
```html
<div class="table-wrapper">
  <table class="table">
    <thead>
      <tr>
        <th>Column 1</th>
        <th>Column 2</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Data 1</td>
        <td>Data 2</td>
      </tr>
    </tbody>
  </table>
</div>
```

### Table with Actions
```html
<table class="table">
  <tbody>
    <tr>
      <td>Product Name</td>
      <td>
        <a href="#" class="btn btn--sm btn--ghost">Edit</a>
        <button class="btn btn--sm btn--ghost" style="color: var(--danger);">Delete</button>
      </td>
    </tr>
  </tbody>
</table>
```

---

## Alerts & Notifications

### Alert Types
```html
<div class="alert alert--primary">
  <div class="alert__icon">
    <i class="fas fa-info-circle"></i>
  </div>
  <div class="alert__content">
    <div class="alert__title">Information</div>
    <p>This is an informational message.</p>
  </div>
</div>

<div class="alert alert--success">
  <i class="fas fa-check-circle"></i> Success message
</div>

<div class="alert alert--warning">
  <i class="fas fa-exclamation-circle"></i> Warning message
</div>

<div class="alert alert--danger">
  <i class="fas fa-times-circle"></i> Error message
</div>
```

---

## Empty States

### Empty State Component
```html
<div class="empty-state">
  <div class="empty-state__icon">
    <i class="fas fa-box"></i>
  </div>
  <h3 class="empty-state__title">No Products Found</h3>
  <p class="empty-state__text">Start by adding your first product to get started.</p>
  <button class="btn btn--primary">Add Product</button>
</div>
```

---

## Colors & Variables

### CSS Variables (Available in all components)

#### Colors
```css
:root {
  --primary: #3b82f6;           /* Blue */
  --primary-light: #60a5fa;
  --primary-dark: #1e40af;
  --secondary: #10b981;
  --success: #10b981;            /* Green */
  --warning: #f59e0b;            /* Amber */
  --danger: #ef4444;             /* Red */
  --info: #3b82f6;
}
```

#### Gray Scale
```css
--gray-50: #f9fafb;    /* Lightest */
--gray-100: #f3f4f6;
--gray-200: #e5e7eb;
--gray-300: #d1d5db;
--gray-400: #9ca3af;
--gray-500: #6b7280;
--gray-600: #4b5563;
--gray-700: #374151;
--gray-800: #1f2937;
--gray-900: #111827;   /* Darkest */
```

#### Spacing
```css
--spacing-xs: 0.25rem;   /* 4px */
--spacing-sm: 0.5rem;    /* 8px */
--spacing-md: 1rem;      /* 16px */
--spacing-lg: 1.5rem;    /* 24px */
--spacing-xl: 2rem;      /* 32px */
--spacing-2xl: 3rem;     /* 48px */
```

#### Shadows
```css
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
```

#### Border Radius
```css
--radius-sm: 0.375rem;   /* 6px */
--radius-md: 0.5rem;     /* 8px */
--radius-lg: 0.75rem;    /* 12px */
```

### Using Variables
```html
<!-- Spacing -->
<div style="padding: var(--spacing-lg);"><!-- 24px --></div>
<div style="margin: var(--spacing-xl) 0;"><!-- 32px top/bottom --></div>

<!-- Colors -->
<div style="background: var(--primary); color: white;">Primary</div>
<div style="color: var(--gray-600);">Muted text</div>

<!-- Shadows -->
<div style="box-shadow: var(--shadow-md);">Elevated</div>

<!-- Border Radius -->
<div style="border-radius: var(--radius-lg);">Rounded</div>
```

---

## Font Awesome Icon Reference

### Common Icons Used

| Icon | Code | Usage |
|------|------|-------|
| Dashboard | `fas fa-chart-line` | Main dashboard |
| Bot/AI | `fas fa-robot` | AI assistant |
| Box | `fas fa-box` | Inventory |
| Credit Card | `fas fa-credit-card` | Payments |
| Users | `fas fa-users` | Clients |
| Users Cog | `fas fa-users-cog` | Employee management |
| List | `fas fa-list` | History/Logs |
| File | `fas fa-file-alt` | Reports |
| Cog | `fas fa-cog` | Settings |
| Plus | `fas fa-plus` | Add/Create |
| Edit | `fas fa-edit` | Edit |
| Trash | `fas fa-trash` | Delete |
| Bell | `fas fa-bell` | Notifications |
| Check Circle | `fas fa-check-circle` | Success |
| Error/X Circle | `fas fa-times-circle` | Error |
| Info Circle | `fas fa-info-circle` | Info |
| Exclamation Triangle | `fas fa-exclamation-triangle` | Warning |
| Lock | `fas fa-lock` | Security |

### Icon Sizing
```html
<i class="fas fa-icon"></i>           <!-- Normal (auto-inherits font-size) -->
<i class="fas fa-icon" style="font-size: 1.25rem;"></i>  <!-- Larger -->
<i class="fas fa-icon" style="font-size: 3rem;"></i>     <!-- Large (empty state) -->
```

---

## Utility Classes

### Margin & Padding
```html
<div class="mb-md">Margin bottom medium (16px)</div>
<div class="mb-lg">Margin bottom large (24px)</div>
<div class="mb-xl">Margin bottom extra large (32px)</div>
<div class="mt-md">Margin top medium (16px)</div>
```

### Flexbox Utilities
```html
<div class="flex">Flex container with center alignment</div>
<div class="flex gap-md">Flex with 16px gap</div>
<div class="flex gap-lg">Flex with 24px gap</div>
<div class="flex--mobile-stack">Flex that stacks on mobile</div>
```

### Grid
```html
<div class="grid">Auto-responsive grid (250px min per column)</div>
```

---

## Responsive Design

### Breakpoints
```css
/* Mobile First Approach */
@media (max-width: 768px) { /* Tablet */ }
@media (max-width: 480px) { /* Mobile */ }
```

### Mobile Considerations
- Sidebar becomes modal/overlay on mobile
- Grid becomes single column
- Padding reduced
- Typography scales down
- Buttons take full width if needed

---

## Best Practices

### ✅ Do's
- Use CSS classes instead of inline styles
- Leverage CSS variables for consistency
- Use semantic HTML tags
- Include Font Awesome icons for visual clarity
- Keep components self-contained
- Use spacing variables for consistent gaps

### ❌ Don'ts
- Avoid mixing inline styles with classes
- Don't hardcode colors (use CSS variables)
- Avoid custom button styling (use btn classes)
- Don't use emojis (use Font Awesome icons)
- Avoid component-specific custom CSS
- Don't break 12-column/responsive grid structure

---

## Component Examples

### Dashboard KPI Section
```html
<section class="page-section">
  <h2 class="page-section__title">
    <div class="page-section__title-icon">
      <i class="fas fa-chart-bar"></i>
    </div>
    Today's Metrics
  </h2>
  
  <div class="kpi-grid">
    <div class="kpi-card">
      <div class="kpi-card__header">
        <div class="kpi-card__icon success">
          <i class="fas fa-money-bill-wave"></i>
        </div>
      </div>
      <div class="kpi-card__title">Revenue</div>
      <div class="kpi-card__value">R$ 8,420.50</div>
      <div class="kpi-card__change positive">↑ 8.2%</div>
    </div>
    
    <!-- More KPI cards -->
  </div>
</section>
```

### Settings Form
```html
<div class="card">
  <h3>Account Settings</h3>
  
  <form>
    <div class="form-group">
      <label class="form-label">Full Name</label>
      <input class="form-input" type="text" value="John Doe" />
    </div>
    
    <div class="form-group">
      <label class="form-label">Email</label>
      <input class="form-input" type="email" value="john@example.com" />
    </div>
    
    <div class="form-group">
      <button type="submit" class="btn btn--primary">Save Changes</button>
      <button type="reset" class="btn btn--secondary">Cancel</button>
    </div>
  </form>
</div>
```

---

**Last Updated**: Session Atual  
**Version**: 1.0  
**Status**: ✅ Ready for Use
