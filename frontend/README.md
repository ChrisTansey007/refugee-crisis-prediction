# Migration Forecasting System - Frontend

React-based frontend application for the Migration Forecasting System.

## Tech Stack

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **TailwindCSS** - Utility-first CSS framework
- **Recharts** - Data visualization
- **Leaflet** - Interactive maps
- **Axios** - HTTP client
- **Lucide React** - Icon library
- **Radix UI** - Accessible component primitives

## Features

- **Dashboard** - System overview with stats and charts
- **Map View** - Geographic visualization of displacement data
- **Data Sources** - Manage external data integrations
- **Models** - ML model management and comparison
- **Predictions** - View forecasts with confidence intervals
- **Reports** - Generate and export analysis reports

## Getting Started

### Prerequisites

- Node.js 18+ and npm

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

The application will be available at `http://localhost:3000`.

### Build

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── Layout.jsx          # Main layout with navigation
│   ├── pages/
│   │   ├── Dashboard.jsx       # Dashboard page
│   │   ├── MapView.jsx         # Interactive map
│   │   ├── DataSources.jsx     # Data source management
│   │   ├── Models.jsx          # ML model management
│   │   ├── Predictions.jsx     # Forecast visualization
│   │   └── Reports.jsx         # Report generation
│   ├── App.jsx                 # Main app component
│   ├── main.jsx                # Entry point
│   └── index.css               # Global styles
├── index.html
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
└── package.json
```

## API Integration

The frontend connects to the backend API at `http://localhost:8000`. API proxy is configured in `vite.config.js`.

### Key Endpoints

- `/api/v1/etl/status` - Get system status
- `/api/v1/ingest/*` - Data ingestion endpoints
- `/api/v1/ml/models` - Model management
- `/api/v1/ml/predict` - Make predictions
- `/api/v1/ml/explain/*` - Model explainability

## Styling

The application uses TailwindCSS with a custom color palette:

- **Primary**: Blue shades for main actions
- **Danger**: Red shades for warnings/alerts
- **Success**: Green for positive states
- **Warning**: Yellow for caution states

## Accessibility

- Semantic HTML elements
- ARIA labels where needed
- Keyboard navigation support
- Color contrast compliance

## Performance

- Code splitting with React Router
- Lazy loading of components
- Optimized bundle size with Vite
- Responsive images and assets

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## Contributing

Follow the project's coding standards and submit PRs for review.

## License

See main project LICENSE file.
