# NLP Debug UI - Architecture Documentation

## Overview

The NLP Debug UI is a React-based web application designed to test and debug the OneTappe NLP API for processing multilingual WhatsApp commands. The application provides a user-friendly interface for sending commands to the API, visualizing the responses, and analyzing the NLP results.

## Project Structure

```
debug-nlp-ui/
├── public/                 # Static assets
│   ├── index.html          # HTML entry point
│   └── manifest.json       # Web app manifest
├── src/                    # Source code
│   ├── components/         # React components
│   │   ├── ErrorDisplay.js     # Error message component
│   │   ├── ExampleResponse.js  # API format examples
│   │   ├── Footer.js           # Application footer
│   │   ├── LoadingSpinner.js   # Loading indicator
│   │   ├── NLPForm.js          # Command input form
│   │   ├── ResultDisplay.js    # NLP analysis results
│   │   ├── TestCommands.js     # Example command selector
│   │   └── WhatsAppPreview.js  # WhatsApp chat preview
│   ├── services/          # API services
│   │   └── api.js         # API integration
│   ├── utils/             # Utility functions and constants
│   │   ├── constants.js   # Application constants
│   │   └── theme.js       # Theme and styling constants
│   ├── App.js             # Main application component
│   ├── index.js           # JavaScript entry point
│   └── index.css          # Global styles
├── .gitignore             # Git ignore file
├── ARCHITECTURE.md        # This architecture documentation
├── package.json           # Project dependencies
├── README.md              # Project documentation
├── setup.sh               # Setup script
├── tailwind.config.js     # Tailwind CSS configuration
└── postcss.config.js      # PostCSS configuration
```

## Component Architecture

### App.js

The main application component that orchestrates the UI and manages the application state. It handles:

- API health checking
- Command submission
- State management for loading, errors, and results
- Layout and component composition

### Key Components

1. **NLPForm**: Handles user input for WhatsApp commands and language selection.

2. **WhatsAppPreview**: Displays a visual representation of how the command and response would appear in a WhatsApp chat.

3. **ResultDisplay**: Shows the NLP analysis results, including detected language, intent, entities, and confidence scores.

4. **TestCommands**: Provides a selection of example commands for testing different scenarios.

5. **ExampleResponse**: Shows the API request and response format for documentation purposes.

6. **ErrorDisplay**: Displays API errors with a retry option.

7. **LoadingSpinner**: Visual indicator for loading states.

8. **Footer**: Contains project information and utility links.

## State Management

The application uses React's built-in state management with hooks:

- `useState` for component-level state
- `useEffect` for side effects like API calls
- `useRef` for accessing child component methods
- `forwardRef` and `useImperativeHandle` for exposing child methods to parent components

## API Integration

The application communicates with the NLP API through the `api.js` service, which provides:

- `processCommand`: Sends WhatsApp commands to the API
- `checkHealth`: Verifies the API is online and accessible

## Styling

The application uses Tailwind CSS for styling with:

- Responsive design for mobile and desktop
- Custom color scheme for WhatsApp-like interface
- Consistent spacing and typography

## Constants and Configuration

Application constants are centralized in:

- `constants.js`: API endpoints, language options, UI text
- `theme.js`: Colors, spacing, typography, and other design tokens

## Error Handling

The application includes comprehensive error handling:

- API connectivity errors
- Command processing errors
- Visual feedback for error states
- Retry mechanisms for API connection issues

## Future Improvements

1. **State Management**: For larger scale, consider using Context API or Redux
2. **Testing**: Add unit and integration tests
3. **Internationalization**: Add support for UI in multiple languages
4. **Persistence**: Add local storage for command history
5. **Advanced Visualization**: Add charts for confidence scores and entity recognition