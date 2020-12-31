#ifndef SETTINGSDIALOG_H
#define SETTINGSDIALOG_H

#include <QDialog>
#include <QObject>
#include <string>
#include <iostream>
#include <map>
#include <QMainWindow>
#include <regex>
#include <iostream>
#include <fstream>
#include <QLabel>
#include <QString>
#include <QLineEdit>
namespace Ui {
class SettingsDialog;
}

using namespace std;

typedef pair<string, string> SettingPair;
typedef map<string, string> SettingType;
typedef pair<string, QLineEdit*> FormSettingPair;
typedef map<string, QLineEdit*>   FormSettingMap;
#define SETTINGFILE "./settings.cfg"
#define VALUEREG "^[\\w\\.:/\\-,;=}{[\\]\\\\ ]+$"
#define SETTINGREG "^[\\w]+$"
#define PAIRREG   "([\\w]+):\\s*([\\w\\.:/\\-,;=}{[\\]\\#*+\\- ]+)"



class SettingsDialog : public QDialog
{
    Q_OBJECT

public:
    explicit SettingsDialog(QWidget *parent = nullptr,SettingType * = nullptr);
    ~SettingsDialog();

private slots:
    void on_saveButton_clicked();
    void on_cancelButton_clicked();
    void settingchanged(const QString &);

private:
    Ui::SettingsDialog *ui;
    SettingType * set;
    bool settingschanged;
    FormSettingMap * formmap;

};


namespace settings{
    SettingType * loadSettings();
    bool saveSettings(SettingType *);
}

#endif // SETTINGSDIALOG_H
