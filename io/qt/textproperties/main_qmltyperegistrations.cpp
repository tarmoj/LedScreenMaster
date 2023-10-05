/****************************************************************************
** Generated QML type registration code
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <QtQml/qqml.h>
#include <QtQml/qqmlmoduleregistration.h>

#include </home/tarmo/tarmo/programm/qt-projects/led-screen-master/main.py>


#if !defined(QT_STATIC)
#define Q_QMLTYPE_EXPORT Q_DECL_EXPORT
#else
#define Q_QMLTYPE_EXPORT
#endif
Q_QMLTYPE_EXPORT void qml_register_types_io_qt_textproperties()
{
    qmlRegisterTypesAndRevisions<Bridge>("io.qt.textproperties", 1);
    qmlRegisterModule("io.qt.textproperties", 1, 0);
}

static const QQmlModuleRegistration registration("io.qt.textproperties", qml_register_types_io_qt_textproperties);
