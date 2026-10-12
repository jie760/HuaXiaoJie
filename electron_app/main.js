const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        title: "我的本地 AI 助手",
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    // 加载你阶段三写好的前端页面
    // 注意这里使用的是相对路径，指向 web 文件夹里的 index.html
    win.loadFile(path.join(__dirname, '../web/index.html'));
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});