#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QToolBar>
#include <QPushButton>
#include <QLineEdit>
#include <QVBoxLayout>
#include <QtWebEngineWidgets/QWebEnginePage>
#include <QtWebEngineWidgets/QWebEngineView>
#include <QUrl>
#include <QObject>
#include <QDebug>
#include <QMessageBox>
#include "settingsdialog.h"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private:
    QWebEngineView * webEngineView;
    QLineEdit * addressLineEdit;
    SettingType * settings;

private:
    Ui::MainWindow *ui;
private slots:
    void load();
    void back();
    void forward();
    void reload();
    void urlChanged(QUrl);
    void goHome();
    void openSettings();
    void exitApp();

};
#endif // MAINWINDOW_H
