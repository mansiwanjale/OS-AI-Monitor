const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const axios = require('axios');

// Create the main window
function createWindow() {
    const win = new BrowserWindow({
        width: 1000,
        height: 700,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'), // Linking the preload script
        }
    });

    win.loadFile('index.html'); // Load the HTML file (or replace with your local Flask URL)
    // win.webContents.openDevTools(); // Uncomment this line for debugging
}

// ========================== IPC Communication Handlers ========================== //

// Generic API call handler function
async function callAPI(method, url, data = null) {
    try {
        const options = {
            method,
            url: `http://127.0.0.1:5000${url}`, // Flask backend URL
            data,
        };
        const response = await axios(options);
        return response.data; // Return API response data
    } catch (error) {
        console.error(`API call error at ${url}:`, error.message);
        throw new Error(error.message); // Throw an error if API call fails
    }
}

// Handle chatbot communication (sending messages and getting a response)
ipcMain.handle('send-to-chatbot', async (event, userMessage) => {
    const data = await callAPI('POST', '/api/chatbot', { message: userMessage });
    return data.reply || "No response from chatbot."; // Return chatbot reply or default message
});

// Handle cleanup scan request (fetching a list of junk files to clean)
ipcMain.handle('scan-cleanup', async () => {
    const data = await callAPI('GET', '/api/scan');
    return data.files || []; // Return the list of junk files (or empty array)
});

// Handle delete selected cleanup files request (delete files passed in 'paths')
ipcMain.handle('delete-cleanup', async (event, paths) => {
    const data = await callAPI('POST', '/api/delete', { paths });
    if (data.status === 'success') {
        console.log(`Deleted ${data.deleted.length} files.`); // Log deletion success
        return data; // Return deletion status and details
    }
    return { status: 'error', message: 'Failed to delete files.' }; // Return error if deletion fails
});

// ========================== App Event Listeners ========================== //

// Initialize app when ready
app.whenReady().then(() => {
    createWindow();

    // Create window if none exists (macOS behavior)
    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

// Quit app when all windows are closed (non-macOS behavior)
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});
