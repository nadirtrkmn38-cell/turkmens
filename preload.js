/**
 * Turkmen'S - Preload (güvenli köprü)
 */
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('turkmens', {
  getVersion: () => ipcRenderer.invoke('app:get-version'),
  getPlatform: () => ipcRenderer.invoke('app:get-platform'),
  quit: () => ipcRenderer.invoke('app:quit'),

  // Auto-update API
  checkForUpdates: () => ipcRenderer.invoke('update:check'),
  installUpdate: () => ipcRenderer.invoke('update:install'),

  // Update event'leri
  onUpdateChecking: (cb) => {
    ipcRenderer.removeAllListeners('update:checking');
    ipcRenderer.on('update:checking', () => cb());
  },
  onUpdateAvailable: (cb) => {
    ipcRenderer.removeAllListeners('update:available');
    ipcRenderer.on('update:available', (_e, info) => cb(info));
  },
  onUpdateProgress: (cb) => {
    ipcRenderer.removeAllListeners('update:progress');
    ipcRenderer.on('update:progress', (_e, info) => cb(info));
  },
  onUpdateDownloaded: (cb) => {
    ipcRenderer.removeAllListeners('update:downloaded');
    ipcRenderer.on('update:downloaded', (_e, info) => cb(info));
  },
  onUpdateError: (cb) => {
    ipcRenderer.removeAllListeners('update:error');
    ipcRenderer.on('update:error', (_e, msg) => cb(msg));
  }
});
