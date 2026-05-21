/**
 * Turkmen'S - Electron Ana Süreç
 * Auto-update entegrasyonu ile production-ready
 */
'use strict';

const { app, BrowserWindow, Menu, shell, ipcMain, dialog } = require('electron');
const path = require('path');
const log = require('electron-log');
const { autoUpdater } = require('electron-updater');

// --- Loglama yapılandırması ---
log.transports.file.level = 'info';
log.transports.console.level = 'info';
log.info(`Turkmen'S başlatılıyor v${app.getVersion()}`);

// --- Auto-updater yapılandırması ---
autoUpdater.logger = log;
autoUpdater.autoDownload = true;
autoUpdater.autoInstallOnAppQuit = true;
autoUpdater.allowDowngrade = false;

// --- Tek instance kilidi (çift açılmayı engelle) ---
const gotLock = app.requestSingleInstanceLock();
if (!gotLock) {
  log.info('Uygulama zaten açık, çıkılıyor.');
  app.quit();
}

app.on('second-instance', () => {
  if (mainWindow) {
    if (mainWindow.isMinimized()) mainWindow.restore();
    mainWindow.focus();
  }
});

let mainWindow = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 800,
    minWidth: 940,
    minHeight: 600,
    backgroundColor: '#202225',
    title: "Turkmen'S",
    icon: path.join(__dirname, 'build', 'icon.ico'),
    autoHideMenuBar: true,
    show: false,
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  mainWindow.loadFile(path.join(__dirname, 'renderer', 'index.html'));

  // Harici linkleri tarayıcıda aç
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url).catch(err => log.error('Link açılamadı:', err));
    return { action: 'deny' };
  });

  // Renderer'da harici URL navigation engelle
  mainWindow.webContents.on('will-navigate', (event, url) => {
    if (!url.startsWith('file://')) {
      event.preventDefault();
      shell.openExternal(url).catch(err => log.error('Link açılamadı:', err));
    }
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

function buildMenu() {
  const template = [
    {
      label: 'Dosya',
      submenu: [
        { role: 'reload', label: 'Yenile' },
        { role: 'forceReload', label: 'Zorla Yenile' },
        { type: 'separator' },
        {
          label: 'Güncellemeleri Denetle',
          click: () => checkForUpdatesManually()
        },
        { type: 'separator' },
        { role: 'quit', label: 'Çıkış' }
      ]
    },
    {
      label: 'Düzen',
      submenu: [
        { role: 'undo', label: 'Geri Al' },
        { role: 'redo', label: 'Yinele' },
        { type: 'separator' },
        { role: 'cut', label: 'Kes' },
        { role: 'copy', label: 'Kopyala' },
        { role: 'paste', label: 'Yapıştır' },
        { role: 'selectAll', label: 'Tümünü Seç' }
      ]
    },
    {
      label: 'Görünüm',
      submenu: [
        { role: 'togglefullscreen', label: 'Tam Ekran' },
        { role: 'toggleDevTools', label: 'Geliştirici Araçları', accelerator: 'Ctrl+Shift+I' },
        { type: 'separator' },
        { role: 'resetZoom', label: 'Yakınlaştırmayı Sıfırla' },
        { role: 'zoomIn', label: 'Yakınlaştır' },
        { role: 'zoomOut', label: 'Uzaklaştır' }
      ]
    },
    {
      label: 'Hakkında',
      submenu: [
        {
          label: "Turkmen'S Hakkında",
          click: () => {
            dialog.showMessageBox(mainWindow, {
              type: 'info',
              title: "Turkmen'S",
              message: "Turkmen'S",
              detail: `Yerli sohbet uygulaması\nSürüm ${app.getVersion()}\n\nElectron ${process.versions.electron}\nChromium ${process.versions.chrome}\nNode.js ${process.versions.node}`,
              buttons: ['Tamam']
            });
          }
        },
        {
          label: 'Log Dosyasını Aç',
          click: () => shell.openPath(log.transports.file.getFile().path)
        }
      ]
    }
  ];
  Menu.setApplicationMenu(Menu.buildFromTemplate(template));
}

// --- Auto-updater event'leri ---
let updateCheckInProgress = false;
let manualCheck = false;

autoUpdater.on('checking-for-update', () => {
  log.info('Güncellemeler kontrol ediliyor...');
  if (mainWindow) mainWindow.webContents.send('update:checking');
});

autoUpdater.on('update-available', (info) => {
  log.info('Güncelleme mevcut:', info.version);
  updateCheckInProgress = false;
  if (mainWindow) {
    mainWindow.webContents.send('update:available', {
      version: info.version,
      releaseNotes: info.releaseNotes || '',
      releaseDate: info.releaseDate || ''
    });
  }
});

autoUpdater.on('update-not-available', (info) => {
  log.info('Güncelleme yok. Mevcut:', info.version);
  updateCheckInProgress = false;
  if (manualCheck && mainWindow) {
    dialog.showMessageBox(mainWindow, {
      type: 'info',
      title: 'Güncellemeler',
      message: 'En son sürümü kullanıyorsun.',
      detail: `Sürüm ${app.getVersion()}`,
      buttons: ['Tamam']
    });
  }
  manualCheck = false;
});

autoUpdater.on('download-progress', (progress) => {
  const pct = Math.round(progress.percent);
  log.info(`İndiriliyor: %${pct} (${Math.round(progress.bytesPerSecond / 1024)} KB/s)`);
  if (mainWindow) mainWindow.webContents.send('update:progress', {
    percent: pct,
    bytesPerSecond: progress.bytesPerSecond,
    transferred: progress.transferred,
    total: progress.total
  });
});

autoUpdater.on('update-downloaded', (info) => {
  log.info('Güncelleme indirildi:', info.version);
  if (mainWindow) {
    mainWindow.webContents.send('update:downloaded', {
      version: info.version
    });
  }
});

autoUpdater.on('error', (err) => {
  log.error('Auto-updater hatası:', err);
  updateCheckInProgress = false;
  if (manualCheck && mainWindow) {
    dialog.showMessageBox(mainWindow, {
      type: 'error',
      title: 'Güncelleme Hatası',
      message: 'Güncellemeler kontrol edilemedi.',
      detail: String(err && err.message ? err.message : err),
      buttons: ['Tamam']
    });
  }
  manualCheck = false;
  if (mainWindow) mainWindow.webContents.send('update:error', String(err && err.message ? err.message : err));
});

function checkForUpdates() {
  if (!app.isPackaged) {
    log.info('Geliştirme modu - güncelleme kontrolü atlanıyor');
    return;
  }
  if (updateCheckInProgress) return;
  updateCheckInProgress = true;
  autoUpdater.checkForUpdates().catch(err => {
    log.error('checkForUpdates başarısız:', err);
    updateCheckInProgress = false;
  });
}

function checkForUpdatesManually() {
  if (!app.isPackaged) {
    dialog.showMessageBox(mainWindow, {
      type: 'info',
      title: 'Güncellemeler',
      message: 'Geliştirme modunda güncelleme kontrolü yapılamaz.',
      detail: 'Bu özellik sadece yüklenmiş uygulamada çalışır.',
      buttons: ['Tamam']
    });
    return;
  }
  manualCheck = true;
  checkForUpdates();
}

// --- IPC handlers ---
ipcMain.handle('app:get-version', () => app.getVersion());
ipcMain.handle('app:get-platform', () => process.platform);

ipcMain.handle('update:check', () => {
  checkForUpdatesManually();
});

ipcMain.handle('update:install', () => {
  log.info('Güncelleme yükleniyor, uygulama yeniden başlatılıyor...');
  setImmediate(() => autoUpdater.quitAndInstall(false, true));
});

ipcMain.handle('app:quit', () => app.quit());

// --- App lifecycle ---
app.whenReady().then(() => {
  buildMenu();
  createWindow();

  // İlk açılışta 3 saniye sonra ve sonra her saatte kontrol et
  setTimeout(() => checkForUpdates(), 3000);
  setInterval(() => checkForUpdates(), 60 * 60 * 1000);

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

// Global hata yakalama
process.on('uncaughtException', (err) => {
  log.error('Yakalanmamış istisna:', err);
});
process.on('unhandledRejection', (reason) => {
  log.error('İşlenmemiş promise:', reason);
});
