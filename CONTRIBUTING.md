# Contributing to QuantJourney Trading Calendar

Thank you for your interest in contributing to the QuantJourney Trading Calendar! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please be respectful and considerate of others.

## How to Contribute

### 1. Fork the Repository
Fork the repository to your GitHub account.

### 2. Clone Your Fork
```bash
git clone https://github.com/yourusername/qj_calendar.git
cd qj_calendar
```

### 3. Create a New Branch
```bash
git checkout -b feature/your-feature-name
```

### 4. Make Your Changes
- Follow PEP 8 style guide for Python code
- Add appropriate docstrings and comments
- Include tests for new features
- Update documentation as needed

### 5. Add Exchange Calendars
When adding a new exchange calendar:
1. Create a new JSON file in `exchange_calendars/`
2. Follow the existing format
3. Include all relevant holidays and special trading days
4. Verify the trading hours and days
5. Add a test case in the unit tests

### 6. Commit Your Changes
```bash
git commit -m "Description of your changes"
```

### 7. Push to Your Fork
```bash
git push origin feature/your-feature-name
```

### 8. Create a Pull Request
1. Go to the original repository
2. Click "New Pull Request"
3. Select your branch
4. Provide a clear description of your changes
5. Submit the pull request

## Development Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
pip install -e .
```

## Testing

Run the unit tests:
```bash
python trading_calendar.py
```

## Documentation

- Keep docstrings up to date
- Update README.md for significant changes
- Add comments for complex logic

## Questions?

If you have any questions, please:
1. Check the existing documentation
2. Open an issue in the repository
3. Contact jakub@quantjourney.pro 