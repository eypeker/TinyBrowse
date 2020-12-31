#include "settingsdialog.h"
#include "ui_settingsdialog.h"


    std::string getLineFromValues(SettingPair const*);
    SettingPair * getValuesFromLine(std::string);
    bool valueFitsPattern(std::string);
    bool settingFitsPattern(std::string);
    void removeSettingFile();
    void createSettingFile();



SettingsDialog::SettingsDialog(QWidget *parent,SettingType * set) :
    QDialog(parent),
    ui(new Ui::SettingsDialog)
{
    ui->setupUi(this);
    this->set=set;
    this->settingschanged = false;
    this->formmap= new FormSettingMap();
    QVBoxLayout* vbl = findChild<QVBoxLayout*>("verticalLayout");
    QFormLayout* fml = findChild<QFormLayout*>("formLayout");
    QPushButton* save = this->findChild<QPushButton*>("saveButton");
    save->setDefault(true);
    QLineEdit * let;
    FormSettingPair * fsp;

    for(SettingPair const& x:*set){
        const char * setting = ("&" + x.first).c_str();
        std::string value = x.second.c_str();

        let = new QLineEdit();
        QObject::connect(let,SIGNAL(textEdited(const QString &)),this,SLOT(settingchanged(const QString & )));

        fsp = new FormSettingPair(x.first,let);
        this->formmap->insert(*fsp);

        let->setText(QString::fromUtf8(value.c_str()));
        fml->addRow(this->tr(setting),let);
    }
    this->setLayout(vbl);
}

SettingsDialog::~SettingsDialog()
{
    delete this->formmap;
    delete ui;
}

void SettingsDialog::on_saveButton_clicked()
{
    using namespace std;
    if(this->settingschanged){
        for (const SettingPair& x:*this->set) {
            string key = x.first;
            FormSettingMap::iterator  it = this->formmap->find(key);
            string value = it->second->text().toUtf8().constData();
            (*this->set)[key] = value;
        }
        settings::saveSettings(this->set);
    }
    SettingsDialog::on_cancelButton_clicked();
}

void SettingsDialog::on_cancelButton_clicked(){
    this->close();
}

void SettingsDialog::settingchanged(const QString &){
    this->settingschanged = true;
}


SettingType * settings::loadSettings(){
    SettingType * set = new SettingType();
    std::ifstream configfile;
    configfile.open(SETTINGFILE);
    std::ofstream cfg;


    if(!configfile.good()){
        cfg.open(SETTINGFILE);
        SettingPair * homeurl = new SettingPair("homeurl","https://ecosia.org");
        set->insert(*homeurl);
        cfg << getLineFromValues(homeurl)<<std::endl;
    }
    cfg.close();


    std::string line;
    while(std::getline(configfile,line)){
        SettingPair * values = getValuesFromLine(line);
        if(values==nullptr){

        }else{
            set->insert(*values);
        }
        delete values;
    }
    return set;
}

bool settings::saveSettings(SettingType * setting){
    removeSettingFile();
    createSettingFile();
    std::ofstream configfile (SETTINGFILE);
    for(SettingPair const& x: *setting){
        configfile << getLineFromValues(&x)<<std::endl;
    }
    return true;
}

std::string getLineFromValues( SettingPair const* value){
    std::string line = "";
    line += value ->first + ": " + value->second;
    return line;
}

SettingPair * getValuesFromLine(std::string line){
    std::regex rx(PAIRREG);
    bool match = std::regex_match(line,rx);
    std::smatch m;
    if(match==false)return nullptr;
    std::regex_search(line,m,rx);
    return new SettingPair(m[1],m[2]);
}

void removeSettingFile(){
    remove(SETTINGFILE);
}

void createSettingFile(){
    std::ofstream configfile (SETTINGFILE);
}

bool valueFitsPattern(std::string value){
    std::regex rx(VALUEREG);
    bool match = std::regex_match(value,rx);
    return match;
}

bool settingFitsPattern(std::string setting){
    std::regex rx(SETTINGREG);
    bool match = std::regex_match(setting,rx);
    return match;
}


