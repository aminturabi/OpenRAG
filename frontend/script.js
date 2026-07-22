document.addEventListener('DOMContentLoaded', () => {
    // -------------------------------------------------------------
    // Application State
    // -------------------------------------------------------------
    const state = {
        activeCollection: localStorage.getItem('ragforge_collection') || localStorage.getItem('openrag_collection') || localStorage.getItem('clarity_rag_collection') || null,
        activeFilename: localStorage.getItem('ragforge_filename') || localStorage.getItem('openrag_filename') || localStorage.getItem('clarity_rag_filename') || null,
        activeChunksCount: localStorage.getItem('ragforge_chunks') || localStorage.getItem('openrag_chunks') || localStorage.getItem('clarity_rag_chunks') || 0,
        apiKey: localStorage.getItem('ragforge_groq_api_key') || localStorage.getItem('openrag_groq_api_key') || localStorage.getItem('clarity_groq_api_key') || '',
        topK: parseInt(localStorage.getItem('ragforge_top_k') || localStorage.getItem('openrag_top_k') || localStorage.getItem('clarity_top_k')) || 4,
        messageContexts: {} // Map to store message ID -> context chunks
    };

    // -------------------------------------------------------------
    // DOM Elements
    // -------------------------------------------------------------
    const elements = {
        // Configurations
        apiKeyInput: document.getElementById('apiKey'),
        togglePasswordBtn: document.getElementById('togglePasswordBtn'),
        eyeIcon: document.getElementById('eyeIcon'),
        topKSlider: document.getElementById('topK'),
        topKValue: document.getElementById('topKValue'),
        
        // Upload
        dropzone: document.getElementById('dropzone'),
        fileInput: document.getElementById('fileInput'),
        browseBtn: document.getElementById('browseBtn'),
        uploadProgressContainer: document.getElementById('uploadProgressContainer'),
        progressBarFill: document.getElementById('progressBarFill'),
        progressText: document.getElementById('progressText'),
        progressPercent: document.getElementById('progressPercent'),
        
        // Active Index
        activeDocSection: document.getElementById('activeDocSection'),
        activeDocName: document.getElementById('activeDocName'),
        activeDocChunks: document.getElementById('activeDocChunks'),
        clearIndexBtn: document.getElementById('clearIndexBtn'),
        
        // Chat
        sidebar: document.getElementById('sidebar'),
        sidebarToggle: document.getElementById('sidebarToggle'),
        headerDocStatus: document.getElementById('headerDocStatus'),
        headerDocText: document.getElementById('headerDocText'),
        chatMessages: document.getElementById('chatMessages'),
        welcomeScreen: document.getElementById('welcomeScreen'),
        chatForm: document.getElementById('chatForm'),
        queryInput: document.getElementById('queryInput'),
        sendBtn: document.getElementById('sendBtn'),
        
        // Drawer
        contextDrawer: document.getElementById('contextDrawer'),
        drawerContent: document.getElementById('drawerContent'),
        closeDrawerBtn: document.getElementById('closeDrawerBtn'),
        drawerOverlay: document.getElementById('drawerOverlay')
    };

    // Helper to safely render icons without crashing the script if unpkg is offline
    const safeCreateIcons = () => {
        if (typeof lucide !== 'undefined' && lucide.createIcons) {
            try {
                lucide.createIcons();
            } catch (e) {
                console.error("Lucide creation error:", e);
            }
        }
    };

    safeCreateIcons();

    // -------------------------------------------------------------
    // Initialization
    // -------------------------------------------------------------
    const init = () => {
        // Load API Key if input exists
        if (elements.apiKeyInput && state.apiKey) {
            elements.apiKeyInput.value = state.apiKey;
        }

        // Load Top K
        elements.topKSlider.value = state.topK;
        elements.topKValue.textContent = state.topK;

        // Restore active index if it exists in local storage
        if (state.activeCollection && state.activeFilename) {
            updateActiveIndexUI(true);
        } else {
            updateActiveIndexUI(false);
        }

        setupEventListeners();
    };

    // -------------------------------------------------------------
    // Event Listeners
    // -------------------------------------------------------------
    const setupEventListeners = () => {
        // Toggle Password Visibility if elements exist
        if (elements.togglePasswordBtn && elements.apiKeyInput) {
            elements.togglePasswordBtn.addEventListener('click', () => {
                const isPassword = elements.apiKeyInput.type === 'password';
                elements.apiKeyInput.type = isPassword ? 'text' : 'password';
                elements.eyeIcon.setAttribute('data-lucide', isPassword ? 'eye-off' : 'eye');
                lucide.createIcons({
                    nameAttr: 'data-lucide',
                    attrs: { class: 'field-icon' } // Keeps spacing styled
                });
                elements.eyeIcon.className = ''; 
                elements.eyeIcon.classList.add('lucide', isPassword ? 'lucide-eye-off' : 'lucide-eye');
            });
        }

        // Save API Key if input exists
        if (elements.apiKeyInput) {
            elements.apiKeyInput.addEventListener('input', (e) => {
                state.apiKey = e.target.value.trim();
                localStorage.setItem('ragforge_groq_api_key', state.apiKey);
            });
        }

        // Top K Slider
        elements.topKSlider.addEventListener('input', (e) => {
            state.topK = parseInt(e.target.value);
            elements.topKValue.textContent = state.topK;
            localStorage.setItem('ragforge_top_k', state.topK);
        });

        // Drag & Drop events
        ['dragenter', 'dragover'].forEach(eventName => {
            elements.dropzone.addEventListener(eventName, (e) => {
                e.preventDefault();
                elements.dropzone.classList.add('dragover');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            elements.dropzone.addEventListener(eventName, (e) => {
                e.preventDefault();
                elements.dropzone.classList.remove('dragover');
            }, false);
        });

        elements.dropzone.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            if (files.length > 0) {
                handleFileUpload(files[0]);
            }
        });

        // Click anywhere on dropzone to open file picker
        elements.dropzone.addEventListener('click', () => {
            elements.fileInput.click();
        });

        // Double protection: click directly on browseBtn to open file picker
        elements.browseBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            elements.fileInput.click();
        });

        elements.fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleFileUpload(e.target.files[0]);
            }
        });

        // Clear Index
        elements.clearIndexBtn.addEventListener('click', clearIndex);

        // Sidebar Toggle for Mobile
        elements.sidebarToggle.addEventListener('click', () => {
            elements.sidebar.classList.toggle('open');
            const isOpen = elements.sidebar.classList.contains('open');
            elements.sidebarToggle.querySelector('i').setAttribute('data-lucide', isOpen ? 'x' : 'menu');
            safeCreateIcons();
        });

        // Auto-grow textarea for chat query
        elements.queryInput.addEventListener('input', () => {
            elements.queryInput.style.height = 'auto';
            elements.queryInput.style.height = (elements.queryInput.scrollHeight - 16) + 'px';
        });

        // Submit form on Enter key (Shift + Enter inserts newline)
        elements.queryInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleChatSubmit();
            }
        });

        // Chat Form Submit
        elements.chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            handleChatSubmit();
        });

        // Close Drawer Panel
        elements.closeDrawerBtn.addEventListener('click', closeDrawer);
        elements.drawerOverlay.addEventListener('click', closeDrawer);
    };

    // -------------------------------------------------------------
    // UI Helpers
    // -------------------------------------------------------------
    const updateActiveIndexUI = (hasIndex) => {
        if (hasIndex) {
            // Enable Inputs
            elements.queryInput.removeAttribute('disabled');
            elements.sendBtn.removeAttribute('disabled');
            elements.queryInput.placeholder = "Ask a question about the active document...";
            
            // Show Active Index Info in Sidebar
            elements.activeDocSection.style.display = 'block';
            elements.activeDocName.textContent = state.activeFilename;
            elements.activeDocChunks.textContent = `${state.activeChunksCount} chunks indexed`;
            
            // Update Chat Header
            elements.headerDocStatus.classList.remove('no-doc');
            elements.headerDocText.textContent = `Active: ${state.activeFilename} (${state.activeChunksCount} chunks)`;
            
            const statusIcon = elements.headerDocStatus.querySelector('.status-info-icon');
            if (statusIcon) {
                const newIcon = document.createElement('i');
                newIcon.className = 'status-info-icon';
                newIcon.setAttribute('data-lucide', 'file-check');
                statusIcon.replaceWith(newIcon);
            }
            
            // Auto focus input
            elements.queryInput.focus();
        } else {
            // Disable Inputs
            elements.queryInput.setAttribute('disabled', 'true');
            elements.sendBtn.setAttribute('disabled', 'true');
            elements.queryInput.placeholder = "Upload a document to start chatting...";
            
            // Hide Sidebar Info
            elements.activeDocSection.style.display = 'none';
            
            // Update Chat Header
            elements.headerDocText.textContent = "No document loaded. Upload a document to start asking questions.";
            
            const statusIcon = elements.headerDocStatus.querySelector('.status-info-icon');
            if (statusIcon) {
                const newIcon = document.createElement('i');
                newIcon.className = 'status-info-icon';
                newIcon.setAttribute('data-lucide', 'info');
                statusIcon.replaceWith(newIcon);
            }
        }
        safeCreateIcons();
    };

    // -------------------------------------------------------------
    // Document Upload & Indexing
    // -------------------------------------------------------------
    const handleFileUpload = (file) => {
        // Reset progress and display
        elements.uploadProgressContainer.style.display = 'block';
        elements.progressBarFill.style.width = '0%';
        elements.progressPercent.textContent = '0%';
        elements.progressText.textContent = 'Preparing file...';

        const formData = new FormData();
        formData.append('file', file);

        // Simulated progress steps during network requests
        let progress = 0;
        const progressInterval = setInterval(() => {
            if (progress < 85) {
                progress += Math.floor(Math.random() * 8) + 1;
                elements.progressBarFill.style.width = `${progress}%`;
                elements.progressPercent.textContent = `${progress}%`;
                if (progress > 30 && progress < 70) {
                    elements.progressText.textContent = 'Parsing and extracting text...';
                } else if (progress >= 70) {
                    elements.progressText.textContent = 'Generating embeddings and index...';
                }
            }
        }, 300);

        fetch('/api/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            clearInterval(progressInterval);
            
            if (data.success) {
                elements.progressBarFill.style.width = '100%';
                elements.progressPercent.textContent = '100%';
                elements.progressText.textContent = 'Completed!';
                
                // Save state
                state.activeCollection = data.collection_name;
                state.activeFilename = data.filename;
                state.activeChunksCount = data.chunks_count;
                
                localStorage.setItem('ragforge_collection', data.collection_name);
                localStorage.setItem('ragforge_filename', data.filename);
                localStorage.setItem('ragforge_chunks', data.chunks_count);
                
                setTimeout(() => {
                    elements.uploadProgressContainer.style.display = 'none';
                    updateActiveIndexUI(true);
                    appendAlertMessage('system', `Successfully indexed document: <strong>${data.filename}</strong>. You can now query it.`, 'success');
                }, 800);
            } else {
                throw new Error(data.error || 'Failed to process document');
            }
        })
        .catch(error => {
            clearInterval(progressInterval);
            elements.uploadProgressContainer.style.display = 'none';
            appendAlertMessage('system', `Upload failed: ${error.message}`, 'error');
            console.error(error);
        });
    };

    // -------------------------------------------------------------
    // Delete/Clear Index
    // -------------------------------------------------------------
    function clearIndex() {
        if (!state.activeCollection) return;
        
        if (!confirm('Are you sure you want to delete the active document index from storage?')) {
            return;
        }

        fetch('/api/clear', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ collection_name: state.activeCollection })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success || data.error) {
                // Wipe local state regardless of server deletion (in case database sync is out of state)
                state.activeCollection = null;
                state.activeFilename = null;
                state.activeChunksCount = 0;
                
                localStorage.removeItem('ragforge_collection');
                localStorage.removeItem('ragforge_filename');
                localStorage.removeItem('ragforge_chunks');
                
                updateActiveIndexUI(false);
                
                // Clear chat messages back to welcome
                elements.chatMessages.innerHTML = '';
                elements.chatMessages.appendChild(elements.welcomeScreen);
                
                appendAlertMessage('system', 'Knowledge base index has been cleared.', 'info');
            }
        })
        .catch(error => {
            console.error('Error clearing collection:', error);
            alert('Failed to clear collection. Check server log.');
        });
    }

    // -------------------------------------------------------------
    // Chat Interactions
    // -------------------------------------------------------------
    const handleChatSubmit = () => {
        const query = elements.queryInput.value.trim();
        if (!query) return;

        // API key will be read from backend environmental variables (.env)

        // Hide welcome screen if showing
        if (elements.welcomeScreen.parentNode) {
            elements.welcomeScreen.remove();
        }

        // Add user message
        appendMessage('user', query);
        
        // Reset query input area
        elements.queryInput.value = '';
        elements.queryInput.style.height = 'auto';

        // Add typing indicator
        const typingIndicator = appendTypingIndicator();
        elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;

        // Perform backend query
        fetch('/api/query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query: query,
                collection_name: state.activeCollection,
                api_key: '',
                top_k: state.topK
            })
        })
        .then(response => response.json())
        .then(data => {
            typingIndicator.remove();
            
            if (data.success) {
                const msgId = appendMessage('assistant', data.answer, data.context);
                if (data.context && data.context.length > 0) {
                    state.messageContexts[msgId] = data.context;
                }
            } else {
                appendAlertMessage('assistant', `Error: ${data.error}`, 'error');
            }
            elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
        })
        .catch(error => {
            typingIndicator.remove();
            appendAlertMessage('assistant', `Failed to contact Flask server: ${error.message}`, 'error');
            elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
        });
    };

    // -------------------------------------------------------------
    // Message Rendering Helpers
    // -------------------------------------------------------------
    const appendMessage = (role, text, context = []) => {
        const msgId = 'msg_' + Date.now() + '_' + Math.random().toString(36).substr(2, 5);
        
        const row = document.createElement('div');
        row.className = `message-row ${role}`;
        
        const avatar = document.createElement('div');
        avatar.className = `message-avatar ${role}`;
        avatar.innerHTML = role === 'user' ? '<i data-lucide="user"></i>' : '<i data-lucide="bot"></i>';
        
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        
        // Add content
        const bodyContent = document.createElement('div');
        bodyContent.className = 'message-body';
        bodyContent.innerHTML = formatMarkdown(text);
        bubble.appendChild(bodyContent);
        
        // Add footer context triggers for assistant
        if (role === 'assistant') {
            const footer = document.createElement('div');
            footer.className = 'message-footer';
            
            if (context && context.length > 0) {
                const btn = document.createElement('div');
                btn.className = 'inspect-context-btn';
                btn.innerHTML = `<i data-lucide="zoom-in" style="width:12px;height:12px;"></i> View Source Grounding (${context.length})`;
                btn.addEventListener('click', () => openContextDrawer(msgId));
                footer.appendChild(btn);
            } else {
                footer.textContent = 'Generated from general LLM space (No doc matches)';
            }
            
            bubble.appendChild(footer);
        }
        
        if (role === 'user') {
            row.appendChild(bubble);
            row.appendChild(avatar);
        } else {
            row.appendChild(avatar);
            row.appendChild(bubble);
        }
        
        elements.chatMessages.appendChild(row);
        safeCreateIcons();
        
        return msgId;
    };

    const appendAlertMessage = (role, text, type = 'info') => {
        const row = document.createElement('div');
        row.className = `message-row ${role}`;
        
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble alert-bubble';
        
        // Styling based on alert type
        let borderStyle = '1px solid var(--border-color)';
        let backgroundStyle = 'rgba(255,255,255,0.03)';
        let colorStyle = 'var(--color-text-main)';
        
        if (type === 'success') {
            borderStyle = '1px solid rgba(16, 185, 129, 0.3)';
            backgroundStyle = 'rgba(16, 185, 129, 0.05)';
            colorStyle = '#a7f3d0';
        } else if (type === 'warning') {
            borderStyle = '1px solid rgba(245, 158, 11, 0.3)';
            backgroundStyle = 'rgba(245, 158, 11, 0.05)';
            colorStyle = '#fde68a';
        } else if (type === 'error') {
            borderStyle = '1px solid rgba(239, 68, 68, 0.3)';
            backgroundStyle = 'rgba(239, 68, 68, 0.05)';
            colorStyle = '#fca5a5';
        }

        bubble.style.border = borderStyle;
        bubble.style.backgroundColor = backgroundStyle;
        bubble.style.color = colorStyle;
        bubble.style.maxWidth = '100%';
        bubble.style.fontSize = '0.85rem';
        bubble.style.borderRadius = 'var(--radius-md)';
        bubble.innerHTML = text;
        
        row.appendChild(bubble);
        elements.chatMessages.appendChild(row);
        elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
    };

    const appendTypingIndicator = () => {
        const row = document.createElement('div');
        row.className = 'message-row assistant';
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar assistant';
        avatar.innerHTML = '<i data-lucide="bot"></i>';
        
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        
        const indicator = document.createElement('div');
        indicator.className = 'typing-indicator';
        indicator.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';
        
        bubble.appendChild(indicator);
        row.appendChild(avatar);
        row.appendChild(bubble);
        
        elements.chatMessages.appendChild(row);
        safeCreateIcons();
        
        return row;
    };

    // Simple Markdown Formatter
    const formatMarkdown = (text) => {
        let formatted = text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;");

        // Code blocks: ```code```
        formatted = formatted.replace(/```([\s\S]+?)```/g, (match, code) => {
            return `<pre><code>${code.trim()}</code></pre>`;
        });

        // Inline code: `code`
        formatted = formatted.replace(/`([^`]+)`/g, '<code>$1</code>');

        // Strong text: **text**
        formatted = formatted.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

        // Lists items: * item or - item
        formatted = formatted.replace(/^\s*[-*]\s+(.+)$/gm, '<li>$1</li>');
        formatted = formatted.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');

        // Paragraphs
        formatted = formatted.replace(/\n\n/g, '</p><p>');
        formatted = `<p>${formatted}</p>`;
        
        // Clean empty tags
        formatted = formatted.replace(/<p><pre>/g, '<pre>').replace(/<\/pre><\/p>/g, '</pre>');
        formatted = formatted.replace(/<p><ul>/g, '<ul>').replace(/<\/ul><\/p>/g, '</ul>');
        formatted = formatted.replace(/<p><\/p>/g, '');

        return formatted;
    };

    // -------------------------------------------------------------
    // Context Drawer Panel Methods
    // -------------------------------------------------------------
    const openContextDrawer = (msgId) => {
        const chunks = state.messageContexts[msgId];
        if (!chunks || chunks.length === 0) return;

        elements.drawerContent.innerHTML = '';
        chunks.forEach((chunk, index) => {
            const card = document.createElement('div');
            card.className = 'chunk-card';
            
            const num = document.createElement('span');
            num.className = 'chunk-index';
            num.textContent = `Match Fragment #${index + 1}`;
            
            const body = document.createElement('div');
            body.className = 'chunk-text';
            body.textContent = chunk;
            
            card.appendChild(num);
            card.appendChild(body);
            elements.drawerContent.appendChild(card);
        });

        elements.contextDrawer.classList.add('open');
        elements.drawerOverlay.classList.add('active');
    };

    function closeDrawer() {
        elements.contextDrawer.classList.remove('open');
        elements.drawerOverlay.classList.remove('active');
    }

    // Fire application start
    init();
});
