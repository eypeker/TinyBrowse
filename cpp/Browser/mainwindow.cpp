#include "mainwindow.h"
#include "ui_mainwindow.h"


MainWindow::MainWindow(QWidget *parent): QMainWindow(parent), ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    this->settings = settings::loadSettings();
//    std::cout << this->settings->begin()->first << "Laber" << std::endl;

    this->setWindowTitle("Yeet");
    this->setWindowIcon(QIcon(":/icons/icon.ico"));

    QToolBar * toolbar = new QToolBar;
    toolbar->setMovable(false);
    this->addToolBar(toolbar);

    QPushButton * homeButton = new QPushButton();
    homeButton->setIcon(QIcon(":/icons/home_16.png"));
    QObject::connect(homeButton, SIGNAL (clicked()), this, SLOT(goHome()));
    toolbar->addWidget(homeButton);

    QPushButton * backButton = new QPushButton();
    backButton->setIcon(QIcon(":/icons/back_16.png"));
    QObject::connect(backButton,SIGNAL(clicked()), this, SLOT(back()));
    toolbar->addWidget(backButton);

    QPushButton * forwardButton = new QPushButton();
    forwardButton->setIcon(QIcon(":/icons/forward_16.png"));
    QObject::connect(forwardButton, SIGNAL(clicked()), this, SLOT(forward()));
    toolbar->addWidget(forwardButton);

    this->addressLineEdit = new QLineEdit();
    QObject::connect(this->addressLineEdit, SIGNAL(returnPressed()),this,SLOT(load()));
    toolbar->addWidget(this->addressLineEdit);

    QPushButton * reloadButton = new QPushButton();
    reloadButton->setIcon(QIcon(":/icons/sync_16.png"));
    QObject::connect(reloadButton,SIGNAL(clicked()),this, SLOT(reload()));
    toolbar->addWidget(reloadButton);

    QPushButton * settingsButton = new QPushButton();
    settingsButton->setIcon(QIcon(":/icons/settings_16.png"));
    QObject::connect(settingsButton, SIGNAL(clicked()), this, SLOT(openSettings()));
    toolbar->addWidget(settingsButton);

    QPushButton * closeButton = new QPushButton();
    closeButton->setIcon(QIcon(":/icons/power-off_16.png"));
    QObject::connect(closeButton,SIGNAL(clicked()),this,SLOT(exitApp()));
    toolbar->addWidget(closeButton);


    this->webEngineView = new QWebEngineView();
    this->setCentralWidget(this->webEngineView);
    QObject::connect(this->webEngineView,SIGNAL(titleChanged(const QString&)), this,SLOT(setWindowTitle(const QString &)));
    QObject::connect(this->webEngineView,SIGNAL(urlChanged(const QUrl&)), this, SLOT(urlChanged(QUrl)));

    goHome();
}

MainWindow::~MainWindow()
{
    delete webEngineView;
    delete addressLineEdit;
    delete ui;
}


void MainWindow::load(){
    QUrl url = QUrl::fromUserInput(this->addressLineEdit->text());
    if(url.isValid()){
        this->webEngineView->load(url);
    }
}

void MainWindow::back(){
    this->webEngineView->page()->triggerAction(QWebEnginePage::Back);
}

void MainWindow::forward(){
    this->webEngineView->page()->triggerAction(QWebEnginePage::Forward);
}

void MainWindow::reload(){
    this->addressLineEdit->setText(this->webEngineView->url().toString());
    webEngineView->reload();
}

void MainWindow::urlChanged(QUrl url){
    this->addressLineEdit->setText(url.toString());
}

void MainWindow::goHome(){
    std::string homeurl = this->settings->find("homeurl")->second;
    this->addressLineEdit->setText(QString::fromStdString(homeurl));
    this->load();
}

void MainWindow::openSettings(){
    SettingsDialog sd(this,this->settings);
    sd.setModal(true);
    sd.exec();
}

void MainWindow::exitApp(){
    QMessageBox::StandardButton reply =
            QMessageBox::question(this,"QuitApp","Are you sure you want to quit?",QMessageBox::No | QMessageBox::Yes);
    if(reply == QMessageBox::Yes){
        QApplication::quit();
    }
}




