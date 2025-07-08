# OneTappe NLP Debug UI

A responsive web interface for testing and debugging the OneTappe multilingual NLP API. This tool allows you to simulate WhatsApp inputs and view the NLP processing results in real-time.

## Features

- WhatsApp-style chat interface for testing commands
- Support for multiple languages (English, Hindi, Hinglish)
- Real-time API status monitoring
- Detailed display of NLP analysis results (intent, entities, confidence scores)
- Responsive design for desktop and mobile devices
- Example commands for quick testing
- API format documentation
- Comprehensive error handling with retry options

## Prerequisites

- Node.js (v14 or higher)
- NPM or Yarn
- OneTappe NLP API running at http://localhost:5000

## Project Structure

The application follows a component-based architecture using React:

```
src/
├── components/         # React components
│   ├── ErrorDisplay.js     # Error message component
│   ├── ExampleResponse.js  # API format examples
│   ├── Footer.js           # Application footer
│   ├── LoadingSpinner.js   # Loading indicator
│   ├── NLPForm.js          # Command input form
│   ├── ResultDisplay.js    # NLP analysis results
│   ├── TestCommands.js     # Example command selector
│   └── WhatsAppPreview.js  # WhatsApp chat preview
├── services/           # API services
│   └── api.js          # API integration
├── utils/              # Utility functions and constants
│   ├── analytics.js    # Usage tracking utilities
│   ├── constants.js    # Application constants
│   ├── formatters.js   # Data formatting utilities
│   ├── responsive.js   # Responsive design utilities
│   ├── theme.js        # Theme and styling constants
│   └── validation.js   # Form validation utilities
├── App.js              # Main application component
└── index.js            # Entry point
```

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed documentation.

## Setup

1. Install dependencies:

```bash
cd frontend/debug-nlp-ui
npm install
```

2. Start the development server:

```bash
npm start
```

3. Open your browser and navigate to http://localhost:3000

## API Integration

This UI connects to the OneTappe NLP API at `http://localhost:5000/api/process`. Make sure the API server is running before using this interface.

API calls are handled through the `src/services/api.js` module, which provides:

- `processCommand(command, language)`: Process a WhatsApp command
- `checkHealth()`: Check API availability

## Configuration

Application constants are centralized in `src/utils/constants.js`, including:

- API endpoints
- Language options
- UI text
- Status indicators

## Styling

The application uses Tailwind CSS for styling with a custom theme defined in `src/utils/theme.js`.

## Available Commands

Test the interface with commands like:

- "Show my inventory" (English)
- "मेरा स्टॉक दिखाओ" (Hindi)
- "Order status dikhao" (Hinglish)
- "Add 10 units of product ABC123" (English)
- "Report for last month" (English)

## Development

This project was built with:

- React.js
- Tailwind CSS
- Axios for API requests

## Usage

### Testing Commands

1. Enter a WhatsApp command in the input field
2. Select the language of the command
3. Click "Process Command" to send it to the API
4. View the results in the WhatsApp Preview and NLP Analysis sections

### Using Example Commands

1. Click on any example command in the Test Commands section
2. The command will be automatically populated in the input field
3. Click "Process Command" to test it

### Checking API Status

- The API status indicator in the header shows if the API is online
- Click "Check API Status" in the footer to manually check API health

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Submit a pull request