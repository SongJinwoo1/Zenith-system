// ... (Your Firebase Config and existing functions)

function showFallbackEditor() {
    const container = document.getElementById('editor-container');
    const fallback = document.getElementById('editor-fallback');

    if (container && fallback) {
        container.innerHTML = '';
        fallback.style.display = 'block';
        container.appendChild(fallback);

        // Create textarea fallback
        const textarea = document.createElement('textarea');
        textarea.id = 'fallback-textarea';
        // --- MODIFIED FOR VISIBILITY ---
        textarea.style.width = '100%';
        textarea.style.height = '100%';
        textarea.style.background = '#1e1e1e';
        textarea.style.color = '#00f2ff'; // Clear Cyan Text
        textarea.style.border = 'none';
        textarea.style.padding = '15px';
        textarea.style.fontFamily = 'Consolas, monospace';
        textarea.style.fontSize = '16px';
        textarea.style.resize = 'none';
        textarea.style.caretColor = 'white';
        // -------------------------------
        textarea.value = '# Monaco failed to load\n# Using fallback editor\nprint("Hello World")';

        container.appendChild(textarea);

        // Override getValue for compatibility
        editor = {
            getValue: () => textarea.value,
            setValue: (v) => textarea.value = v,
            layout: () => {}
        };

        isEditorReady = true;
        document.getElementById('run-btn').disabled = false;
        document.getElementById('run-btn').innerHTML = '▶️ EXECUTE CODE';
    }
}

// ... (The rest of your code remains exactly as it was)
