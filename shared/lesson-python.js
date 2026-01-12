// Interactive Python Lesson JavaScript
// Shared functionality for all Python lessons

// Pyodide setup for lessons
let pyodideReadyPromise = loadPyodide();

async function initializeLessonPython() {
  let pyodide = await pyodideReadyPromise;

  // NotWorking
  // Load extra Python libraries for use in lessons
  // Add more package names to this array as needed
  // await pyodide.loadPackage(["numpy", "matplotlib", "seaborn"]);
  // Example: await pyodide.loadPackage(["scipy", "pandas"]);



  // Initialize all terminals (supports up to 10 terminals)
  for (let i = 1; i <= 10; i++) {
    const terminal = document.getElementById(`lesson-terminal-${i}`);
    if (terminal) {
      terminal.innerHTML = '<div class="python-prompt">>>> </div><div class="python-output">Python interpreter ready! Type your code above.</div>';
    }
  }

  return pyodide;
}

async function runLessonCode(terminalId) {
  let pyodide = await pyodideReadyPromise;
  let code = document.getElementById(`lesson-input-${terminalId}`).value;
  let terminal = document.getElementById(`lesson-terminal-${terminalId}`);
  
  if (!code.trim()) {
    addToLessonTerminal(terminalId, '<div class="python-error">Please enter some Python code first!</div>');
    return;
  }
  
  // Add the code to terminal
  addToLessonTerminal(terminalId, `<div class="python-prompt">>>> </div><div style="color: white;">${escapeHtml(code)}</div>`);
  
  try {
    // Capture stdout
    pyodide.runPython(`
      import sys
      from io import StringIO
      old_stdout = sys.stdout
      sys.stdout = StringIO()
    `);
    
    // Run the user's code
    let result = pyodide.runPython(code);
    
    // Get the output
    let stdout = pyodide.runPython("sys.stdout.getvalue()");
    pyodide.runPython("sys.stdout = old_stdout");
    
    // Display output
    if (stdout) {
      addToLessonTerminal(terminalId, `<div class="python-output">${escapeHtml(stdout)}</div>`);
    }
    
    if (result !== undefined && !stdout) {
      addToLessonTerminal(terminalId, `<div class="python-output">${escapeHtml(String(result))}</div>`);
    }
    
  } catch (err) {
    addToLessonTerminal(terminalId, `<div class="python-error">Error: ${escapeHtml(err.message)}</div>`);
  }
  
  // Scroll to bottom
  terminal.scrollTop = terminal.scrollHeight;
}

function loadExample(terminalId, code) {
  document.getElementById(`lesson-input-${terminalId}`).value = code;
}

function clearLessonTerminal(terminalId) {
  document.getElementById(`lesson-terminal-${terminalId}`).innerHTML = '<div class="python-prompt">>>> </div><div class="python-output">Terminal cleared. Ready for new code!</div>';
}

function addToLessonTerminal(terminalId, content) {
  let terminal = document.getElementById(`lesson-terminal-${terminalId}`);
  terminal.innerHTML += content;
  terminal.scrollTop = terminal.scrollHeight;
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// Auto-run code if specified in data attribute
function autoRunExample(terminalId) {
  const terminal = document.getElementById(`lesson-terminal-${terminalId}`);
  const autoCode = terminal.getAttribute('data-autorun');
  if (autoCode) {
    document.getElementById(`lesson-input-${terminalId}`).value = autoCode;
    runLessonCode(terminalId);
  }
}

// Enhanced keyboard shortcuts and interactions
function setupLessonInteractions() {
  // Handle keyboard shortcuts
  const textareas = document.querySelectorAll('.lesson-input');
  textareas.forEach((textarea, index) => {
    textarea.addEventListener('keydown', function(e) {
      if (e.ctrlKey && e.key === 'Enter') {
        e.preventDefault();
        runLessonCode(index + 1);
      }
      
      // Handle tab for indentation
      if (e.key === 'Tab') {
        e.preventDefault();
        const start = this.selectionStart;
        const end = this.selectionEnd;
        this.value = this.value.substring(0, start) + '    ' + this.value.substring(end);
        this.selectionStart = this.selectionEnd = start + 4;
      }
    });
  });

  // Add copy button functionality
  document.querySelectorAll('.copy-output-btn').forEach(button => {
    button.addEventListener('click', function() {
      const terminalId = this.getAttribute('data-terminal');
      const terminal = document.getElementById(`lesson-terminal-${terminalId}`);
      const outputText = terminal.innerText;
      navigator.clipboard.writeText(outputText).then(() => {
        this.textContent = '✅ Copied!';
        setTimeout(() => {
          this.textContent = '📋 Copy Output';
        }, 2000);
      });
    });
  });

  // Auto-run examples on page load if specified
  for (let i = 1; i <= 10; i++) {
    autoRunExample(i);
  }
}

// Font size adjustment functions
function increaseFontSize() {
  document.body.classList.remove('lesson-small-font');
  document.body.classList.add('lesson-large-font');
}

function decreaseFontSize() {
  document.body.classList.remove('lesson-large-font');
  document.body.classList.add('lesson-small-font');
}

function resetFontSize() {
  document.body.classList.remove('lesson-large-font', 'lesson-small-font');
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
  initializeLessonPython();
  setupLessonInteractions();
});

// Export functions for use in individual lessons
window.LessonPython = {
  runLessonCode,
  loadExample,
  clearLessonTerminal,
  increaseFontSize,
  decreaseFontSize,
  resetFontSize,
  initializeLessonPython
};
