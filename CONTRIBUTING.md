# Contributing to OpenAI & Azure Text-to-Speech Application

Thank you for your interest in contributing to the OpenAI & Azure Text-to-Speech Application! Here’s a guide to help you get started, including setup instructions, style guidelines, and testing information.

---

## Getting Started

1. **Fork the Repository**:
   - Click on the "Fork" button at the top right of the repository page.
   - This creates a copy of the repository under your GitHub account.

2. **Clone Your Fork**:
   - Open a terminal and clone your fork:
     ```bash
     git clone https://github.com/<your-username>/openai_azure_text2speech.git
     cd openai_azure_text2speech
     ```

3. **Create a Branch**:
   - Create a branch for your feature or bug fix. Using a branch keeps the `main` branch stable.
     ```bash
     git checkout -b feature/your-feature-name
     ```

4. **Set Up Environment Variables**:
   - Ensure you have a `.env` file in the root directory with your API keys:
     ```plaintext
     OPENAI_API_KEY=YOUR_OPENAI_API_KEY
     AZURE_API_KEY=YOUR_AZURE_API_KEY
     ```

5. **Install Dependencies**:
   - Install required dependencies in a virtual environment:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     ```

---

## Contribution Workflow

1. **Make Your Changes**:
   - Write clear, well-documented code.
   - Ensure your changes follow the coding standards outlined below.

2. **Write Tests**:
   - Write tests for new functionality or bug fixes to maintain code quality. 
   - We recommend using the `pytest` framework:
     ```bash
     pip install pytest
     pytest
     ```

3. **Check for Formatting Issues**:
   - Ensure code is formatted according to PEP 8 using `flake8` or `black`:
     ```bash
     pip install flake8 black
     flake8 .
     black .
     ```

4. **Commit Changes**:
   - Use descriptive commit messages. Aim to keep each commit focused and purposeful.
     ```bash
     git add .
     git commit -m "Add feature: customizable text truncation"
     ```

5. **Push Changes**:
   - Push the changes to your branch on GitHub:
     ```bash
     git push origin feature/your-feature-name
     ```

6. **Open a Pull Request (PR)**:
   - Navigate to the original repository on GitHub and open a new PR from your branch.
   - Include a title, a description of changes, and any additional details that help explain the purpose and context of your work.

---

## Style Guide

Please ensure your contributions align with the following coding standards:

- **Python Style**: Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code.
- **Docstrings**: Include clear docstrings for each function and class using the Google style.
- **Comments**: Use comments to explain complex logic or workflows within the code.
- **Commit Messages**: Use descriptive messages (e.g., "Fix Azure API error handling").
- **File Organization**: Maintain modularity by creating new files for significant features or logically separate functionality.

---

## Testing Guidelines

Testing is essential to ensure that all features work as expected and that changes do not introduce bugs. Here are some testing guidelines:

- **Unit Tests**: Write unit tests for any new function or feature.
- **Functional Tests**: Test the functionality as part of the app's workflow, especially any user interface changes.
- **Run Tests Before PR**: Before creating a pull request, make sure all tests pass:
  ```bash
  pytest
  ```

---

## Additional Resources

- **Documentation**: Familiarize yourself with `app.py` and `README.md` to understand the app's workflow and dependencies.
- **Questions**: If you have any questions, please open an issue or reach out to the maintainers.

Thank you for contributing to this project! Your effort helps improve and grow the OpenAI & Azure Text-to-Speech Application.
```

This **CONTRIBUTING.md** provides a step-by-step guide for new contributors, ensuring they understand the repository's structure and follow best practices for coding and testing. It also includes instructions on setting up the environment, maintaining code style, and performing testing to ensure the quality of contributions.