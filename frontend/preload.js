const { contextBridge, ipcRenderer } = require('electron');

// Expose API methods to the renderer process
contextBridge.exposeInMainWorld('electronAPI', {
    // Chatbot Communication
    sendToChatbot: async (message) => {
        try {
            const reply = await ipcRenderer.invoke('send-to-chatbot', message);
            return reply;
        } catch (error) {
            console.error('Error in chatbot communication:', error);
            return 'Error communicating with the chatbot.'; // Return error message if communication fails
        }
    },

    // Cleanup Scan (find junk files)
    scanCleanup: async () => {
        try {
            const files = await ipcRenderer.invoke('scan-cleanup');
            return files; // Return list of found junk files
        } catch (error) {
            console.error('Error scanning for cleanup:', error);
            return []; // Return empty array if scanning fails
        }
    },

    // Cleanup Delete (delete junk files)
    deleteCleanup: async (paths) => {
        try {
            const result = await ipcRenderer.invoke('delete-cleanup', paths);
            return result; // Return deletion status and result
        } catch (error) {
            console.error('Error deleting cleanup files:', error);
            return { status: 'error', message: 'Failed to delete files.' }; // Return error if deletion fails
        }
    },
   
});
